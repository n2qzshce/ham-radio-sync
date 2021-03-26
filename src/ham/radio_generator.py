import csv
import logging
import os

from src.ham.dmr.dmr_contact import DmrContact
from src.ham.dmr.dmr_id import DmrId
from src.ham.dmr.dmr_user import DmrUser
from src.ham.radio.radio_additional import RadioAdditionalData
from src.ham.radio.radio_channel import RadioChannel
from src.ham.radio.radio_channel_builder import RadioChannelBuilder
from src.ham.radio.radio_zone import RadioZone
from src.ham.util import radio_types, file_util
from src.ham.util.file_util import FileUtil, RadioWriter
from src.ham.util.validator import Validator


class RadioGenerator:
	def __init__(self, radio_list):
		self.radio_list = radio_list
		self._validator = Validator()

	@classmethod
	def info(cls):
		logging.info("""
		HAM RADIO SYNC GENERATOR
		Homepage: https://github.com/n2qzshce/ham-radio-sync
		
		Purpose: The intent of this program is to generate .csv files to import into various radio applications by using
		a master set of csv files that have all the relevant information.\n
		How to use: Start by running the Wizard to generate the `in` directory and `out` directory.
		For more information about these files, please see:
			https://github.com/n2qzshce/ham-radio-sync/blob/master/INPUTS_OUTPUTS_SYNCING.md
			
		Functions:
			Cleanup - Will delete the contents of your `in` and `out` directory.
			Wizard - Creates sample input files to help you get started.
			Migrate - If you have recently updated ham radio sync, this can add any new columns that may be
				needed. Migrations will rename your existing files by adding a `.bak` extension. You can run the
				"migrations cleanup" to remove these files.
			Create radio plugs - Will generate CSVs to import for the radios you have selected.
			Debug logging - This will enable chattier logging. Generally only needed if you have been instructed to do so.
		""")

	def generate_all_declared(self):
		file_errors = Validator.validate_files_exist()
		if len(file_errors) > 0:
			return

		digital_contacts, digi_contact_errors = self._generate_digital_contact_data()
		dmr_ids, dmr_id_errors = self._generate_dmr_id_data()
		zones, zone_errors = self._generate_zone_data()
		user, user_data_errors = self._generate_user_data()
		preload_errors = digi_contact_errors + dmr_id_errors + zone_errors + user_data_errors

		feed = FileUtil.open_file("in/input.csv", "r")
		csv_reader = csv.DictReader(feed)

		line_num = 1
		radio_channel_errors = []
		for line in csv_reader:
			line_errors = self._validator.validate_radio_channel(line, line_num, feed.name)
			radio_channel_errors += line_errors
			line_num += 1

		all_errors = preload_errors + radio_channel_errors
		if len(all_errors) > 0:
			logging.error("--- VALIDATION ERRORS, CANNOT CONTINUE ---")
			for err in all_errors:
				logging.error(f"\t\tfile: `{err.file_name}` line:{err.line_num} validation error: {err.message}")
		else:
			logging.info("File validation complete, no obvious formatting errors found")

		radio_files = dict()
		radio_channels = dict()
		headers_gen = RadioChannel.create_empty()
		FileUtil.safe_create_dir('out')

		channel_numbers = dict()
		for radio in self.radio_list:
			radio_casted = RadioChannelBuilder.casted(headers_gen, radio)
			FileUtil.safe_create_dir(f'out/{radio}')
			logging.info(f"Generating for radio type `{radio}`")

			if radio_casted.skip_radio_csv(radio):
				logging.info(f"`{radio}` uses special output style. Skipping channels csv")
				continue
			output = RadioWriter(f'out/{radio}/{radio}_channels.csv', '\r\n')
			file_headers = radio_casted.headers(radio)
			output.writerow(file_headers)
			radio_files[radio] = output
			channel_numbers[radio] = 1

		feed.close()
		feed = FileUtil.open_file("in/input.csv", "r")
		csv_reader = csv.DictReader(feed)
		logging.info("Processing radio channels")
		line_num = 1
		for line in csv_reader:
			logging.debug(f"Processing radio line {line_num}")
			if line_num % file_util.RADIO_LINE_LOG_INTERVAL == 0:
				logging.info(f"Processing radio line {line_num}")

			self._validator.validate_radio_channel(line, line_num, feed.name)

			radio_channel = RadioChannel(line, digital_contacts, dmr_ids)
			radio_channels[radio_channel.number] = radio_channel
			line_num += 1

			if radio_channel.zone_id.fmt_val(None) is not None:
				zones[radio_channel.zone_id.fmt_val()].add_channel(radio_channel)

			for radio in self.radio_list:
				casted_channel = RadioChannelBuilder.casted(radio_channel, radio)

				if not radio_types.supports_dmr(radio) and casted_channel.is_digital():
					continue
				if radio not in radio_files.keys():
					continue

				input_data = casted_channel.output(radio, channel_numbers[radio])
				radio_files[radio].writerow(input_data)
				channel_numbers[radio] += 1

		additional_data = RadioAdditionalData(radio_channels, dmr_ids, digital_contacts, zones, user)
		for radio in self.radio_list:
			if radio in radio_files.keys():
				radio_files[radio].close()
			additional_data.output(radio)

		logging.info(f"Radio generator complete. Your output files are in `{os.path.abspath('out')}`")
		return

	def _generate_digital_contact_data(self):
		logging.info("Processing digital contacts")
		feed = FileUtil.open_file("in/digital_contacts.csv", "r")
		csv_feed = csv.DictReader(feed)
		digital_contacts = dict()
		errors = []

		line_num = 1
		for line in csv_feed:
			line_errors = self._validator.validate_digital_contact(line, 1, feed.name)
			errors += line_errors
			line_num += 1
			if len(line_errors) != 0:
				continue
			contact = DmrContact(line)
			digital_contacts[contact.radio_id.fmt_val()] = contact

		return digital_contacts, errors

	def _generate_dmr_id_data(self):
		logging.info("Processing dmr ids")
		feed = FileUtil.open_file("in/dmr_id.csv", "r")
		csv_feed = csv.DictReader(feed)
		dmr_ids = dict()
		errors = []
		line_num = 1
		for line in csv_feed:
			line_errors = self._validator.validate_dmr_id(line, line_num, feed.name)
			errors += line_errors
			line_num += 1
			if len(line_errors) != 0:
				continue
			dmr_id = DmrId(line)
			dmr_ids[dmr_id.number.fmt_val()] = dmr_id

		return dmr_ids, errors

	def _generate_zone_data(self):
		logging.info("Processing zones")
		feed = FileUtil.open_file('in/zones.csv', 'r')
		csv_feed = csv.DictReader(feed)
		zones = dict()
		errors = []
		line_num = 1
		for line in csv_feed:
			line_errors = self._validator.validate_radio_zone(line, line_num, feed.name)
			errors += line_errors
			line_num += 1
			if len(line_errors) != 0:
				continue
			zone = RadioZone(line)
			zones[zone.number.fmt_val()] = zone

		return zones, errors

	def _generate_user_data(self):
		logging.info("Processing dmr IDs. This step can take a while.")
		feed = FileUtil.open_file('in/user.csv', 'r', encoding='utf-8')
		csv_feed = csv.DictReader(feed)
		users = dict()
		errors = []
		rows_processed = 0
		for line in csv_feed:
			line_errors = self._validator.validate_dmr_user(line, rows_processed + 1, feed.name)
			errors += line_errors
			rows_processed += 1
			if len(line_errors) != 0:
				continue
			zone = DmrUser(line)
			users[zone.radio_id.fmt_val()] = zone
			logging.debug(f"Writing user row {rows_processed}")
			if rows_processed % file_util.USER_LINE_LOG_INTERVAL == 0:
				logging.info(f"Processed {rows_processed} DMR users")

		return users, errors

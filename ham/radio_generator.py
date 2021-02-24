import logging
import csv

from ham.util import file_util, radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.dmr.dmr_user import DmrUser
from ham.util.file_util import FileUtil, RadioWriter
from ham.radio.radio_additional import RadioAdditionalData
from ham.radio.radio_channel import RadioChannel
from ham.radio.radio_zone import RadioZone
from ham.util.validation_error import ValidationError
from ham.util.validator import Validator


class RadioGenerator:
	def __init__(self, radio_list):
		self.radio_list = radio_list
		self._validator = Validator()

	def generate_all_declared(self):
		file_errors = self._validate_files_exist()
		if len(file_errors) > 0:
			logging.error("--- FILE MISSING ERRORS, CANNOT CONTINUE ---")
			for err in file_errors:
				logging.error(f"\t\t{err.message}")
			return
		else:
			logging.info("All necessary files found")

		digital_contacts, digi_contact_errors = self._generate_digital_contact_data()
		dmr_ids, dmr_id_errors = self._generate_dmr_id_data()
		zones, zone_errors = self._generate_zone_data()
		user, user_data_errors = self._generate_user_data()

		feed = open("in/input.csv", "r")
		csv_reader = csv.DictReader(feed)

		line_num = 1
		radio_channel_errors = []
		for line in csv_reader:
			line_errors = self._validator.validate_radio_channel(line, line_num, feed.name)
			radio_channel_errors += line_errors
			line_num += 1

		all_errors = digi_contact_errors + dmr_id_errors + zone_errors + user_data_errors + radio_channel_errors
		if len(all_errors) > 0:
			logging.error("--- VALIDATION ERRORS, CANNOT CONTINUE ---")
			for err in all_errors:
				logging.error(f"\t\tfile: `{err.file_name}` line:{err.line_num} validation error: {err.message}")
			return
		else:
			logging.info("File validation complete, no obvious formatting errors found")

		radio_files = dict()
		radio_channels = dict()
		headers_gen = RadioChannel.create_empty()
		FileUtil.safe_create_dir('out')

		channel_numbers = dict()
		for radio in self.radio_list:
			FileUtil.safe_create_dir(f'out/{radio}')
			logging.info(f"Generating for radio type `{radio}`")

			if RadioChannel.skip_radio_csv(radio):
				logging.info(f"`{radio}` uses special output style. Skipping channels csv")
				continue
			output = RadioWriter(f'out/{radio}/{radio}_channels.csv', '\r\n')
			file_headers = headers_gen.headers(radio)
			output.writerow(file_headers)
			radio_files[radio] = output
			channel_numbers[radio] = 1

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
				if not radio_types.supports_dmr(radio) and radio_channel.is_digital():
					continue
				if radio not in radio_files.keys():
					continue

				input_data = radio_channel.output(radio, channel_numbers[radio])
				radio_files[radio].writerow(input_data)
				channel_numbers[radio] += 1

		additional_data = RadioAdditionalData(radio_channels, dmr_ids, digital_contacts, zones, user)
		for radio in self.radio_list:
			if radio in radio_files.keys():
				radio_files[radio].close()
			additional_data.output(radio)

		logging.info("Radio generator complete")
		return

	def _validate_files_exist(self):
		errors = []

		files_list = ["in/input.csv", "in/digital_contacts.csv", "in/dmr_id.csv", 'in/zones.csv', 'in/user.csv']
		for file_name in files_list:
			try:
				f = open(file_name, "r")
				f.close()
			except FileNotFoundError:
				err = ValidationError(f"Cannot open file: `{file_name}`", None, file_name)
				errors.append(err)

		return errors

	def _generate_digital_contact_data(self):
		logging.info("Processing digital contacts")
		feed = open("in/digital_contacts.csv", "r")
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
		feed = open("in/dmr_id.csv", "r")
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
		feed = open('in/zones.csv', 'r')
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
		feed = open('in/user.csv', 'r', encoding='utf-8')
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

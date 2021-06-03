import csv
import logging
import os
from time import sleep

from src import radio_sync_version
from src.ham.migration.migration_manager import MigrationManager
from src.ham.radio.dmr_contact import DmrContact
from src.ham.radio.dmr_id import DmrId
from src.ham.radio.dmr_user import DmrUser
from src.ham.radio.radio_additional import RadioAdditional
from src.ham.radio.radio_additional_builder import RadioAdditionalBuilder
from src.ham.radio.radio_casted_builder import RadioChannelBuilder
from src.ham.radio.radio_channel import RadioChannel
from src.ham.radio.radio_zone import RadioZone
from src.ham.util import radio_types, file_util
from src.ham.util.file_util import FileUtil, RadioWriter
from src.ham.util.path_manager import PathManager
from src.ham.util.validator import Validator


class RadioGenerator:
	def __init__(self, radio_list, ):
		self.radio_list = radio_list
		self._validator = Validator()
		self._migrations = MigrationManager()

	@classmethod
	def info(cls, dangerous_ops_info):
		logging.info(f'''
		HAM RADIO SYNC GENERATOR v{radio_sync_version.version}
		Homepage: https://github.com/n2qzshce/ham-radio-sync

		Purpose: The intent of this program is to generate codeplug files to import into various radio applications by 
		using a master set of csv files that have all the relevant information.

		How to use: Start by running the Wizard to generate the `in` directory and `out` directory.
		For more information about these files, please see:
			https://github.com/n2qzshce/ham-radio-sync/blob/master/INPUTS_OUTPUTS_SYNCING.md
			
		{dangerous_ops_info}

		Functions:
			(Dangerous Operation) Cleanup - Will delete the contents of your `in` and `out` directory.
			(Dangerous Operation) Wizard - Creates sample input files to help you get started.
			(Dangerous Operation) Migrate - If you have recently updated ham radio sync, this can add any new columns that
				may be needed. Migrations will rename your existing files by adding a `.bak` extension. You can run the
				'migrations cleanup' to remove these files.
			Create radio plugs - Will generate CSVs to import for the radios you have selected.
			Debug logging - This will enable chattier logging. Generally only needed if you have been instructed to do so.
		''')

	def generate_all_declared(self):
		file_errors = self._validator.validate_files_exist()
		self._validator.flush_names()
		if len(file_errors) > 0:
			return False

		results = self._migrations.check_migrations_needed()
		if len(results.keys()) > 0:
			logging.warning('You may be using an old version of the input files. Have you run migrations?')
			logging.warning("Migrations check is under the 'File' menu.")
			sleep(1)

		digital_contacts, digi_contact_errors = self._generate_digital_contact_data()
		dmr_ids, dmr_id_errors = self._generate_dmr_id_data()
		zones, zone_errors = self._generate_zone_data()
		user, user_data_errors = self._generate_user_data()
		preload_errors = digi_contact_errors + dmr_id_errors + zone_errors + user_data_errors

		feed = PathManager.open_input_file('input.csv', 'r')
		csv_reader = csv.DictReader(feed)

		radio_channel_errors = []
		radio_channels = []
		line_num = 1
		for line in csv_reader:
			line_errors = self._validator.validate_radio_channel(line, line_num, feed.name, digital_contacts, zones)
			radio_channel_errors += line_errors
			line_num += 1

			if len(line_errors) > 0:
				continue

			radio_channel = RadioChannel(line, digital_contacts, dmr_ids)
			radio_channels.append(radio_channel)

			if radio_channel.zone_id.fmt_val(None) is not None:
				zones[radio_channel.zone_id.fmt_val()].add_channel(radio_channel)
		feed.close()

		all_errors = preload_errors + radio_channel_errors
		if len(all_errors) > 0:
			logging.error('--- VALIDATION ERRORS, CANNOT CONTINUE ---')
			for err in all_errors:
				logging.error(f'\t\tfile: `{err.file_name}` line:{err.line_num} validation error: {err.message}')
			return False
		else:
			logging.info('File validation complete, no obvious formatting errors found')

		radio_files = dict()
		headers_gen = RadioChannel.create_empty()
		FileUtil.safe_create_dir('out')

		channel_numbers = dict()
		for radio in self.radio_list:
			radio_casted = RadioChannelBuilder.casted(headers_gen, radio)
			FileUtil.safe_create_dir(f'out/{radio}')
			logging.info(f'Generating for radio type `{radio}`')

			if radio_casted.skip_radio_csv():
				logging.info(f'`{radio}` uses special output style. Skipping channels csv')
				continue
			output = RadioWriter.output_writer(f'{radio}/{radio}_channels.csv', '\r\n')
			file_headers = radio_casted.headers()
			output.writerow(file_headers)
			radio_files[radio] = output
			channel_numbers[radio] = 1

		logging.info('Processing radio channels')
		line = 1
		for radio_channel in radio_channels:
			logging.debug(f'Processing radio line {line}')
			if line % file_util.RADIO_LINE_LOG_INTERVAL == 0:
				logging.info(f'Processing radio line {line}')
			line += 1
			for radio in self.radio_list:
				if radio not in radio_files.keys():
					continue

				if not radio_types.supports_dmr(radio) and radio_channel.is_digital():
					continue

				casted_channel = RadioChannelBuilder.casted(radio_channel, radio)

				input_data = casted_channel.output(channel_numbers[radio])
				radio_files[radio].writerow(input_data)
				channel_numbers[radio] += 1

		additional_data = RadioAdditional(radio_channels, dmr_ids, digital_contacts, zones, user)
		for radio in self.radio_list:
			if radio in radio_files.keys():
				radio_files[radio].close()
			casted_additional_data = RadioAdditionalBuilder.casted(additional_data, radio)
			casted_additional_data.output()

		logging.info(f'''Radio generator complete. Your output files are in 
					`{os.path.abspath('out')}`
					The next step is to import these files into your radio programming application. (e.g. CHiRP)''')
		return True

	def _generate_digital_contact_data(self):
		logging.info('Processing digital contacts')
		feed = PathManager.open_input_file('digital_contacts.csv', 'r')
		csv_feed = csv.DictReader(feed)
		digital_contacts = dict()
		errors = []

		line_num = 1
		for line in csv_feed:
			logging.debug(f'Processing line {line_num}: `{line}`')
			line_errors = self._validator.validate_digital_contact(line, 1, feed.name)
			errors += line_errors
			line_num += 1
			if len(line_errors) != 0:
				continue
			contact = DmrContact(line)
			digital_contacts[contact.digital_id.fmt_val()] = contact
		feed.close()
		return digital_contacts, errors

	def _generate_dmr_id_data(self):
		logging.info('Processing dmr ids')
		feed = PathManager.open_input_file('dmr_id.csv', 'r')
		csv_feed = csv.DictReader(feed)
		dmr_ids = dict()
		errors = []
		line_num = 0
		for line in csv_feed:
			logging.debug(f'Processing line {line_num}: `{line}`')
			line_num += 1
			line_errors = self._validator.validate_dmr_id(line, line_num, feed.name)
			errors += line_errors
			if len(line_errors) != 0:
				continue
			dmr_id = DmrId(line)
			dmr_ids[line_num] = dmr_id
		feed.close()
		return dmr_ids, errors

	def _generate_zone_data(self):
		logging.info('Processing zones')
		feed = PathManager.open_input_file('zones.csv', 'r')
		csv_feed = csv.DictReader(feed)
		zones = dict()
		errors = []
		line_num = 1
		for line in csv_feed:
			logging.debug(f'Processing line {line_num}: `{line}`')
			line_errors = self._validator.validate_radio_zone(line, line_num, feed.name)
			errors += line_errors
			line_num += 1
			if len(line_errors) != 0:
				continue
			zone = RadioZone(line)
			zones[zone.number.fmt_val()] = zone
		feed.close()
		return zones, errors

	def _generate_user_data(self):
		logging.info('Processing dmr IDs. This step can take a while.')
		feed = PathManager.open_input_file('user.csv', 'r')
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
			logging.debug(f'Writing user row {rows_processed}')
			if rows_processed % file_util.USER_LINE_LOG_INTERVAL == 0:
				logging.info(f'Processed {rows_processed} DMR users')
		feed.close()
		return users, errors

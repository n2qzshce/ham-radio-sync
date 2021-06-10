import csv
import logging
import os
import re
import shutil

from src.ham.radio.default_radio.dmr_contact_default import DmrContactDefault
from src.ham.radio.default_radio.radio_channel_default import RadioChannelDefault
from src.ham.radio.default_radio.radio_zone_default import RadioZoneDefault
from src.ham.util.file_util import FileUtil
from src.ham.util.path_manager import PathManager


class MigrationManager:
	def __init__(self):
		return

	def _add_cols_to_file(self, file_name, cols):
		original_name = PathManager.get_input_path(file_name)
		backup_name = f'{original_name}.bak'
		temp_name = f'{original_name}.tmp'
		os.rename(original_name, backup_name)
		shutil.copyfile(backup_name, temp_name)
		for col in cols:
			self._add_col(f'{file_name}.tmp', col, '')

		os.rename(temp_name, original_name)

	def _add_col(self, file_name, col_name, default_val):
		logging.info(f'Adding column `{col_name}` to `{file_name}`')
		reader = PathManager.open_input_file(f'{file_name}', 'r')
		cols = reader.readline().replace('\n', '').replace('\r', '').split(',')
		if cols == ['']:
			cols = []
		if col_name not in cols:
			cols.append(col_name)
		reader.seek(0)

		writer = PathManager.open_input_file(f'{file_name}.tmp', 'w+')
		dict_writer = csv.DictWriter(writer, fieldnames=cols, dialect='unix', quoting=0)
		dict_reader = csv.DictReader(reader, fieldnames=cols)

		dict_writer.writeheader()
		for row in dict_reader:
			if dict_reader.line_num == 1:
				continue
			for k in row.keys():
				if row[k] is None:
					row[k] = default_val
			dict_writer.writerow(row)

		reader.close()
		writer.close()

		original_name = PathManager.get_input_path(file_name)
		temp_name = f'{original_name}.tmp'

		os.remove(original_name)
		os.rename(temp_name, original_name)
		return

	def _delete_col(self, file_name, col_name):
		logging.info(f'Deleting column `{col_name}` in `{file_name}`')
		reader = PathManager.open_input_file(f'{file_name}', 'r')
		text_line = reader.readline().replace('\n', '')

		old_cols = text_line.split(',')
		cols = text_line.split(',')
		if cols == ['']:
			cols = []
		if col_name in cols:
			cols.remove(col_name)
		reader.seek(0)

		writer = PathManager.open_input_file(f'{file_name}.tmp', 'w+')
		dict_reader = csv.DictReader(reader, fieldnames=old_cols)
		dict_writer = csv.DictWriter(writer, fieldnames=cols, dialect='unix', quoting=0)

		dict_writer.writeheader()
		for row in dict_reader:
			if dict_reader.line_num == 1:
				continue
			if col_name in row.keys():
				row.pop(col_name)
			dict_writer.writerow(row)

		reader.close()
		writer.close()
		os.remove(file_name)
		os.rename(f'{file_name}.tmp', f'{file_name}')
		return

	def remove_backups(self):
		if not PathManager.input_path_exists(''):
			return
		files_list = os.listdir(PathManager.get_input_path())
		for file_name in files_list:
			if re.search('\\.bak$', file_name):
				file_path = PathManager.get_input_path(file_name)
				logging.info(f'Removing backup `{file_path}`')
				os.remove(file_path)
		return

	def check_migrations_needed(self):
		not_needed_cols = dict()

		channels_file = PathManager.get_input_path('input.csv')
		channel_cols = dict(RadioChannelDefault.create_empty().__dict__)
		extra_cols = self._migration_check(channels_file, channel_cols)

		if len(extra_cols) > 0:
			not_needed_cols['input.csv'] = extra_cols

		contacts_file = PathManager.get_input_path('digital_contacts.csv')
		contact_cols = dict(DmrContactDefault.create_empty().__dict__)
		extra_cols = self._migration_check(contacts_file, contact_cols)

		if len(extra_cols) > 0:
			not_needed_cols['digital_contacts.csv'] = extra_cols

		zones_file = PathManager.get_input_path('zones.csv')
		zone_cols = dict(RadioZoneDefault.create_empty().__dict__)
		extra_cols = self._migration_check(zones_file, zone_cols)

		if len(extra_cols) > 0:
			not_needed_cols['zones.csv'] = extra_cols

		return not_needed_cols

	def log_check_migrations(self):
		try:
			results = self.check_migrations_needed()
		except Exception:
			logging.info('Migrations check could not be run. Have you run the setup wizard?')
			return

		output_str = ''
		for k in results.keys():
			for v in results[k]:
				output_str += f'{k:20s} | {v}\n'
		if len(output_str) != 0:
			logging.info(f'The following extra columns were found: \n{"file name":20s} | extra column\n{output_str}')
			logging.info(f'New columns may still be needed. Create radio plugs to validate and create.')
		else:
			logging.info(f'No migrations needed for files in {PathManager.get_input_path()}')

	def _migration_check(self, input_file, needed_cols):
		f = PathManager.open_input_file(input_file, 'r')
		dict_reader = csv.DictReader(f)
		provided_fields = dict_reader.fieldnames
		f.close()

		needed_fields = needed_cols.keys()

		not_needed = []
		for provided in provided_fields:
			if provided not in needed_fields:
				not_needed.append(provided)
		return not_needed

	def migrate(self):
		existing_backups = False
		files_list = []
		if PathManager.input_path_exists(''):
			files_list = os.listdir(PathManager.get_input_path())
		for file_name in files_list:
			if re.search('\\.bak$', file_name):
				logging.warning(f'Existing backup file: `{PathManager.get_input_path(file_name)}`')
				existing_backups = True

		if existing_backups:
			logging.info('Backup files still exist. Please delete before continuing.')
			logging.info('MIGRATIONS HAVE NOT BEEN RUN')
			return

		self._migrate_one()
		self._migrate_two()
		self._migrate_three()
		self._migrate_four()
		self._migrate_five()
		logging.info('Migrations are complete. Your original files have been renamed to have a `.bak` extension.')

	def _migrate_one(self):
		logging.info('Running migration step 1: Creating directories...')
		FileUtil.safe_create_dir('in')
		FileUtil.safe_create_dir('out')

	def _migrate_two(self):
		logging.info('Running migration step 2: Creating in.csv')

		if not PathManager.input_path_exists('input.csv'):
			f = PathManager.open_input_file('input.csv', 'w+')
			f.close()

		if not PathManager.input_path_exists('digital_contacts.csv'):
			f = PathManager.open_input_file('digital_contacts.csv', 'w+')
			f.close()

		if not PathManager.input_path_exists('zones.csv'):
			f = PathManager.open_input_file('zones.csv', 'w+')
			f.close()

		if not PathManager.input_path_exists('user.csv'):
			f = PathManager.open_input_file('user.csv', 'w+')
			f.close()
			user_columns = ['RADIO_ID', 'CALLSIGN', 'FIRST_NAME', 'LAST_NAME', 'CITY', 'STATE', 'COUNTRY', 'REMARKS']
			self._add_cols_to_file(PathManager.get_input_path('user.csv'), user_columns)

		if not PathManager.input_path_exists('dmr_id.csv'):
			f = PathManager.open_input_file('dmr_id.csv', 'w+')
			f.close()

	def _migrate_three(self):
		logging.info('Running migration step 3: adding columns part 1')
		radio_columns = [
									'number', 'name', 'medium_name', 'short_name', 'zone_id', 'rx_freq', 'rx_ctcss',
									'rx_dcs', 'rx_dcs_invert', 'tx_power', 'tx_offset', 'tx_ctcss', 'tx_dcs',
									'tx_dcs_invert', 'digital_timeslot', 'digital_color', 'digital_contact_id'
		]
		self._add_cols_to_file('input.csv', radio_columns)

		contacts_columns = ['number', 'digital_id', 'name', 'call_type']
		self._add_cols_to_file('digital_contacts.csv', contacts_columns)

		dmr_ids_columns = ['number', 'radio_id', 'name']
		self._add_cols_to_file('dmr_id.csv', dmr_ids_columns)

		zone_columns = ['number', 'name']
		self._add_cols_to_file('zones.csv', zone_columns)

	def _migrate_four(self):
		logging.info("Running migration step 4: removing 'number' columns")
		self._delete_col(PathManager.get_input_path('input.csv'), 'number')
		self._delete_col(PathManager.get_input_path('dmr_id.csv'), 'number')
		self._delete_col(PathManager.get_input_path('digital_contacts.csv'), 'number')

	def _migrate_five(self):
		logging.info("Running migration step 5: adding 'latitude' and 'longitude' columns")
		self._add_col(PathManager.get_input_path('input.csv'), 'latitude', None)
		self._add_col(PathManager.get_input_path('input.csv'), 'longitude', None)

import csv
import logging
import os
import re
import shutil

from src.ham.util.file_util import FileUtil


class MigrationManager:
	def __init__(self):
		return

	def _add_cols_to_file(self, file_name, cols):
		os.rename(f'{file_name}', f'{file_name}.bak')
		shutil.copyfile(f'{file_name}.bak', f'{file_name}.tmp')
		for col in cols:
			self._add_col(f'{file_name}.tmp', col, '')

		os.rename(f'{file_name}.tmp', f'{file_name}')

	def _add_col(self, file_name, col_name, default_val):
		logging.info(f'Adding column `{col_name}` to `{file_name}`')
		reader = FileUtil.open_file(f'{file_name}', 'r')
		cols = reader.readline().replace('\n', '').split(',')
		if cols == ['']:
			cols = []
		if col_name not in cols:
			cols.append(col_name)
		reader.seek(0)

		writer = FileUtil.open_file(f'{file_name}.tmp', 'w+')
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
		os.remove(file_name)
		os.rename(f'{file_name}.tmp', f'{file_name}')
		return

	def remove_backups(self):
		if not os.path.exists('in/'):
			return
		files_list = os.listdir('in/')
		for file_name in files_list:
			if re.search('\\.bak$', file_name):
				logging.info(f"Removing backup `in/{file_name}`")
				os.remove(f'in/{file_name}')
		return

	def migrate(self):
		existing_backups = False
		files_list = []
		if os.path.exists('in/'):
			files_list = os.listdir('in/')
		for file_name in files_list:
			if re.search('\\.bak$', file_name):
				logging.warning(f"Existing backup file: `{os.path.abspath('in/'+file_name)}`")
				existing_backups = True

		if existing_backups:
			logging.info("Backup files still exist. Please delete before continuing.")
			logging.info("MIGRATIONS HAVE NOT BEEN RUN")
			return

		self._migrate_one()
		self._migrate_two()
		self._migrate_three()
		logging.info("Migrations are complete. Your original files have been renamed to have a `.bak` extension.")

	def _migrate_one(self):
		logging.info("Running migration step 1: Creating directories...")
		FileUtil.safe_create_dir('in')
		FileUtil.safe_create_dir('out')

	def _migrate_two(self):
		logging.info("Running migration step 2: Creating in.csv")

		if not os.path.exists('in/input.csv'):
			f = FileUtil.open_file('in/input.csv', 'w+')
			f.close()

		if not os.path.exists('in/digital_contacts.csv'):
			f = FileUtil.open_file('in/digital_contacts.csv', 'w+')
			f.close()

		if not os.path.exists('in/zones.csv'):
			f = FileUtil.open_file('in/zones.csv', 'w+')
			f.close()

		if not os.path.exists('in/user.csv'):
			f = FileUtil.open_file('in/user.csv', 'w+')
			f.close()
			user_columns = ['RADIO_ID', 'CALLSIGN', 'FIRST_NAME', 'LAST_NAME', 'CITY', 'STATE', 'COUNTRY', 'REMARKS']
			self._add_cols_to_file('in/user.csv', user_columns)

		if not os.path.exists('in/dmr_id.csv'):
			f = FileUtil.open_file('in/dmr_id.csv', 'w+')
			f.close()

	def _migrate_three(self):
		logging.info("Running migration step 3: adding columns part 1")
		radio_columns = [
									'number', 'name', 'medium_name', 'short_name', 'zone_id', 'rx_freq', 'rx_ctcss',
									'rx_dcs', 'rx_dcs_invert', 'tx_power', 'tx_offset', 'tx_ctcss', 'tx_dcs',
									'tx_dcs_invert', 'digital_timeslot', 'digital_color', 'digital_contact_id'
		]
		self._add_cols_to_file('in/input.csv', radio_columns)

		contacts_columns = ['number', 'digital_id', 'name', 'call_type']
		self._add_cols_to_file('in/digital_contacts.csv', contacts_columns)

		dmr_ids_columns = ['number', 'radio_id', 'name']
		self._add_cols_to_file('in/dmr_id.csv', dmr_ids_columns)

		zone_columns = ['number', 'name']
		self._add_cols_to_file('in/zones.csv', zone_columns)
		return

import csv
import logging
import os
import shutil

USER_LINE_LOG_INTERVAL = 50000
RADIO_LINE_LOG_INTERVAL = 5


class RadioWriter:
	def __init__(self, file_path):
		logging.debug(f'Creating CSV at {file_path}')
		self._writer = open(f'{file_path}', 'w+', encoding='utf-8', newline='\n')
		self._csv_writer = csv.writer(self._writer, dialect='unix', quoting=0)

	def writerow(self, row):
		return self._csv_writer.writerow(row)

	def close(self):
		return self._writer.close()


class FileUtil:
	@classmethod
	def safe_delete_dir(cls, dir_name):
		try:
			shutil.rmtree(f'{dir_name}')
			logging.info(f'`{dir_name}` directory deleted')
		except OSError:
			logging.info(f'No `{dir_name}` directory to delete')

	@classmethod
	def safe_create_dir(cls, dir_name):
		if not os.path.exists(dir_name):
			logging.info(f'Creating directory `{dir_name}`')
			os.mkdir(dir_name)
		else:
			logging.info(f'Directory `{dir_name}` exists, skipping.')

	@classmethod
	def create_radio_writer(cls, file_path):
		radio_writer = RadioWriter(file_path)
		return radio_writer

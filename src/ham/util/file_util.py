import csv
import logging
import os
import shutil

from src.ham.util.path_manager import PathManager

USER_LINE_LOG_INTERVAL = 50000
RADIO_LINE_LOG_INTERVAL = 5


class RadioWriter:
	def __init__(self, file_path, newline_char):
		logging.debug(f'Creating CSV at {file_path}')
		self._writer = open(f'{file_path}', 'w+', encoding='utf-8', newline=newline_char)
		self._csv_writer = csv.writer(self._writer, dialect='unix', quoting=0)

	@classmethod
	def input_writer(cls, file_path, newline_char):
		input_path = PathManager.get_input_path(file_path)
		return RadioWriter(input_path, newline_char)

	@classmethod
	def output_writer(cls, file_path, newline_char):
		output_path = PathManager.get_output_path(file_path)
		return RadioWriter(output_path, newline_char)

	def writerow(self, row):
		return self._csv_writer.writerow(row)

	def write_raw(self, data):
		return self._writer.write(data)

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
			os.mkdir(os.path.join(dir_name))
		else:
			logging.info(f'Directory `{dir_name}` exists, skipping.')


class GlobalConstants:
	logging_formatter = logging.Formatter(
		fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename).6s:%(lineno)3s:  %(message)s',
		datefmt="%Y-%m-%d %H:%M:%S"
	)

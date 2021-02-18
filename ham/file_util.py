import logging
import os
import shutil


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

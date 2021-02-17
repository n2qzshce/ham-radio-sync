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
			logging.info(f'`{dir_name}` exists, skipping.')

	@classmethod
	def line_to_dict(cls, line, headers):
		column_values = dict()
		cols = line.replace('\n', '').split(",")
		if len(headers) != len(cols):
			logging.error(f"Mismatch between lines! Headers: `{','.join(headers)}` Columns: `{','.join(cols)}` Line: `{line}`")
			logging.error(f"Check that lines end with a `,`")
		for i in range(0, len(headers) - 1):
			column_values[headers[i]] = cols[i]
		return column_values

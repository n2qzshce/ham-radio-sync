import csv
import logging

from src.ham.radio.chirp.radio_import_chirp import RadioImportChirp
from src.ham.util import radio_types
from src.ham.util.path_manager import PathManager


class RadioImporter:
	def run_import(self, style, path):
		import_name = PathManager.get_import_path()
		feed = open(import_name, 'r')
		csv_reader = csv.DictReader(feed)

		switch = {
			radio_types.CHIRP: RadioImportChirp,
		}

		if style not in switch.keys():
			feed.close()
			raise Exception(f"Cannot import from {style}")

		channels = []
		errors = []
		for line in csv_reader:
			try:
				channel = switch[style]().run_import(line)
				channels.append(channel)
			except Exception as e:
				errors.append(e)

		feed.close()

		if len(errors) != 0:
			logging.error(f'Failed to import file: `{path}`, Error count: {len(errors)}.')
			raise BaseException("Cannot import file.")
		return channels

import csv
import logging

from src.ham.radio.chirp.radio_import_chirp import RadioImportChirp
from src.ham.radio.default_radio.radio_channel_default import RadioChannelDefault
from src.ham.radio.radio_casted_builder import RadioChannelBuilder
from src.ham.util import radio_types
from src.ham.util.file_util import RadioWriter
from src.ham.util.path_manager import PathManager


class RadioImporter:
	def run_import(self, style, path):
		logging.info(f'Importing file: `{path}`')
		import_name = path
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
			logging.info(f"Importing line `{line['Name']}`")
			try:
				channel = switch[style]().run_import(line, path)
				channels.append(channel)
			except Exception as e:
				errors.append(e)

		feed.close()

		if len(errors) != 0:
			logging.error(f'Failed to import file: `{path}`, Error count: {len(errors)}.')
			raise BaseException("Cannot import file.")
		return channels

	def channels_to_file(self, channels):
		logging.info('Writing imported files.')
		headers = RadioChannelDefault.create_empty().headers()
		writer = RadioWriter.output_writer('import_result.csv', '\r\n')
		writer.writerow(headers)
		channel_num = 1
		for chan in channels:  # who is this for chan
			channel_default = RadioChannelBuilder.casted(chan, radio_types.DEFAULT)
			writer.writerow(channel_default.output(channel_num))
			channel_num += 1
		writer.close()

		result_path = PathManager.get_output_path('import_result.csv')
		logging.info(f'Import complete! Your imported file is in `{result_path}`')
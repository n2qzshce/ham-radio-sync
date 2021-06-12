import logging

from src.ham.radio.chirp.radio_channel_chirp import RadioChannelChirp
from src.ham.radio.radio_channel import RadioChannel
from src.ham.util.validation_error import ValidationError
from src.ham.util.validator import Validator


class RadioImportChirp:
	def __init__(self):
		self.validator = Validator()
		self.validator.flush_names()

	def run_import(self, cols, import_path):
		radio_channel_cols = RadioChannel.generate_empty_dict()
		radio_channel_cols['name'] = cols['Name']
		radio_channel_cols['medium_name'] = cols['Name']
		radio_channel_cols['short_name'] = cols['Name']
		radio_channel_cols['zone_id'] = ''
		radio_channel_cols['rx_freq'] = cols['Frequency']
		radio_channel_cols['rx_ctcss'] = ''

		if cols['Tone'] == 'Tone' or cols['Tone'] == 'TSQL':
			radio_channel_cols['tx_ctcss'] = cols['rToneFreq']

		if cols['Tone'] == 'TSQL':
			radio_channel_cols['rx_ctcss'] = cols['cToneFreq']

		if cols['Tone'] == 'DTCS':
			radio_channel_cols['rx_dcs'] = cols['DtcsCode']
			radio_channel_cols['tx_dcs'] = cols['DtcsCode']
			if cols['DtcsPolarity'][0] == 'R':
				radio_channel_cols['rx_dcs_invert'] = 'True'
			if cols['DtcsPolarity'][1] == 'R':
				radio_channel_cols['tx_dcs_invert'] = 'True'
		radio_channel_cols['tx_power'] = 'High'

		if float(cols['Offset']) != 0:
			neg = 1
			if cols['Duplex'] == '-':
				neg = -1
			radio_channel_cols['tx_offset'] = float(cols['Offset']) * neg

		line_num = int(cols['Location']) + 1

		errors = self.validator.validate_radio_channel(radio_channel_cols, line_num, import_path, None, None)
		for err in errors:
			logging.error(f'\t\tline:{err.line_num} validation error: {err.message}')
			raise ValidationError("Import line failed to parse.", line_num, import_path)

		channel = RadioChannelChirp(radio_channel_cols, None, None)
		return channel

from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types


class RadioChannelChirp(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)
		self.number.set_alias(radio_types.CHIRP, 'Location')
		self.short_name.set_alias(radio_types.CHIRP, 'Name')
		self.rx_freq.set_alias(radio_types.CHIRP, 'Frequency')
		self.rx_ctcss.set_alias(radio_types.CHIRP, 'cToneFreq')
		self.rx_dcs.set_alias(radio_types.CHIRP, 'DtcsCode')
		self.tx_offset.set_alias(radio_types.CHIRP, 'Offset')
		self.tx_ctcss.set_alias(radio_types.CHIRP, 'rToneFreq')

	def skip_radio_csv(self):
		return False

	def headers(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.CHIRP)}")
		output.append(f"{self.short_name.get_alias(radio_types.CHIRP)}")
		output.append(f"{self.rx_freq.get_alias(radio_types.CHIRP)}")
		output.append(f"Duplex")
		output.append(f"{self.tx_offset.get_alias(radio_types.CHIRP)}")
		output.append(f"{'Tone'}")
		output.append(f"{self.tx_ctcss.get_alias(radio_types.CHIRP)}")
		output.append(f"{self.rx_ctcss.get_alias(radio_types.CHIRP)}")
		output.append(f"{self.rx_dcs.get_alias(radio_types.CHIRP)}")
		output.append(f"DtcsPolarity")
		output.append(f"Mode")
		output.append(f"TStep")
		output.append(f"Skip")
		output.append(f"Comment")
		output.append(f"URCALL")
		output.append(f"RPT1CALL")
		output.append(f"RPT2CALL")
		output.append(f"DVCODE")
		return output

	def output(self, channel_number):
		number = channel_number - 1

		duplex = ''
		if self.tx_offset.fmt_val() is not None:
			if self.tx_offset.fmt_val() < 0:
				duplex = '-'
			else:
				duplex = '+'

		tone = ''
		if self.tx_ctcss.fmt_val() is not None:
			tone = 'Tone'
			if self.rx_ctcss.fmt_val() is not None:
				tone = 'TSQL'
		if self.rx_dcs.fmt_val() is not None:
			tone = 'DTCS'

		dtcs_polarity = 'NN'
		if self.rx_dcs_invert.fmt_val() is not None:
			invert_rx = self.rx_dcs_invert.fmt_val()
			if invert_rx:
				dtcs_polarity = 'R' + dtcs_polarity[1]

			invert_tx = self.tx_dcs_invert.fmt_val()
			if invert_tx:
				dtcs_polarity = dtcs_polarity[0] + 'R'

		rx_step = 5.0

		output = list()
		output.append(f"{number}")
		output.append(f"{self.short_name.fmt_val().upper():.7s}")
		output.append(f"{self.rx_freq.fmt_val():.6f}")
		output.append(f"{duplex}")
		output.append(f"{abs(self.tx_offset.fmt_val(0.0)):.6f}")
		output.append(f"{tone}")
		output.append(f"{self.tx_ctcss.fmt_val(67.0):.1f}")
		output.append(f"{self.rx_ctcss.fmt_val(67.0):.1f}")
		output.append(f"{str(self.rx_dcs.fmt_val(23)).zfill(3)}")
		output.append(f"{dtcs_polarity}")
		output.append(f"FM")
		output.append(f"{rx_step:0.2f}")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		return output

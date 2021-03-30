from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types


class RadioChannelFtm400(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)
		self.number.set_alias(radio_types.FTM400_RT, 'Channel Number')
		self.medium_name.set_alias(radio_types.FTM400_RT, 'Name')
		self.rx_freq.set_alias(radio_types.FTM400_RT, 'Receive Frequency')
		self.rx_ctcss.set_alias(radio_types.FTM400_RT, 'CTCSS')
		self.rx_dcs.set_alias(radio_types.FTM400_RT, 'DCS')
		self.tx_offset.set_alias(radio_types.FTM400_RT, 'Offset Frequency')
		self.tx_power.set_alias(radio_types.FTM400_RT, 'Tx Power')

	def skip_radio_csv(self):
		return False

	def headers(self):
		output = list()

		output.append(f"{self.number.get_alias(radio_types.FTM400_RT)}")
		output.append(f"{self.rx_freq.get_alias(radio_types.FTM400_RT)}")
		output.append(f"Transmit Frequency")
		output.append(f"{self.tx_offset.get_alias(radio_types.FTM400_RT)}")
		output.append(f"Offset Direction")
		output.append(f"Operating Mode")
		output.append(f"{self.medium_name.get_alias(radio_types.FTM400_RT)}")
		output.append(f"Show Name")
		output.append(f"Tone Mode")
		output.append(f"{self.rx_ctcss.get_alias(radio_types.FTM400_RT)}")
		output.append(f"{self.rx_dcs.get_alias(radio_types.FTM400_RT)}")
		output.append(f"{self.tx_power.get_alias(radio_types.FTM400_RT)}")
		output.append(f"Skip")
		output.append(f"Step")
		output.append(f"Clock Shift")
		output.append(f"Comment")
		output.append(f"User CTCSS")

		return output

	def output(self, channel_number):
		tx_freq = self.rx_freq.fmt_val() + self.tx_offset.fmt_val(0)

		tx_units = ''
		tx_offset = ''

		abs_tx_offset = abs(self.tx_offset.fmt_val(0))
		if abs_tx_offset > 0:
			tx_units = ' kHz'  # That whitespace is intentional and important
			tx_offset = f'{abs_tx_offset * 1000:.3f}'
			if abs_tx_offset > 1:
				tx_units = ' mHz'
				tx_offset = f'{abs_tx_offset:3f}'

		offset_direction = ''
		if self.tx_offset.fmt_val() is not None:
			if self.tx_offset.fmt_val() > 0:
				offset_direction = 'Plus'
			else:
				offset_direction = 'Minus'

		tone_mode = 'None'
		tone = ''
		if self.tx_ctcss.fmt_val() is not None or self.rx_ctcss.fmt_val() is not None:
			tone = self.rx_ctcss.fmt_val()
			if self.tx_ctcss.fmt_val() is not None:
				tone_mode = 'Tone'
				tone = self.tx_ctcss.fmt_val()
			if self.tx_ctcss.fmt_val() is not None and self.rx_ctcss.fmt_val() is not None:
				tone_mode = 'T Sql'
		if self.rx_dcs.fmt_val() is not None:
			tone_mode = 'DCS'

		output = list()
		output.append(f"{channel_number}")
		output.append(f"{self.rx_freq.fmt_val():.5f}")
		output.append(f"{tx_freq:.5f}")
		output.append(f"{tx_offset}{tx_units}")
		output.append(f"{offset_direction}")
		output.append(f"FM Narrow")
		output.append(f"{self.medium_name.fmt_val()}")
		output.append(f"Large")
		output.append(f"{tone_mode}")
		output.append(f"{tone}")
		output.append(f"{self.rx_dcs.fmt_val('')}")
		output.append(f"{self.tx_power.fmt_val('High')}")
		output.append(f"Off")
		output.append(f"Auto")
		output.append(f"Off")
		output.append(f"")
		output.append(f"300 Hz")

		return output

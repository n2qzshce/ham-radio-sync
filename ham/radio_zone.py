from ham import radio_types
from ham.data_column import DataColumn


class RadioZone:
	def __init__(self, cols):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'], shape=int)
		self.number.set_alias(radio_types.D878, 'No.')

		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.name.set_alias(radio_types.D878, 'Zone Name')
		self._associated_channels = list()

	def add_channel(self, radio_channel):
		self._associated_channels.append(radio_channel)

	@classmethod
	def create_empty(cls):
		col_vals = dict()
		col_vals['number'] = ''
		col_vals['name'] = ''
		return RadioZone(col_vals)

	def headers(self, style):
		switch = {
			radio_types.DEFAULT : self._headers_default,
			radio_types.D878 : self._headers_d878
		}

		return switch[style]()

	def _headers_default(self):
		output = ''
		output += f"{self.number.get_alias(radio_types.DEFAULT)},"
		output += f"{self.name.get_alias(radio_types.DEFAULT)},"
		return output

	def _headers_d878(self):
		output = ''
		output += f'{self.number.get_alias(radio_types.D878)},'  # "No.",
		output += f'{self.name.get_alias(radio_types.D878)},'  # "Zone Name",
		output += f'Zone Channel Member,'  # "Zone Channel Member",
		output += f'Zone Channel Member RX Frequency,'  # "Zone Channel Member RX Frequency",
		output += f'Zone Channel Member TX Frequency,'  # "Zone Channel Member TX Frequency",
		output += f'A Channel,'  # "A Channel",
		output += f'A Channel RX Frequency,'  # "A Channel RX Frequency",
		output += f'A Channel TX Frequency,'  # "A Channel TX Frequency",
		output += f'B Channel,'  # "B Channel",
		output += f'B Channel RX Frequency,'  # "B Channel RX Frequency",
		output += f'B Channel TX Frequency,'  # "B Channel TX Frequency"
		return output

	def output(self, style):
		zone_channel_member = list()
		zone_channel_rx = list()
		zone_channel_tx = list()

		for channel in self._associated_channels:
			zone_channel_member.append(f"{channel.name.fmt_val():.16s}")
			zone_channel_rx.append(f"{channel.rx_freq.fmt_val():.5f}")
			tx_freq = channel.rx_freq.fmt_val() + channel.tx_offset.fmt_val(0)
			zone_channel_tx.append(f"{tx_freq:.5f}")

		a_channel = self._associated_channels[0]
		b_channel = self._associated_channels[0]

		if len(self._associated_channels) > 1:
			b_channel = self._associated_channels[1]

		output = ''
		output += f"{self.number.fmt_val()},"  # "No.",
		output += f"{self.name.fmt_val()},"  # "Zone Name",
		output += f"{'|'.join(zone_channel_member)},"  # "Zone Channel Member",
		output += f"{'|'.join(zone_channel_rx)},"  # "Zone Channel Member RX Frequency",
		output += f"{'|'.join(zone_channel_tx)},"  # "Zone Channel Member TX Frequency",
		output += f"{a_channel.name.fmt_val():.16s},"  # "A Channel",
		output += f"{a_channel.rx_freq.fmt_val():.5f},"  # "A Channel RX Frequency",
		output += f"{a_channel.rx_freq.fmt_val() + a_channel.tx_offset.fmt_val(0):.5f},"  # "A Channel TX Frequency",
		output += f"{b_channel.name.fmt_val():.16s},"   # "B Channel",
		output += f"{b_channel.rx_freq.fmt_val():.5f},"  # "B Channel RX Frequency",
		output += f"{b_channel.rx_freq.fmt_val() + b_channel.tx_offset.fmt_val(0):.5f},"  # "B Channel TX Frequency"
		return output

from src.ham.radio.radio_zone import RadioZone
from src.ham.util import radio_types


class RadioZoneDefault(RadioZone):
	def __init__(self, cols):
		super().__init__(cols)
		self.number.set_alias(radio_types.D878, 'No.')
		self.name.set_alias(radio_types.D878, 'Zone Name')

	def add_channel(self, radio_channel):
		self._associated_channels.append(radio_channel)

	def has_channels(self):
		return len(self._associated_channels) > 0

	def headers(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.name.get_alias(radio_types.DEFAULT)}")
		return output

	def output(self):
		output = list()
		output.append(f"{self.number.fmt_val('')}")
		output.append(f"{self.name.fmt_val('')}")
		return output
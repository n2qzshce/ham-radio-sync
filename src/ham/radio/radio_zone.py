from src.ham.util.data_column import DataColumn


class RadioZone:
	def __init__(self, cols):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'], shape=int)
		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)

		self._associated_channels = list()
		self.cols = cols

	def add_channel(self, radio_channel):
		self._associated_channels.append(radio_channel)

	def has_channels(self):
		return len(self._associated_channels) > 0

	@classmethod
	def create_empty(cls):
		col_vals = dict()
		col_vals['number'] = ''
		col_vals['name'] = ''
		return cls(col_vals)

	def headers(self):
		raise Exception("Base method cannot be called!")

	def output(self):
		raise Exception("Base method cannot be called!")

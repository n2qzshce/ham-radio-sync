from ham import radio_types
from ham.data_column import DataColumn


class DmrId:
	@classmethod
	def create_empty(cls):
		cols = dict()
		cols['number'] = ''
		cols['radio_id'] = ''
		cols['name'] = ''
		return DmrId(cols)

	def __init__(self, cols):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'], shape=int)
		self.number.set_alias(radio_types.D878, 'No.')

		self.radio_id = DataColumn(fmt_name='radio_id', fmt_val=cols['radio_id'], shape=int)
		self.radio_id.set_alias(radio_types.D878, 'Radio ID')

		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.name.set_alias(radio_types.D878, 'Name')

	def headers(self, style):
		switch = {
			radio_types.DEFAULT: self._headers_default,
			radio_types.D878: self._headers_d878,
		}

		return switch[style]()

	def output(self, style):
		switch = {
			radio_types.DEFAULT: self._output_default,
			radio_types.D878: self._output_d878
		}

		return switch[style]()

	def _headers_default(self):
		output = ''
		output += f"{self.number.get_alias(radio_types.DEFAULT)},"
		output += f"{self.radio_id.get_alias(radio_types.DEFAULT)},"
		output += f"{self.name.get_alias(radio_types.DEFAULT)},"
		return output

	def _output_default(self):
		output = ''
		output += f"{self.number.fmt_val()},"
		output += f"{self.radio_id.fmt_val()},"
		output += f"{self.name.fmt_val()},"
		return output

	def _headers_d878(self):
		output = ''
		output += f"{self.number.get_alias(radio_types.D878)},"
		output += f"{self.radio_id.get_alias(radio_types.D878)},"
		output += f"{self.name.get_alias(radio_types.D878)},"
		return output

	def _output_d878(self):
		output = ''
		output += f"{self.number.fmt_val()},"
		output += f"{self.radio_id.fmt_val()},"
		output += f"{self.name.fmt_val()},"
		return output


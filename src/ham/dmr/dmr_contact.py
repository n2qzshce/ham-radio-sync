from src.ham.util import radio_types
from src.ham.util.data_column import DataColumn


class DmrContact:
	@classmethod
	def create_empty(cls):
		cols = dict()
		cols['number'] = ''
		cols['digital_id'] = ''
		cols['name'] = ''
		cols['call_type'] = ''
		return DmrContact(cols)

	def __init__(self, cols):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'], shape=int)
		self.number.set_alias(radio_types.D878, 'No.')
		self.number.set_alias(radio_types.CS800, 'No')

		self.radio_id = DataColumn(fmt_name='digital_id', fmt_val=cols['digital_id'], shape=int)
		self.radio_id.set_alias(radio_types.D878, 'Radio ID')
		self.radio_id.set_alias(radio_types.CS800, 'Call ID')

		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.name.set_alias(radio_types.D878, 'Name')
		self.name.set_alias(radio_types.CS800, 'Call Alias')

		self.call_type = DataColumn(fmt_name='call_type', fmt_val=cols['call_type'], shape=str)
		self.call_type.set_alias(radio_types.D878, 'Call Type')
		self.call_type.set_alias(radio_types.CS800, 'Call Type')
		return

	def headers(self, style):
		switch = {
			radio_types.DEFAULT: self._headers_default,
			radio_types.D878: self._headers_d878,
			radio_types.CS800: self._headers_cs800,
		}

		return switch[style]()

	def output(self, style):
		switch = {
			radio_types.DEFAULT: self._output_default,
			radio_types.D878: self._output_d878,
			radio_types.CS800: self._output_cs800
		}

		return switch[style]()

	def _headers_default(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.radio_id.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.call_type.get_alias(radio_types.DEFAULT)}")
		return output

	def _output_default(self):
		output = list()
		output.append(f"{self.number.fmt_val()}")
		output.append(f"{self.radio_id.fmt_val()}")
		output.append(f"{self.name.fmt_val()}")
		output.append(f"{self.call_type.fmt_val()}")
		return output

	def _headers_d878(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.D878)}")
		output.append(f"{self.radio_id.get_alias(radio_types.D878)}")
		output.append(f"{self.name.get_alias(radio_types.D878)}")
		output.append(f"{self.call_type.get_alias(radio_types.D878)}")
		output.append(f"Call Alert")
		return output

	def _output_d878(self):
		call_type = 'All Call'
		if self.call_type.fmt_val() == 'group':
			call_type = 'Group Call'

		output = list()
		output.append(f"{self.number.fmt_val()}")
		output.append(f"{self.radio_id.fmt_val()}")
		output.append(f"{self.name.fmt_val()}")
		output.append(f"{call_type}")
		output.append(f"None")
		return output

	def _headers_cs800(self):
		output = list()
		output.append(f'{self.number.get_alias(radio_types.CS800)}')
		output.append(f'{self.name.get_alias(radio_types.CS800)}')
		output.append(f'{self.call_type.get_alias(radio_types.CS800)}')
		output.append(f'{self.radio_id.get_alias(radio_types.CS800)}')
		output.append(f'Receive Tone')
		return output

	def _output_cs800(self):
		output = list()
		output.append(f'{self.number.fmt_val()}')
		output.append(f'{self.name.fmt_val()}')
		output.append(f'Group Call')
		output.append(f'{self.radio_id.fmt_val()}')
		output.append(f'No')
		return output


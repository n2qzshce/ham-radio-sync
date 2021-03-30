from src.ham.radio.dmr_contact import DmrContact
from src.ham.util import radio_types


class DmrContactCs800(DmrContact):
	def __init__(self, cols):
		super().__init__(cols)
		self.number.set_alias(radio_types.CS800, 'No')
		self.radio_id.set_alias(radio_types.CS800, 'Call ID')
		self.name.set_alias(radio_types.CS800, 'Call Alias')
		self.call_type.set_alias(radio_types.CS800, 'Call Type')
		return

	def headers(self):
		output = list()
		output.append(f'{self.number.get_alias(radio_types.CS800)}')
		output.append(f'{self.name.get_alias(radio_types.CS800)}')
		output.append(f'{self.call_type.get_alias(radio_types.CS800)}')
		output.append(f'{self.radio_id.get_alias(radio_types.CS800)}')
		output.append(f'Receive Tone')
		return output

	def output(self):
		output = list()
		output.append(f'{self.number.fmt_val()}')
		output.append(f'{self.name.fmt_val()}')
		output.append(f'Group Call')
		output.append(f'{self.radio_id.fmt_val()}')
		output.append(f'No')
		return output

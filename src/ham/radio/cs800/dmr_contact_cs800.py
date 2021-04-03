from src.ham.radio.dmr_contact import DmrContact
from src.ham.util import radio_types


class DmrContactCs800(DmrContact):
	def __init__(self, cols):
		super().__init__(cols)
		self.digital_id.set_alias(radio_types.CS800, 'Call ID')
		self.name.set_alias(radio_types.CS800, 'Call Alias')
		self.call_type.set_alias(radio_types.CS800, 'Call Type')
		return

	def headers(self):
		output = list()
		output.append(f'No')
		output.append(f'{self.name.get_alias(radio_types.CS800)}')
		output.append(f'{self.call_type.get_alias(radio_types.CS800)}')
		output.append(f'{self.digital_id.get_alias(radio_types.CS800)}')
		output.append(f'Receive Tone')
		return output

	def output(self, number):
		output = list()
		output.append(f'{number}')
		output.append(f'{self.name.fmt_val()}')
		output.append(f'Group Call')
		output.append(f'{self.digital_id.fmt_val()}')
		output.append(f'No')
		return output

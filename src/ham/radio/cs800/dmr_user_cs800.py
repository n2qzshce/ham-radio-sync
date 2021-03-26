from src.ham.radio.dmr_user import DmrUser
from src.ham.util import radio_types


class DmrUserCs800(DmrUser):
	def __init__(self, cols, number=None):
		super().__init__(cols, number=number)
		self.number.set_alias(radio_types.CS800, 'No')
		self.callsign.set_alias(radio_types.CS800, 'Call Alias')
		self.radio_id.set_alias(radio_types.CS800, 'Call ID')

	def headers(self):
		output = list()
		output.append(f'{self.number.get_alias(radio_types.CS800)}')
		output.append(f'{self.callsign.get_alias(radio_types.CS800)}')
		output.append(f'Call Type')
		output.append(f'{self.radio_id.get_alias(radio_types.CS800)}')
		output.append(f'Receive Tone')
		return output

	def output(self):
		output = list()
		output.append(f'{self.number.fmt_val()}')
		output.append(f'{self.callsign.fmt_val()} {self.first_name.fmt_val()} {self.last_name.fmt_val("")[:1]}')
		output.append(f'Private Call')
		output.append(f'{self.radio_id.fmt_val()}')
		output.append(f'No')
		return output

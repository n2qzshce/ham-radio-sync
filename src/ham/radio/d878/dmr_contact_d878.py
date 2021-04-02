from src.ham.radio.dmr_contact import DmrContact
from src.ham.util import radio_types


class DmrContactD878(DmrContact):
	def __init__(self, cols):
		super().__init__(cols)
		self.radio_id.set_alias(radio_types.D878, 'Radio ID')
		self.name.set_alias(radio_types.D878, 'Name')
		self.call_type.set_alias(radio_types.D878, 'Call Type')
		return

	def headers(self):
		output = list()
		output.append(f"No.")
		output.append(f"{self.radio_id.get_alias(radio_types.D878)}")
		output.append(f"{self.name.get_alias(radio_types.D878)}")
		output.append(f"{self.call_type.get_alias(radio_types.D878)}")
		output.append(f"Call Alert")
		return output

	def output(self, number):
		call_type = 'All Call'
		if self.call_type.fmt_val() == 'group':
			call_type = 'Group Call'

		output = list()
		output.append(f"{number}")
		output.append(f"{self.radio_id.fmt_val()}")
		output.append(f"{self.name.fmt_val()}")
		output.append(f"{call_type}")
		output.append(f"None")
		return output

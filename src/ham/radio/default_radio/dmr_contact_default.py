from src.ham.radio.dmr_contact import DmrContact
from src.ham.util import radio_types


class DmrContactDefault(DmrContact):

	def __init__(self, cols):
		super().__init__(cols)
		return

	def headers(self):
		output = list()
		output.append(f"{self.radio_id.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.call_type.get_alias(radio_types.DEFAULT)}")
		return output

	def output(self, number):
		output = list()
		output.append(f"{self.radio_id.fmt_val()}")
		output.append(f"{self.name.fmt_val()}")
		output.append(f"{self.call_type.fmt_val()}")
		return output

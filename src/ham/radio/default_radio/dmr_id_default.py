from src.ham.radio.dmr_id import DmrId
from src.ham.util import radio_types


class DmrIdDefault(DmrId):

	def __init__(self, cols):
		super().__init__(cols)

	def headers(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.radio_id.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.name.get_alias(radio_types.DEFAULT)}")
		return output

	def output(self):
		output = list()
		output.append(f"{self.number.fmt_val()}")
		output.append(f"{self.radio_id.fmt_val()}")
		output.append(f"{self.name.fmt_val()}")
		return output

from src.ham.radio.dmr_id import DmrId
from src.ham.util import radio_types


class DmrIdD878(DmrId):
	def __init__(self, cols):
		super().__init__(cols)
		self.number.set_alias(radio_types.D878, 'No.')
		self.radio_id.set_alias(radio_types.D878, 'Radio ID')
		self.name.set_alias(radio_types.D878, 'Name')

	def headers(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.D878)}")
		output.append(f"{self.radio_id.get_alias(radio_types.D878)}")
		output.append(f"{self.name.get_alias(radio_types.D878)}")
		return output

	def output(self):
		output = list()
		output.append(f"{self.number.fmt_val()}")
		output.append(f"{self.radio_id.fmt_val()}")
		output.append(f"{self.name.fmt_val()}")
		return output

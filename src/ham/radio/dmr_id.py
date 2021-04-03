from src.ham.util.data_column import DataColumn


class DmrId:
	@classmethod
	def create_empty(cls):
		cols = dict()
		cols['radio_id'] = ''
		cols['name'] = ''
		return cls(cols)

	def __init__(self, cols):
		self.radio_id = DataColumn(fmt_name='radio_id', fmt_val=cols['radio_id'], shape=int)
		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.cols = cols

	def headers(self):
		raise Exception("Base method cannot be called!")

	def output(self, number):
		raise Exception("Base method cannot be called!")

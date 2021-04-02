from src.ham.util.data_column import DataColumn


class DmrContact:
	@classmethod
	def create_empty(cls):
		cols = dict()
		cols['digital_id'] = ''
		cols['name'] = ''
		cols['call_type'] = ''
		return cls(cols)

	def __init__(self, cols):
		self.radio_id = DataColumn(fmt_name='digital_id', fmt_val=cols['digital_id'], shape=int)
		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.call_type = DataColumn(fmt_name='call_type', fmt_val=cols['call_type'], shape=str)

		self.cols = cols
		return

	def headers(self):
		raise Exception("Base method cannot be called!")

	def output(self):
		raise Exception("Base method cannot be called!")


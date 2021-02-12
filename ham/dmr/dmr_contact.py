from ham.data_column import DataColumn


class DmrContact:
	@classmethod
	def create_empty(cls):
		col_vals = dict()
		col_vals['number'] = ''
		col_vals['radio_id'] = ''
		col_vals['name'] = ''
		col_vals['call_type'] = ''
		return DmrContact(col_vals)

	def __init__(self, cols):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'])
		self.number = DataColumn(fmt_name='radio_id', fmt_val=cols['radio_id'])
		self.number = DataColumn(fmt_name='name', fmt_val=cols['name'])
		self.number = DataColumn(fmt_name='call_type', fmt_val=cols['call_type'])
		return

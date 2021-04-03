from src.ham.util.data_column import DataColumn


class DmrUser:
	@classmethod
	def create_empty(cls):
		cols = dict()
		cols['RADIO_ID'] = ''
		cols['CALLSIGN'] = ''
		cols['FIRST_NAME'] = ''
		cols['LAST_NAME'] = ''
		cols['CITY'] = ''
		cols['STATE'] = ''
		cols['COUNTRY'] = ''
		cols['REMARKS'] = ''
		return cls(cols)

	def __init__(self, cols):
		self.radio_id = DataColumn(fmt_name='RADIO_ID', fmt_val=cols['RADIO_ID'], shape=str)
		self.callsign = DataColumn(fmt_name='CALLSIGN', fmt_val=cols['CALLSIGN'], shape=str)
		self.first_name = DataColumn(fmt_name='FIRST_NAME', fmt_val=cols['FIRST_NAME'], shape=str)
		self.last_name = DataColumn(fmt_name='LAST_NAME', fmt_val=cols['LAST_NAME'], shape=str)
		self.city = DataColumn(fmt_name='CITY', fmt_val=cols['CITY'], shape=str)
		self.state = DataColumn(fmt_name='STATE', fmt_val=cols['STATE'], shape=str)
		self.country = DataColumn(fmt_name='COUNTRY', fmt_val=cols['COUNTRY'], shape=str)
		self.remarks = DataColumn(fmt_name='REMARKS', fmt_val=cols['REMARKS'], shape=str)

		self.cols = cols

	def headers(self):
		raise Exception("Base method cannot be called!")

	def output(self, number):
		raise Exception("Base method cannot be called!")

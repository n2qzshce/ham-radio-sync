from src.ham.radio.dmr_user import DmrUser
from src.ham.util import radio_types
from src.ham.util.data_column import DataColumn


class DmrUserDefault(DmrUser):
	def __init__(self, cols, number=None):
		super().__init__(cols, number=number)
		self.radio_id = DataColumn(fmt_name='RADIO_ID', fmt_val=cols['RADIO_ID'], shape=str)
		self.callsign = DataColumn(fmt_name='CALLSIGN', fmt_val=cols['CALLSIGN'], shape=str)
		self.first_name = DataColumn(fmt_name='FIRST_NAME', fmt_val=cols['FIRST_NAME'], shape=str)
		self.last_name = DataColumn(fmt_name='LAST_NAME', fmt_val=cols['LAST_NAME'], shape=str)
		self.city = DataColumn(fmt_name='CITY', fmt_val=cols['CITY'], shape=str)
		self.state = DataColumn(fmt_name='STATE', fmt_val=cols['STATE'], shape=str)
		self.country = DataColumn(fmt_name='COUNTRY', fmt_val=cols['COUNTRY'], shape=str)
		self.remarks = DataColumn(fmt_name='REMARKS', fmt_val=cols['REMARKS'], shape=str)
		self.number = DataColumn(fmt_name='NUMBER', fmt_val=number, shape=int)
		self.number.set_alias(radio_types.CS800, 'No')

	def headers(self):
		output = list()
		output.append(f"{self.radio_id.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.callsign.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.first_name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.last_name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.city.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.state.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.country.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.remarks.get_alias(radio_types.DEFAULT)}")
		return output

	def output(self):
		output = list()
		output.append(f"{self.radio_id.fmt_val('')}")
		output.append(f"{self.callsign.fmt_val('')}")
		output.append(f"{self.first_name.fmt_val('')}")
		output.append(f"{self.last_name.fmt_val('')}")
		output.append(f"{self.city.fmt_val('')}")
		output.append(f"{self.state.fmt_val('')}")
		output.append(f"{self.country.fmt_val('')}")
		output.append(f"{self.remarks.fmt_val('')}")
		return output

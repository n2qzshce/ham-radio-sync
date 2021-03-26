from src.ham.util.data_column import DataColumn


class RadioChannel:
	@classmethod
	def create_empty(cls):
		col_vals = dict()
		col_vals['number'] = ''
		col_vals['name'] = ''
		col_vals['medium_name'] = ''
		col_vals['short_name'] = ''
		col_vals['zone_id'] = ''
		col_vals['rx_freq'] = ''
		col_vals['rx_ctcss'] = ''
		col_vals['rx_dcs'] = ''
		col_vals['rx_dcs_invert'] = ''
		col_vals['tx_power'] = ''
		col_vals['tx_offset'] = ''
		col_vals['tx_ctcss'] = ''
		col_vals['tx_dcs'] = ''
		col_vals['tx_dcs_invert'] = ''
		col_vals['digital_timeslot'] = ''
		col_vals['digital_color'] = ''
		col_vals['digital_contact_id'] = ''
		return cls(col_vals, digital_contacts=None, dmr_ids=None)

	def __init__(self, cols, digital_contacts, dmr_ids):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'], shape=int)
		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.medium_name = DataColumn(fmt_name='medium_name', fmt_val=cols['medium_name'], shape=str)
		self.short_name = DataColumn(fmt_name='short_name', fmt_val=cols['short_name'], shape=str)
		self.zone_id = DataColumn(fmt_name='zone_id', fmt_val=cols['zone_id'], shape=int)
		self.rx_freq = DataColumn(fmt_name='rx_freq', fmt_val=cols['rx_freq'], shape=float)
		self.rx_ctcss = DataColumn(fmt_name='rx_ctcss', fmt_val=cols['rx_ctcss'], shape=float)
		self.rx_dcs = DataColumn(fmt_name='rx_dcs', fmt_val=cols['rx_dcs'], shape=int)
		self.rx_dcs_invert = DataColumn(fmt_name='rx_dcs_invert', fmt_val=cols['rx_dcs_invert'], shape=bool)
		self.tx_offset = DataColumn(fmt_name='tx_offset', fmt_val=cols['tx_offset'], shape=float)
		self.tx_ctcss = DataColumn(fmt_name='tx_ctcss', fmt_val=cols['tx_ctcss'], shape=float)
		self.tx_dcs = DataColumn(fmt_name='tx_dcs', fmt_val=cols['tx_dcs'], shape=int)
		self.tx_dcs_invert = DataColumn(fmt_name='tx_dcs_invert', fmt_val=cols['tx_dcs_invert'], shape=bool)
		self.digital_timeslot = DataColumn(fmt_name='digital_timeslot', fmt_val=cols['digital_timeslot'], shape=int)
		self.digital_color = DataColumn(fmt_name='digital_color', fmt_val=cols['digital_color'], shape=int)
		self.digital_contact = DataColumn(fmt_name='digital_contact_id', fmt_val=cols['digital_contact_id'], shape=int)
		self.tx_power = DataColumn(fmt_name='tx_power', fmt_val=cols['tx_power'], shape=str)

		self.cols = cols
		self.digital_contacts = digital_contacts
		self.dmr_ids = dmr_ids

	def is_digital(self):
		return self.digital_color.fmt_val() is not None

	def skip_radio_csv(self):
		raise Exception("Base method cannot be called!")

	def headers(self):
		raise Exception("Base method cannot be called!")

	def output(self, channel_number):
		raise Exception("Base method cannot be called!")

# styles
DEFAULT = 'default'
BAOFENG = 'baofeng'

class DataColumn:
	fmt_name = None
	default_val = None

	def __init__(self, fmt_name=None, fmt_val=None):
		self.fmt_name = fmt_name
		self.default_val = fmt_val

	def output(self, is_header):
		if is_header:
			return self.fmt_name
		else:
			return self.default_val


class Group:
	group = DataColumn(fmt_name='Group', fmt_val='')
	name = DataColumn(fmt_name='Name', fmt_val='')

	def __init__(self, row_str):
		cols = row_str.split(',')
		self.group = DataColumn(fmt_name='Group', fmt_val=cols[0])
		self.name = DataColumn(fmt_name='Name', fmt_val=cols[1])

	def output(self, style, is_header):
		switch = {
			DEFAULT: self.output_default,
		}

		return switch[style](is_header)

	def output_default(self, is_header):
		return \
			f"{self.group.output(is_header)},"\
			f"{self.name.output(is_header)}"


class RadioChannel:
	number =			DataColumn(fmt_name='', fmt_val=0)
	name =				DataColumn(fmt_name='', fmt_val=0)
	short_name =		DataColumn(fmt_name='', fmt_val=0)
	group_id =			DataColumn(fmt_name='', fmt_val=0)
	rx_freq =			DataColumn(fmt_name='', fmt_val=0)
	rx_ctcss =			DataColumn(fmt_name='', fmt_val=0)
	rx_dcs =			DataColumn(fmt_name='', fmt_val=0)
	rx_dcs_invert =		DataColumn(fmt_name='', fmt_val=0)
	tx_freq =			DataColumn(fmt_name='', fmt_val=0)
	tx_tone =			DataColumn(fmt_name='', fmt_val=0)
	tx_dcs_invert =		DataColumn(fmt_name='', fmt_val=0)
	is_digital =		DataColumn(fmt_name='', fmt_val=0)
	digital_timeslot =	DataColumn(fmt_name='', fmt_val=0)
	digital_color =		DataColumn(fmt_name='', fmt_val=0)
	digital_contact =	DataColumn(fmt_name='', fmt_val=0)
	band_width =		DataColumn(fmt_name='', fmt_val=0)

	def __init__(self):
		return

	def __init__(self, row_str):
		cols = row_str.split(',')
		self.number = DataColumn(fmt_name='number', fmt_val=cols[0])
		self.name = DataColumn(fmt_name='name', fmt_val=cols[1])
		self.short_name = DataColumn(fmt_name='short_name', fmt_val=cols[2])
		self.group_id = DataColumn(fmt_name='group_id', fmt_val=cols[3])
		self.rx_freq = DataColumn(fmt_name='rx_freq', fmt_val=cols[4])
		self.rx_ctcss = DataColumn(fmt_name='rx_ctcss', fmt_val=cols[5])
		self.rx_dcs = DataColumn(fmt_name='rx_dcs', fmt_val=cols[6])
		self.rx_dcs_invert = DataColumn(fmt_name='rx_dcs_invert', fmt_val=cols[7])
		self.tx_freq = DataColumn(fmt_name='tx_offset', fmt_val=cols[8])
		self.tx_tone = DataColumn(fmt_name='tx_ctcss', fmt_val=cols[9])
		self.tx_dcs_invert = DataColumn(fmt_name='tx_dcs_invert', fmt_val=cols[10])
		self.is_digital = DataColumn(fmt_name='is_digital', fmt_val=cols[11])
		self.digital_timeslot = DataColumn(fmt_name='digital_timeslot', fmt_val=cols[12])
		self.digital_color = DataColumn(fmt_name='digital_color', fmt_val=cols[13])
		self.digital_contact = DataColumn(fmt_name='digital_contact', fmt_val=cols[14])
		self.band_width = DataColumn(fmt_name='band_width', fmt_val=cols[15])

	def output(self, style, is_header):
		switch = {
			DEFAULT: self.output_default,
		}

		return switch[style](is_header)

	def output_default(self, is_header):
		return \
			f"{self.number.output(is_header)},"\
			f"{self.name.output(is_header)},"\
			f"{self.short_name.output(is_header)},"\
			f"{self.group_id.output(is_header)},"\
			f"{self.rx_freq.output(is_header)},"\
			f"{self.rx_ctcss.output(is_header)},"\
			f"{self.rx_dcs.output(is_header)},"\
			f"{self.rx_dcs_invert.output(is_header)},"\
			f"{self.tx_freq.output(is_header)},"\
			f"{self.tx_tone.output(is_header)},"\
			f"{self.tx_dcs_invert.output(is_header)},"\
			f"{self.is_digital.output(is_header)},"\
			f"{self.digital_timeslot.output(is_header)},"\
			f"{self.digital_color.output(is_header)},"\
			f"{self.digital_contact.output(is_header)},"\
			f"{self.band_width.output(is_header)}"

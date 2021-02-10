# styles
import logging

DEFAULT = 'default'
BAOFENG = 'baofeng'


class DataColumn:
	alias_names = dict()
	fmt_val = None

	def __init__(self, fmt_name=None, fmt_val=None):
		self.fmt_val = fmt_val

		self.alias_names = dict()
		self.alias_names[DEFAULT] = fmt_name

	def set_alias(self, style, name):
		self.alias_names[style] = name

	def get_alias(self, style):
		if style not in self.alias_names.keys():
			logging.error(f"Cannot find alias for style: `{style}` of `{self.alias_names[DEFAULT]}`")
		return self.alias_names[style]


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

	def output_default(self):
		return \
			f"{self.group}," \
			f"{self.name}"


class RadioChannel:
	def __init__(self, col_vals):
		self.number = DataColumn(fmt_name='number', fmt_val=col_vals['number'])
		self.number.set_alias(BAOFENG, 'Location')

		self.name = DataColumn(fmt_name='name', fmt_val=col_vals['name'])
		self.short_name = DataColumn(fmt_name='short_name', fmt_val=col_vals['short_name'])
		self.short_name.set_alias(BAOFENG, 'Name')

		self.group_id = DataColumn(fmt_name='group_id', fmt_val=col_vals['group_id'])
		self.rx_freq = DataColumn(fmt_name='rx_freq', fmt_val=col_vals['rx_freq'])
		self.rx_freq.set_alias(BAOFENG, 'Frequency')

		self.rx_ctcss = DataColumn(fmt_name='rx_ctcss', fmt_val=col_vals['rx_ctcss'])
		self.rx_ctcss.set_alias(BAOFENG, 'rToneFreq')

		self.rx_dcs = DataColumn(fmt_name='rx_dcs', fmt_val=col_vals['rx_dcs'])
		self.rx_dcs.set_alias(BAOFENG, 'DtcsCode')

		self.rx_dcs_invert = DataColumn(fmt_name='rx_dcs_invert', fmt_val=col_vals['rx_dcs_invert'])
		self.tx_offset = DataColumn(fmt_name='tx_offset', fmt_val=col_vals['tx_offset'])
		self.tx_offset.set_alias(BAOFENG, 'Offset')

		self.tx_ctcss = DataColumn(fmt_name='tx_ctcss', fmt_val=col_vals['tx_ctcss'])
		self.tx_ctcss.set_alias(BAOFENG, 'cToneFreq')

		self.tx_dcs_invert = DataColumn(fmt_name='tx_dcs_invert', fmt_val=col_vals['tx_dcs_invert'])
		self.digital_timeslot = DataColumn(fmt_name='digital_timeslot', fmt_val=col_vals['digital_timeslot'])
		self.digital_color = DataColumn(fmt_name='digital_color', fmt_val=col_vals['digital_color'])
		self.digital_contact = DataColumn(fmt_name='digital_contact', fmt_val=col_vals['digital_contact'])

	@classmethod
	def make_empty(cls):
		col_vals = dict()
		col_vals['number'] = ''
		col_vals['name'] = ''
		col_vals['short_name'] = ''
		col_vals['group_id'] = ''
		col_vals['rx_freq'] = ''
		col_vals['rx_ctcss'] = ''
		col_vals['rx_dcs'] = ''
		col_vals['rx_dcs_invert'] = ''
		col_vals['tx_offset'] = ''
		col_vals['tx_ctcss'] = ''
		col_vals['tx_dcs_invert'] = ''
		col_vals['digital_timeslot'] = ''
		col_vals['digital_color'] = ''
		col_vals['digital_contact'] = ''
		return RadioChannel(col_vals)

	def output(self, style):
		switch = {
			DEFAULT: self.output_default,
			BAOFENG: self.output_baofeng,
		}

		return switch[style]()

	def headers(self, style):
		switch = {
			DEFAULT: self.headers_default,
			BAOFENG: self.headers_baofeng,
		}

		return switch[style]()

	def headers_default(self):
		return \
			f"{self.number.get_alias(DEFAULT)}," \
			f"{self.name.get_alias(DEFAULT)}," \
			f"{self.short_name.get_alias(DEFAULT)}," \
			f"{self.group_id.get_alias(DEFAULT)}," \
			f"{self.rx_freq.get_alias(DEFAULT)}," \
			f"{self.rx_ctcss.get_alias(DEFAULT)}," \
			f"{self.rx_dcs.get_alias(DEFAULT)}," \
			f"{self.rx_dcs_invert.get_alias(DEFAULT)}," \
			f"{self.tx_offset.get_alias(DEFAULT)}," \
			f"{self.tx_ctcss.get_alias(DEFAULT)}," \
			f"{self.tx_dcs_invert.get_alias(DEFAULT)}," \
			f"{self.digital_timeslot.get_alias(DEFAULT)}," \
			f"{self.digital_color.get_alias(DEFAULT)}," \
			f"{self.digital_contact.get_alias(DEFAULT)},"

	def headers_baofeng(self):
		return \
			f"{self.number.get_alias(BAOFENG)}," \
			f"{self.short_name.get_alias(BAOFENG)}," \
			f"{self.rx_freq.get_alias(BAOFENG)}," \
			f"Duplex," \
			f"{self.tx_offset.get_alias(BAOFENG)}," \
			f"{'Tone'}," \
			f"{self.rx_ctcss.get_alias(BAOFENG)}," \
			f"{self.tx_ctcss.get_alias(BAOFENG)}," \
			f"{self.rx_dcs.get_alias(BAOFENG)}," \
			f"DtcsPolarity," \
			f"Mode," \
			f"TStep," \
			f"Skip," \
			f"Comment," \
			f"URCALL," \
			f"RPT1CALL," \
			f"RPT2CALL," \
			f"DVCODE,"

	def output_default(self):
		return \
			f"{self.number.fmt_val}," \
			f"{self.name.fmt_val}," \
			f"{self.short_name.fmt_val}," \
			f"{self.group_id.fmt_val}," \
			f"{self.rx_freq.fmt_val}," \
			f"{self.rx_ctcss.fmt_val}," \
			f"{self.rx_dcs.fmt_val}," \
			f"{self.rx_dcs_invert.fmt_val}," \
			f"{self.tx_offset.fmt_val}," \
			f"{self.tx_ctcss.fmt_val}," \
			f"{self.tx_dcs_invert.fmt_val}," \
			f"{self.digital_timeslot.fmt_val}," \
			f"{self.digital_color.fmt_val}," \
			f"{self.digital_contact.fmt_val}," \

	def output_baofeng(self):
		number = int(self.number.fmt_val) - 1
		rx_freq = float(self.rx_freq.fmt_val)
		tx_offset = 0
		if self.tx_offset.fmt_val != '':
			tx_offset = float(self.tx_offset.fmt_val)

		duplex = ''
		if tx_offset != 0:
			if tx_offset < 0:
				duplex = '-'
			else:
				duplex = '+'

		tone = ''
		if self.tx_ctcss.fmt_val != '':
			tone = 'Tone'
			if self.rx_ctcss.fmt_val != '':
				tone = 'TSQL'
		if self.rx_dcs.fmt_val != '':
			tone = 'DTCS'

		rx_ctcss = 67.0
		if self.rx_ctcss.fmt_val != '':
			rx_ctcss = float(self.rx_ctcss.fmt_val)

		tx_ctcss = 67.0
		if self.tx_ctcss.fmt_val != '':
			tx_ctcss = float(self.tx_ctcss.fmt_val)

		rx_dcs = 23
		if self.rx_dcs.fmt_val != '':
			rx_dcs = int(self.rx_dcs.fmt_val)

		dtcs_polarity = 'NN'
		if self.rx_dcs_invert != '':
			invert_rx = self.rx_dcs_invert == 'true'
			if invert_rx:
				dtcs_polarity = 'R' + dtcs_polarity[1]

			invert_tx = self.tx_dcs_invert == 'true'
			if invert_tx:
				dtcs_polarity = dtcs_polarity[0] + 'R'

		return \
			f"{number}," \
			f"{self.short_name.fmt_val.upper():.7s}," \
			f"{rx_freq:.6f}," \
			f"{duplex}," \
			f"{abs(tx_offset):.6f}," \
			f"{tone}," \
			f"{rx_ctcss:.1f}," \
			f"{tx_ctcss:.1f}," \
			f"{str(rx_dcs).zfill(3)}," \
			f"{dtcs_polarity}," \
			f"FM," \
			f"{5.0:0.2f}," \
			f"," \
			f"," \
			f"," \
			f"," \
			f"," \
			f","

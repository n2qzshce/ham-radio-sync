# styles
import logging

DEFAULT = 'default'
BAOFENG = 'baofeng'
FTM400 = 'ftm400'


class DataColumn:
	_alias_names = dict()
	_fmt_val = None
	_shape = None

	def __init__(self, fmt_name=None, fmt_val=None, shape=None):
		self._fmt_val = fmt_val
		self._alias_names = dict()
		self._alias_names[DEFAULT] = fmt_name
		self._shape = shape

	def set_alias(self, style, name):
		self._alias_names[style] = name

	def get_alias(self, style):
		if style not in self._alias_names.keys():
			logging.error(f"Cannot find alias for style: `{style}` of `{self._alias_names[DEFAULT]}`")
		return self._alias_names[style]
	
	def fmt_val(self, none_val=None):
		if self._fmt_val == '':
			return none_val

		return self._shape(self._fmt_val)


class Group:
	def __init__(self, row_str):
		cols = row_str.split(',')
		self.group_id = DataColumn(fmt_name='Group ID', fmt_val=cols[0])
		self.name = DataColumn(fmt_name='Name', fmt_val=cols[1])

	def header(self, style):
		switch = {
			DEFAULT: self.header_default,
		}

		return switch[style]()

	def header_default(self):
		return \
			f"{self.group_id.get_alias(DEFAULT)}," \
			f"{self.name.get_alias(DEFAULT)}"

	def output(self, style):
		switch = {
			DEFAULT: self.output_default,
		}

		return switch[style]()

	def output_default(self):
		return \
			f"{self.group_id.fmt_val()}," \
			f"{self.name.fmt_val()}"


class RadioChannel:
	def __init__(self, col_vals):
		self.number = DataColumn(fmt_name='number', fmt_val=col_vals['number'], shape=int)
		self.number.set_alias(BAOFENG, 'Location')
		self.number.set_alias(FTM400, 'Channel Number')

		self.name = DataColumn(fmt_name='name', fmt_val=col_vals['name'], shape=str)
		self.medium_name = DataColumn(fmt_name='medium_name', fmt_val=col_vals['medium_name'], shape=str)
		self.medium_name.set_alias(FTM400, 'Name')

		self.short_name = DataColumn(fmt_name='short_name', fmt_val=col_vals['short_name'], shape=str)
		self.short_name.set_alias(BAOFENG, 'Name')

		self.group_id = DataColumn(fmt_name='group_id', fmt_val=col_vals['group_id'], shape=int)
		self.rx_freq = DataColumn(fmt_name='rx_freq', fmt_val=col_vals['rx_freq'], shape=float)
		self.rx_freq.set_alias(BAOFENG, 'Frequency')
		self.rx_freq.set_alias(FTM400, 'Receive Frequency')

		self.rx_ctcss = DataColumn(fmt_name='rx_ctcss', fmt_val=col_vals['rx_ctcss'], shape=float)
		self.rx_ctcss.set_alias(BAOFENG, 'rToneFreq')
		self.rx_ctcss.set_alias(FTM400, 'CTCSS')

		self.rx_dcs = DataColumn(fmt_name='rx_dcs', fmt_val=col_vals['rx_dcs'], shape=float)
		self.rx_dcs.set_alias(BAOFENG, 'DtcsCode')
		self.rx_dcs.set_alias(FTM400, 'DCS')

		self.rx_dcs_invert = DataColumn(fmt_name='rx_dcs_invert', fmt_val=col_vals['rx_dcs_invert'], shape=bool)
		self.tx_offset = DataColumn(fmt_name='tx_offset', fmt_val=col_vals['tx_offset'], shape=float)
		self.tx_offset.set_alias(BAOFENG, 'Offset')
		self.tx_offset.set_alias(FTM400, 'Offset Frequency')

		self.tx_ctcss = DataColumn(fmt_name='tx_ctcss', fmt_val=col_vals['tx_ctcss'], shape=float)
		self.tx_ctcss.set_alias(BAOFENG, 'cToneFreq')

		self.tx_dcs_invert = DataColumn(fmt_name='tx_dcs_invert', fmt_val=col_vals['tx_dcs_invert'], shape=bool)
		self.digital_timeslot = DataColumn(fmt_name='digital_timeslot', fmt_val=col_vals['digital_timeslot'], shape=int)
		self.digital_color = DataColumn(fmt_name='digital_color', fmt_val=col_vals['digital_color'], shape=int)
		self.digital_contact = DataColumn(fmt_name='digital_contact', fmt_val=col_vals['digital_contact'], shape=int)

		self.tx_power = DataColumn(fmt_name='tx_power', fmt_val=col_vals['tx_power'], shape=str)
		self.tx_power.set_alias(FTM400, 'Tx Power')

	@classmethod
	def make_empty(cls):
		col_vals = dict()
		col_vals['number'] = ''
		col_vals['name'] = ''
		col_vals['medium_name'] = ''
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
		col_vals['tx_power'] = ''
		return RadioChannel(col_vals)

	def headers(self, style):
		switch = {
			DEFAULT: self.headers_default,
			BAOFENG: self.headers_baofeng,
			FTM400: self.headers_ftm400,
		}

		return switch[style]()

	def output(self, style):
		switch = {
			DEFAULT: self.output_default,
			BAOFENG: self.output_baofeng,
			FTM400: self.output_ftm400,
		}

		return switch[style]()

	def headers_default(self):
		output = ''
		output += f"{self.number.get_alias(DEFAULT)},"
		output += f"{self.name.get_alias(DEFAULT)},"
		output += f"{self.medium_name.get_alias(DEFAULT)},"
		output += f"{self.short_name.get_alias(DEFAULT)},"
		output += f"{self.group_id.get_alias(DEFAULT)},"
		output += f"{self.rx_freq.get_alias(DEFAULT)},"
		output += f"{self.rx_ctcss.get_alias(DEFAULT)},"
		output += f"{self.rx_dcs.get_alias(DEFAULT)},"
		output += f"{self.rx_dcs_invert.get_alias(DEFAULT)},"
		output += f"{self.tx_offset.get_alias(DEFAULT)},"
		output += f"{self.tx_ctcss.get_alias(DEFAULT)},"
		output += f"{self.tx_dcs_invert.get_alias(DEFAULT)},"
		output += f"{self.digital_timeslot.get_alias(DEFAULT)},"
		output += f"{self.digital_color.get_alias(DEFAULT)},"
		output += f"{self.digital_contact.get_alias(DEFAULT)},"
		return output

	def headers_baofeng(self):
		output = ''
		output += f"{self.number.get_alias(BAOFENG)},"
		output += f"{self.short_name.get_alias(BAOFENG)},"
		output += f"{self.rx_freq.get_alias(BAOFENG)},"
		output += f"Duplex,"
		output += f"{self.tx_offset.get_alias(BAOFENG)},"
		output += f"{'Tone'},"
		output += f"{self.rx_ctcss.get_alias(BAOFENG)},"
		output += f"{self.tx_ctcss.get_alias(BAOFENG)},"
		output += f"{self.rx_dcs.get_alias(BAOFENG)},"
		output += f"DtcsPolarity,"
		output += f"Mode,"
		output += f"TStep,"
		output += f"Skip,"
		output += f"Comment,"
		output += f"URCALL,"
		output += f"RPT1CALL,"
		output += f"RPT2CALL,"
		output += f"DVCODE,"
		return output

	def headers_ftm400(self):
		return \
			f"{self.number.get_alias(FTM400)},"\
			f"{self.rx_freq.get_alias(FTM400)},"\
			f"Transmit Frequency,"\
			f"{self.tx_offset.get_alias(FTM400)},"\
			f"Offset Direction,"\
			f"Operating Mode,"\
			f"{self.medium_name.get_alias(FTM400)},"\
			f"Show Name,"\
			f"Tone Mode,"\
			f"{self.rx_ctcss.get_alias(FTM400)},"\
			f"{self.rx_dcs.get_alias(FTM400)},"\
			f"{self.tx_power.get_alias(FTM400)},"\
			f"Skip,"\
			f"Step,"\
			f"Clock Shift,"\
			f"Comment,"\
			f"User CTCSS,"

	def output_default(self):
		output = ''
		output += f"{self.number.fmt_val('')},"
		output += f"{self.name.fmt_val('')},"
		output += f"{self.medium_name.fmt_val('')},"
		output += f"{self.short_name.fmt_val('')},"
		output += f"{self.group_id.fmt_val('')},"
		output += f"{self.rx_freq.fmt_val('')},"
		output += f"{self.rx_ctcss.fmt_val('')},"
		output += f"{self.rx_dcs.fmt_val('')},"
		output += f"{self.rx_dcs_invert.fmt_val('')},"
		output += f"{self.tx_offset.fmt_val('')},"
		output += f"{self.tx_ctcss.fmt_val('')},"
		output += f"{self.tx_dcs_invert.fmt_val('')},"
		output += f"{self.digital_timeslot.fmt_val('')},"
		output += f"{self.digital_color.fmt_val('')},"
		output += f"{self.digital_contact.fmt_val('')},"
		return output

	def output_baofeng(self):
		number = self.number.fmt_val() - 1

		duplex = ''
		if self.tx_offset.fmt_val() is not None:
			if self.tx_offset.fmt_val() < 0:
				duplex = '-'
			else:
				duplex = '+'

		tone = ''
		if self.tx_ctcss.fmt_val() is not None:
			tone = 'Tone'
			if self.rx_ctcss.fmt_val() is not None:
				tone = 'TSQL'
		if self.rx_dcs.fmt_val() != '':
			tone = 'DTCS'

		dtcs_polarity = 'NN'
		if self.rx_dcs_invert.fmt_val() is not None:
			invert_rx = self.rx_dcs_invert.fmt_val()
			if invert_rx:
				dtcs_polarity = 'R' + dtcs_polarity[1]

			invert_tx = self.tx_dcs_invert.fmt_val()
			if invert_tx:
				dtcs_polarity = dtcs_polarity[0] + 'R'

		output = ''
		output += f"{number},"
		output += f"{self.short_name.fmt_val().upper():.7s},"
		output += f"{self.rx_freq.fmt_val():.6f},"
		output += f"{duplex},"
		output += f"{abs(self.tx_offset.fmt_val(0.0)):.6f},"
		output += f"{tone},"
		output += f"{self.rx_ctcss.fmt_val(67.0):.1f},"
		output += f"{self.tx_ctcss.fmt_val(67.0):.1f},"
		output += f"{str(self.rx_dcs.fmt_val(23)).zfill(3)},"
		output += f"{dtcs_polarity},"
		output += f"FM,"
		output += f"{5.0:0.2f},"
		output += f","
		output += f","
		output += f","
		output += f","
		output += f","
		output += f","
		return output

	def output_ftm400(self):
		tx_freq = self.rx_freq.fmt_val() + self.tx_offset.fmt_val(0)

		tx_units = ''
		tx_offset = ''

		abs_tx_offset = abs(self.tx_offset.fmt_val(0))
		if abs_tx_offset > 0:
			tx_units = ' kHz' #That whitespace is intentional and important
			tx_offset = f'{abs_tx_offset * 1000:.3f}'
			if abs_tx_offset > 1:
				tx_units = ' mHz'
				tx_offset = f'{abs_tx_offset:3f}'

		offset_direction = ''
		if self.tx_offset.fmt_val() is not None:
			if self.tx_offset.fmt_val() > 0:
				offset_direction = 'Plus'
			else:
				offset_direction = 'Minus'

		tone_mode = 'None'
		if self.tx_ctcss.fmt_val() is not None or self.rx_ctcss.fmt_val() is not None:
			if self.tx_ctcss.fmt_val() is not None:
				tone_mode = 'Tone'
			if self.tx_ctcss.fmt_val() is not None and self.tx_ctcss.fmt_val() is not None:
				tone_mode = 'T Sql'
		if self.rx_dcs.fmt_val() is not None:
			tone_mode = 'DCS'

		output = ''
		output += f"{self.number.fmt_val()},"
		output += f"{self.rx_freq.fmt_val():.5f},"
		output += f"{tx_freq:.5f},"
		output += f"{tx_offset}{tx_units},"
		output += f"{offset_direction},"
		output += f"FM Narrow,"
		output += f"{self.medium_name.fmt_val()},"
		output += f"Large,"
		output += f"{tone_mode},"
		output += f"{self.rx_ctcss.fmt_val('')},"
		output += f"{self.rx_dcs.fmt_val('')},"
		output += f"{self.tx_power.fmt_val('High')},"
		output += f"Off,"
		output += f"Auto,"
		output += f"Off,"
		output += f","
		output += f"300 Hz,"

		return output

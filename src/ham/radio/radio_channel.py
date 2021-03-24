from src.ham.util import radio_types
from src.ham.util.data_column import DataColumn


class RadioChannel:
	def __init__(self, cols, digital_contacts, dmr_ids):
		self.number = DataColumn(fmt_name='number', fmt_val=cols['number'], shape=int)
		self.number.set_alias(radio_types.BAOFENG, 'Location')
		self.number.set_alias(radio_types.FTM400, 'Channel Number')
		self.number.set_alias(radio_types.D878, 'No.')
		self.number.set_alias(radio_types.CS800, 'No')

		self.name = DataColumn(fmt_name='name', fmt_val=cols['name'], shape=str)
		self.name.set_alias(radio_types.D878, 'Channel Name')
		self.name.set_alias(radio_types.CS800, 'Channel Alias')

		self.medium_name = DataColumn(fmt_name='medium_name', fmt_val=cols['medium_name'], shape=str)
		self.medium_name.set_alias(radio_types.FTM400, 'Name')

		self.short_name = DataColumn(fmt_name='short_name', fmt_val=cols['short_name'], shape=str)
		self.short_name.set_alias(radio_types.BAOFENG, 'Name')

		self.zone_id = DataColumn(fmt_name='zone_id', fmt_val=cols['zone_id'], shape=int)

		self.rx_freq = DataColumn(fmt_name='rx_freq', fmt_val=cols['rx_freq'], shape=float)
		self.rx_freq.set_alias(radio_types.BAOFENG, 'Frequency')
		self.rx_freq.set_alias(radio_types.FTM400, 'Receive Frequency')
		self.rx_freq.set_alias(radio_types.D878, 'Receive Frequency')
		self.rx_freq.set_alias(radio_types.CS800, 'Receive Frequency')

		self.rx_ctcss = DataColumn(fmt_name='rx_ctcss', fmt_val=cols['rx_ctcss'], shape=float)
		self.rx_ctcss.set_alias(radio_types.BAOFENG, 'cToneFreq')
		self.rx_ctcss.set_alias(radio_types.FTM400, 'CTCSS')

		self.rx_dcs = DataColumn(fmt_name='rx_dcs', fmt_val=cols['rx_dcs'], shape=int)
		self.rx_dcs.set_alias(radio_types.BAOFENG, 'DtcsCode')
		self.rx_dcs.set_alias(radio_types.FTM400, 'DCS')

		self.rx_dcs_invert = DataColumn(fmt_name='rx_dcs_invert', fmt_val=cols['rx_dcs_invert'], shape=bool)
		self.tx_offset = DataColumn(fmt_name='tx_offset', fmt_val=cols['tx_offset'], shape=float)
		self.tx_offset.set_alias(radio_types.BAOFENG, 'Offset')
		self.tx_offset.set_alias(radio_types.FTM400, 'Offset Frequency')

		self.tx_ctcss = DataColumn(fmt_name='tx_ctcss', fmt_val=cols['tx_ctcss'], shape=float)
		self.tx_ctcss.set_alias(radio_types.BAOFENG, 'rToneFreq')

		self.tx_dcs = DataColumn(fmt_name='tx_dcs', fmt_val=cols['tx_dcs'], shape=int)

		self.tx_dcs_invert = DataColumn(fmt_name='tx_dcs_invert', fmt_val=cols['tx_dcs_invert'], shape=bool)

		self.digital_timeslot = DataColumn(fmt_name='digital_timeslot', fmt_val=cols['digital_timeslot'], shape=int)
		self.digital_timeslot.set_alias(radio_types.D878, 'Slot')
		self.digital_timeslot.set_alias(radio_types.CS800, 'Time Slot')

		self.digital_color = DataColumn(fmt_name='digital_color', fmt_val=cols['digital_color'], shape=int)
		self.digital_color.set_alias(radio_types.D878, 'Color Code')
		self.digital_color.set_alias(radio_types.CS800, 'Color Code')

		self.digital_contact = DataColumn(fmt_name='digital_contact_id', fmt_val=cols['digital_contact_id'], shape=int)

		self.tx_power = DataColumn(fmt_name='tx_power', fmt_val=cols['tx_power'], shape=str)
		self.tx_power.set_alias(radio_types.FTM400, 'Tx Power')
		self.tx_power.set_alias(radio_types.D878, 'Transmit Power')
		self.tx_power.set_alias(radio_types.CS800, 'Power Level')

		self.digital_contacts = digital_contacts
		self.dmr_ids = dmr_ids

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
		return RadioChannel(col_vals, digital_contacts=None, dmr_ids=None)

	def is_digital(self):
		return self.digital_color.fmt_val() is not None

	@classmethod
	def skip_radio_csv(cls, style):
		switch = {
			radio_types.DEFAULT: False,
			radio_types.BAOFENG: False,
			radio_types.FTM400: False,
			radio_types.D878: False,
			radio_types.CS800: True,
		}

		return switch[style]

	def headers(self, style):
		switch = {
			radio_types.DEFAULT: self._headers_default,
			radio_types.BAOFENG: self._headers_baofeng,
			radio_types.FTM400: self._headers_ftm400,
			radio_types.D878: self._headers_d878,
			radio_types.CS800: self._headers_cs800,
		}

		return switch[style]()

	def output(self, style, channel_number):
		switch = {
			radio_types.DEFAULT: self._output_default,
			radio_types.BAOFENG: self._output_baofeng,
			radio_types.FTM400: self._output_ftm400,
			radio_types.D878: self._output_d878,
			radio_types.CS800: self._output_cs800,
		}

		return switch[style](channel_number)

	def _headers_default(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.medium_name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.short_name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.zone_id.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_power.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_freq.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_ctcss.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_dcs.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_dcs_invert.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_offset.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_ctcss.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_dcs.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_dcs_invert.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.digital_timeslot.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.digital_color.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.digital_contact.get_alias(radio_types.DEFAULT)}")
		return output

	def _output_default(self, channel_number):
		output = list()
		output.append(f"{channel_number}")
		output.append(f"{self.name.fmt_val('')}")
		output.append(f"{self.medium_name.fmt_val('')}")
		output.append(f"{self.short_name.fmt_val('')}")
		output.append(f"{self.zone_id.fmt_val('')}")
		output.append(f"{self.tx_power.fmt_val('')}")
		output.append(f"{self.rx_freq.fmt_val('')}")
		output.append(f"{self.rx_ctcss.fmt_val('')}")
		output.append(f"{self.rx_dcs.fmt_val('')}")
		output.append(f"{self.rx_dcs_invert.fmt_val('')}")
		output.append(f"{self.tx_offset.fmt_val('')}")
		output.append(f"{self.tx_ctcss.fmt_val('')}")
		output.append(f"{self.tx_dcs.fmt_val('')}")
		output.append(f"{self.tx_dcs_invert.fmt_val('')}")
		output.append(f"{self.digital_timeslot.fmt_val('')}")
		output.append(f"{self.digital_color.fmt_val('')}")
		output.append(f"{self.digital_contact.fmt_val('')}")
		return output

	def _headers_baofeng(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.BAOFENG)}")
		output.append(f"{self.short_name.get_alias(radio_types.BAOFENG)}")
		output.append(f"{self.rx_freq.get_alias(radio_types.BAOFENG)}")
		output.append(f"Duplex")
		output.append(f"{self.tx_offset.get_alias(radio_types.BAOFENG)}")
		output.append(f"{'Tone'}")
		output.append(f"{self.tx_ctcss.get_alias(radio_types.BAOFENG)}")
		output.append(f"{self.rx_ctcss.get_alias(radio_types.BAOFENG)}")
		output.append(f"{self.rx_dcs.get_alias(radio_types.BAOFENG)}")
		output.append(f"DtcsPolarity")
		output.append(f"Mode")
		output.append(f"TStep")
		output.append(f"Skip")
		output.append(f"Comment")
		output.append(f"URCALL")
		output.append(f"RPT1CALL")
		output.append(f"RPT2CALL")
		output.append(f"DVCODE")
		return output

	def _output_baofeng(self, channel_number):
		number = channel_number - 1

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
		if self.rx_dcs.fmt_val() is not None:
			tone = 'DTCS'

		dtcs_polarity = 'NN'
		if self.rx_dcs_invert.fmt_val() is not None:
			invert_rx = self.rx_dcs_invert.fmt_val()
			if invert_rx:
				dtcs_polarity = 'R' + dtcs_polarity[1]

			invert_tx = self.tx_dcs_invert.fmt_val()
			if invert_tx:
				dtcs_polarity = dtcs_polarity[0] + 'R'

		output = list()
		output.append(f"{number}")
		output.append(f"{self.short_name.fmt_val().upper():.7s}")
		output.append(f"{self.rx_freq.fmt_val():.6f}")
		output.append(f"{duplex}")
		output.append(f"{abs(self.tx_offset.fmt_val(0.0)):.6f}")
		output.append(f"{tone}")
		output.append(f"{self.tx_ctcss.fmt_val(67.0):.1f}")
		output.append(f"{self.rx_ctcss.fmt_val(67.0):.1f}")
		output.append(f"{str(self.rx_dcs.fmt_val(23)).zfill(3)}")
		output.append(f"{dtcs_polarity}")
		output.append(f"FM")
		output.append(f"{5.0:0.2f}")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		output.append(f"")
		return output

	def _headers_ftm400(self):
		output = list()

		output.append(f"{self.number.get_alias(radio_types.FTM400)}")
		output.append(f"{self.rx_freq.get_alias(radio_types.FTM400)}")
		output.append(f"Transmit Frequency")
		output.append(f"{self.tx_offset.get_alias(radio_types.FTM400)}")
		output.append(f"Offset Direction")
		output.append(f"Operating Mode")
		output.append(f"{self.medium_name.get_alias(radio_types.FTM400)}")
		output.append(f"Show Name")
		output.append(f"Tone Mode")
		output.append(f"{self.rx_ctcss.get_alias(radio_types.FTM400)}")
		output.append(f"{self.rx_dcs.get_alias(radio_types.FTM400)}")
		output.append(f"{self.tx_power.get_alias(radio_types.FTM400)}")
		output.append(f"Skip")
		output.append(f"Step")
		output.append(f"Clock Shift")
		output.append(f"Comment")
		output.append(f"User CTCSS")

		return output

	def _output_ftm400(self, channel_number):
		tx_freq = self.rx_freq.fmt_val() + self.tx_offset.fmt_val(0)

		tx_units = ''
		tx_offset = ''

		abs_tx_offset = abs(self.tx_offset.fmt_val(0))
		if abs_tx_offset > 0:
			tx_units = ' kHz'  # That whitespace is intentional and important
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
		tone = ''
		if self.tx_ctcss.fmt_val() is not None or self.rx_ctcss.fmt_val() is not None:
			tone = self.rx_ctcss.fmt_val()
			if self.tx_ctcss.fmt_val() is not None:
				tone_mode = 'Tone'
				tone = self.tx_ctcss.fmt_val()
			if self.tx_ctcss.fmt_val() is not None and self.rx_ctcss.fmt_val() is not None:
				tone_mode = 'T Sql'
		if self.rx_dcs.fmt_val() is not None:
			tone_mode = 'DCS'

		output = list()
		output.append(f"{channel_number}")
		output.append(f"{self.rx_freq.fmt_val():.5f}")
		output.append(f"{tx_freq:.5f}")
		output.append(f"{tx_offset}{tx_units}")
		output.append(f"{offset_direction}")
		output.append(f"FM Narrow")
		output.append(f"{self.medium_name.fmt_val()}")
		output.append(f"Large")
		output.append(f"{tone_mode}")
		output.append(f"{tone}")
		output.append(f"{self.rx_dcs.fmt_val('')}")
		output.append(f"{self.tx_power.fmt_val('High')}")
		output.append(f"Off")
		output.append(f"Auto")
		output.append(f"Off")
		output.append(f"")
		output.append(f"300 Hz")

		return output

	def _headers_d878(self):
		output = list()
		output.append(f"{self.number.get_alias(radio_types.D878)}")  # "No.,"
		output.append(f"{self.name.get_alias(radio_types.D878)}")  # "Channel Name,"
		output.append(f"{self.rx_freq.get_alias(radio_types.D878)}")  # "Receive Frequency,"
		output.append(f"Transmit Frequency")  # "Transmit Frequency,"
		output.append(f"Channel Type")  # "Channel Type,"
		output.append(f"{self.tx_power.get_alias(radio_types.D878)}")  # "Transmit Power,"
		output.append(f"Band Width")  # "Band Width,"
		output.append(f"CTCSS/DCS Decode")  # "CTCSS/DCS Decode,"
		output.append(f"CTCSS/DCS Encode")  # "CTCSS/DCS Encode,"
		output.append(f"Contact")  # "Contact,"
		output.append(f"Contact Call Type")  # "Contact Call Type,"
		output.append(f"Contact TG/DMR ID")  # "Contact TG/DMR ID,"
		output.append(f"Radio ID")  # "Radio ID,"
		output.append(f"Busy Lock/TX Permit")  # "Busy Lock/TX Permit,"
		output.append(f"Squelch Mode")  # "Squelch Mode,"
		output.append(f"Optional Signal")  # "Optional Signal,"
		output.append(f"DTMF ID")  # "DTMF ID,"
		output.append(f"2Tone ID")  # "2Tone ID,"
		output.append(f"5Tone ID")  # "5Tone ID,"
		output.append(f"PTT ID")  # "PTT ID,"
		output.append(f"{self.digital_color.get_alias(radio_types.D878)}")  # "Color Code,"
		output.append(f"{self.digital_timeslot.get_alias(radio_types.D878)}")  # "Slot,"
		output.append(f"Scan List")  # "Scan List,"
		output.append(f"Receive Group List")  # "Receive Group List,"
		output.append(f"PTT Prohibit")  # "PTT Prohibit,"
		output.append(f"Reverse")  # "Reverse,"
		output.append(f"Simplex TDMA")  # "Simplex TDMA,"
		output.append(f"Slot Suit")  # "Slot Suit,"
		output.append(f"AES Digital Encryption")  # "AES Digital Encryption,"
		output.append(f"Digital Encryption")  # "Digital Encryption,"
		output.append(f"Call Confirmation")  # "Call Confirmation,"
		output.append(f"Talk Around(Simplex)")  # "Talk Around(Simplex)," #todo dmr talkaround
		output.append(f"Work Alone")  # "Work Alone,"
		output.append(f"Custom CTCSS")  # "Custom CTCSS,"
		output.append(f"2TONE Decode")  # "2TONE Decode,"
		output.append(f"Ranging")  # "Ranging,"
		output.append(f"Through Mode")  # "Through Mode,"
		output.append(f"Digi APRS RX")  # "Digi APRS RX,"
		output.append(f"Analog APRS PTT Mode")  # "Analog APRS PTT Mode,"
		output.append(f"Digital APRS PTT Mode")  # "Digital APRS PTT Mode,"
		output.append(f"APRS Report Type")  # "APRS Report Type,"
		output.append(f"Digital APRS Report Channel")  # "Digital APRS Report Channel,"
		output.append(f"Correct Frequency[Hz]")  # "Correct Frequency[Hz],"
		output.append(f"SMS Confirmation")  # "SMS Confirmation,"
		output.append(f"Exclude channel from roaming")  # "Exclude channel from roaming,"
		output.append(f"DMR MODE")  # "DMR MODE,"
		output.append(f"DataACK Disable")  # "DataACK Disable,"
		output.append(f"R5toneBot")  # "R5toneBot,"
		output.append(f"R5ToneEot")  # "R5ToneEot,"
		return output

	def _output_d878(self, channel_number):
		tx_frequency = self.rx_freq.fmt_val() + self.tx_offset.fmt_val(0)

		channel_type = 'A-Analog'
		busy_lock = 'Off'
		dmr_mode = 0
		contact_call_type = 'All Call'
		contact = self.digital_contacts[self.digital_contact.fmt_val(0)]
		dmr_name = self.dmr_ids[1].name.fmt_val()
		contact_id = self.dmr_ids[1].radio_id.fmt_val()
		call_confirmation = 'Off'
		if self.is_digital():
			channel_type = 'D-Digital'
			busy_lock = 'Always'
			dmr_mode = 1
			contact_call_type = 'Group Call'
			contact_id = contact.radio_id.fmt_val()
			call_confirmation = 'On'

		ctcs_dcs_decode = 'Off'
		if self.rx_ctcss.fmt_val() is not None or self.rx_dcs.fmt_val() is not None:
			if self.rx_ctcss.fmt_val() is not None:
				ctcs_dcs_decode = f"{self.rx_ctcss.fmt_val():.1f}"
			if self.rx_dcs.fmt_val() is not None:
				polarity = 'N'
				if self.rx_dcs_invert.fmt_val(False):
					polarity = 'I'
				dcs_code = int(self.rx_dcs.fmt_val())
				ctcs_dcs_decode = f"D{str(dcs_code).zfill(3)}{polarity}"

		ctcs_dcs_encode = 'Off'
		if self.tx_ctcss.fmt_val() is not None or self.tx_dcs.fmt_val() is not None:
			if self.tx_ctcss.fmt_val() is not None:
				ctcs_dcs_encode = f"{self.tx_ctcss.fmt_val():.1f}"
			if self.tx_dcs.fmt_val() is not None:
				polarity = 'N'
				if self.tx_dcs_invert.fmt_val(False):
					polarity = 'I'
				dcs_code = int(self.rx_dcs.fmt_val())
				ctcs_dcs_encode = f"D{str(dcs_code).zfill(3)}{polarity}"

		output = list()
		output.append(f"{channel_number}")  # "No.,"
		output.append(f"{self.name.fmt_val():.16s}")  # "Channel Name,"
		output.append(f"{self.rx_freq.fmt_val():.5f}")  # "Receive Frequency,"
		output.append(f"{tx_frequency:.5f}")  # "Transmit Frequency,"
		output.append(f"{channel_type}")  # "Channel Type,"
		output.append(f"{self.tx_power.fmt_val()}")  # "Transmit Power,"
		output.append(f"12.5K")  # "Band Width,"
		output.append(f"{ctcs_dcs_decode}")  # "CTCSS/DCS Decode,"
		output.append(f"{ctcs_dcs_encode}")  # "CTCSS/DCS Encode,"
		output.append(f"{contact.name.fmt_val()}")  # "Contact,"
		output.append(f"{contact_call_type}")  # "Contact Call Type,"
		output.append(f"{contact_id}")  # "Contact TG/DMR ID,"
		output.append(f"{dmr_name}")  # "Radio ID,"
		output.append(f"{busy_lock}")  # "Busy Lock/TX Permit,"
		output.append(f"Carrier")  # "Squelch Mode,"
		output.append(f"Off")  # "Optional Signal,"
		output.append(f"1")  # "DTMF ID,"
		output.append(f"1")  # "2Tone ID,"
		output.append(f"1")  # "5Tone ID,"
		output.append(f"Off")  # "PTT ID,"
		output.append(f"{self.digital_color.fmt_val(1)}")  # "Color Code,"
		output.append(f"{self.digital_timeslot.fmt_val(1)}")  # "Slot,"
		output.append(f"None")  # "Scan List,"
		output.append(f"None")  # "Receive Group List,"
		output.append(f"Off")  # "PTT Prohibit,"
		output.append(f"Off")  # "Reverse,"
		output.append(f"Off")  # "Simplex TDMA,"
		output.append(f"Off")  # "Slot Suit,"
		output.append(f"Normal Encryption")  # "AES Digital Encryption,"
		output.append(f"Off")  # "Digital Encryption,"
		output.append(f"{call_confirmation}")  # "Call Confirmation,"
		output.append(f"Off")  # "Talk Around(Simplex),"
		output.append(f"Off")  # "Work Alone,"
		output.append(f"251.1")  # "Custom CTCSS,"
		output.append(f"0")  # "2TONE Decode,"
		output.append(f"Off")  # "Ranging,"
		output.append(f"Off")  # "Through Mode,"
		output.append(f"Off")  # "Digi APRS RX,"
		output.append(f"Off")  # "Analog APRS PTT Mode,"
		output.append(f"Off")  # "Digital APRS PTT Mode,"
		output.append(f"Off")  # "APRS Report Type,"
		output.append(f"1")  # "Digital APRS Report Channel,"
		output.append(f"0")  # "Correct Frequency[Hz],"
		output.append(f"Off")  # "SMS Confirmation,"
		output.append(f"0")  # "Exclude channel from roaming,"
		output.append(f"{dmr_mode}")  # "DMR MODE,"
		output.append(f"0")  # "DataACK Disable,"
		output.append(f"0")  # "R5toneBot,"
		output.append(f"0")  # "R5ToneEot,"
		return output

	def _headers_cs800(self):
		if self.is_digital():
			return self._headers_cs800_digital()
		else:
			return self._headers_cs800_analog()

	def _headers_cs800_digital(self):
		output = list()
		output.append(self.number.get_alias(radio_types.CS800))  # No
		output.append(self.name.get_alias(radio_types.CS800))  # Channel Alias
		output.append('Digital Id')  # Digital Id
		output.append(self.digital_color.get_alias(radio_types.CS800))  # Color Code
		output.append(self.digital_timeslot.get_alias(radio_types.CS800))  # Time Slot
		output.append('Scan List')  # Scan List
		output.append('Auto Scan Start')  # Auto Scan Start
		output.append('Rx Only')  # Rx Only
		output.append('Talk Around')  # Talk Around
		output.append('Lone Worker')  # Lone Worker
		output.append('VOX')  # VOX
		output.append(self.rx_freq.get_alias(radio_types.CS800))  # Receive Frequency
		output.append('RX Ref Frequency')  # RX Ref Frequency
		output.append('RX Group List')  # RX Group List
		output.append('Emergency Alarm Indication')  # Emergency Alarm Indication
		output.append('Emergency Alarm Ack')  # Emergency Alarm Ack
		output.append('Emergency Call Indication')  # Emergency Call Indication
		output.append('Transmit Frequency')  # Transmit Frequency
		output.append('TX Ref Frequency')  # TX Ref Frequency
		output.append('TX Contact')  # TX Contact
		output.append('Emergency System')  # Emergency System
		output.append('Power Level')  # Power Level
		output.append('TX Admit')  # TX Admit
		output.append('TX Time-out Time[s]')  # TX Time-out Time[s]
		output.append('TOT Re-key Time[s]')  # TOT Re-key Time[s]
		output.append('TOT Pre-Alert Time[s]')  # TOT Pre-Alert Time[s]
		output.append('Private Call Confirmed')  # Private Call Confirmed
		output.append('Data Call Confirmed')  # Data Call Confirmed
		output.append('Encrypt')  # Encrypt

		return output

	def _headers_cs800_analog(self):
		output = list()
		output.append(f'{self.number.get_alias(radio_types.CS800)}')  # No
		output.append(f'{self.name.get_alias(radio_types.CS800)}')  # Channel Alias
		output.append(f'Squelch Level')  # Squelch Level
		output.append(f'Channel Band[KHz]')  # Channel Band[KHz]
		output.append(f'Personality List')  # Personality List
		output.append(f'Scan List')  # Scan List
		output.append(f'Auto Scan Start')  # Auto Scan Start
		output.append(f'Rx Only')  # Rx Only
		output.append(f'Talk Around')  # Talk Around
		output.append(f'Lone Worker')  # Lone Worker
		output.append(f'VOX')  # VOX
		output.append(f'Scrambler')  # Scrambler
		output.append(f'Emp De-emp')  # Emp De-emp
		output.append(f'{self.rx_freq.get_alias(radio_types.CS800)}')  # Receive Frequency
		output.append(f'RX CTCSS/CDCSS Type')  # RX CTCSS/CDCSS Type
		output.append(f'CTCSS/CDCSS')  # CTCSS/CDCSS
		output.append(f'RX Ref Frequency')  # RX Ref Frequency
		output.append(f'Rx Squelch Mode')  # Rx Squelch Mode
		output.append(f'Monitor Squelch Mode')  # Monitor Squelch Mode
		output.append(f'Channel Switch Squelch Mode')  # Channel Switch Squelch Mode
		output.append(f'Transmit Frequency')  # Transmit Frequency
		output.append(f'TX CTCSS/CDCSS Type')  # TX CTCSS/CDCSS Type
		output.append(f'CTCSS/CDCSS')  # CTCSS/CDCSS
		output.append(f'TX Ref Frequency')  # TX Ref Frequency
		output.append(f'Power Level')  # Power Level
		output.append(f'Tx Admit')  # Tx Admit
		output.append(f'Reverse Burst/Turn off code')  # Reverse Burst/Turn off code
		output.append(f'TX Time-out Time[s]')  # TX Time-out Time[s]
		output.append(f'TOT Re-key Time[s]')  # TOT Re-key Time[s]
		output.append(f'TOT Pre-Alert Time[s]')  # TOT Pre-Alert Time[s]
		output.append(f'CTCSS Tail Revert Option')  # CTCSS Tail Revert Option

		return output

	def _output_cs800(self, channel_number):
		if self.is_digital():
			return self._output_cs800_digital(channel_number)
		else:
			return self._output_cs800_analog(channel_number)

	def _output_cs800_digital(self, channel_number):
		transmit_frequency = self.rx_freq.fmt_val() + self.tx_offset.fmt_val(0)

		output = list()
		output.append(f'{channel_number}')  # No
		output.append(f'{self.name.fmt_val()}')  # Channel Alias
		output.append(f'3')  # Digital Id
		output.append(f'{self.digital_color.fmt_val()}')  # Color Code
		output.append(f'Slot {self.digital_timeslot.fmt_val()}')  # Time Slot
		output.append(f'None')  # Scan List
		output.append(f'Off')  # Auto Scan Start
		output.append(f'Off')  # Rx Only
		output.append(f'Off')  # Talk Around
		output.append(f'Off')  # Lone Worker
		output.append(f'Off')  # VOX
		output.append(f'{self.rx_freq.fmt_val()}')  # Receive Frequency
		output.append(f'Middle')  # RX Ref Frequency
		output.append(f'None')  # RX Group List
		output.append(f'Off')  # Emergency Alarm Indication
		output.append(f'Off')  # Emergency Alarm Ack
		output.append(f'Off')  # Emergency Call Indication
		output.append(f'{transmit_frequency:.4f}')  # Transmit Frequency
		output.append(f'Middle')  # TX Ref Frequency
		output.append(f'{self.digital_contacts[self.digital_contact.fmt_val()].name.fmt_val()}')  # TX Contact
		output.append(f'None')  # Emergency System
		output.append(f'{self.tx_power.fmt_val()}')  # Power Level
		output.append(f'Color Code')  # TX Admit
		output.append(f'180')  # TX Time-out Time[s]
		output.append(f'0')  # TOT Re-key Time[s]
		output.append(f'0')  # TOT Pre-Alert Time[s]
		output.append(f'On')  # Private Call Confirmed
		output.append(f'Off')  # Data Call Confirmed
		output.append(f'Off')  # Encrypt

		return output

	def _output_cs800_analog(self, channel_number):
		transmit_frequency = self.rx_freq.fmt_val() + self.tx_offset.fmt_val(0)
		rx_tone_type = 'NONE'
		rx_tone = 'NONE'
		if self.rx_ctcss.fmt_val() is not None:
			rx_tone_type = 'CTCSS'
			rx_tone = f'{self.rx_ctcss.fmt_val():.1f}'
		if self.rx_dcs.fmt_val() is not None:
			rx_tone_type = 'CDCSS'
			if self.rx_dcs_invert.fmt_val(False):
				rx_tone_type = 'CDCSS INVERT'
			rx_tone = f'{str(self.rx_dcs.fmt_val()).zfill(3)}'
		rx_squelch = 'Audio'
		monitor_squelch = 'Carrier'
		if self.rx_ctcss.fmt_val() is not None or self.rx_dcs.fmt_val() is not None:
			rx_squelch = 'CTCSS/DCS and Audio'
			monitor_squelch = 'CTCSS/CDCSS'
		

		tx_tone_type = 'NONE'
		tx_tone = 'NONE'
		if self.tx_ctcss.fmt_val() is not None:
			tx_tone_type = 'CTCSS'
			tx_tone = f'{self.tx_ctcss.fmt_val():.1f}'
		if self.tx_dcs.fmt_val() is not None:
			tx_tone_type = 'CDCSS'
			if self.tx_dcs_invert.fmt_val(False):
				tx_tone_type = 'CDCSS INVERT'
			tx_tone = f'{str(self.tx_dcs.fmt_val()).zfill(3)}'

		output = list()
		output.append(f'{channel_number}')  # No
		output.append(f'{self.name.fmt_val()}')  # Channel Alias
		output.append(f'Normal')  # Squelch Level
		output.append(f'12.5')  # Channel Band[KHz]
		output.append(f'Personality 1')  # Personality List
		output.append(f'None')  # Scan List
		output.append(f'Off')  # Auto Scan Start
		output.append(f'Off')  # Rx Only
		output.append(f'Off')  # Talk Around
		output.append(f'Off')  # Lone Worker
		output.append(f'Off')  # VOX
		output.append(f'Off')  # Scrambler
		output.append(f'Off')  # Emp De-emp
		output.append(f'{self.rx_freq.fmt_val()}')  # Receive Frequency
		output.append(f'{rx_tone_type}')  # RX CTCSS/CDCSS Type
		output.append(f'{rx_tone}')  # CTCSS/CDCSS
		output.append(f'Middle')  # RX Ref Frequency
		output.append(f'{rx_squelch}')  # Rx Squelch Mode
		output.append(f'{monitor_squelch}')  # Monitor Squelch Mode
		output.append(f'RX Squelch Mode')  # Channel Switch Squelch Mode
		output.append(f'{transmit_frequency:.4f}')  # Transmit Frequency
		output.append(f'{tx_tone_type}')  # TX CTCSS/CDCSS Type
		output.append(f'{tx_tone}')  # CTCSS/CDCSS
		output.append(f'Middle')  # TX Ref Frequency
		output.append(f'{self.tx_power.fmt_val()}')  # Power Level
		output.append(f'Always Allow')  # Tx Admit
		output.append(f'Off')  # Reverse Burst/Turn off code
		output.append(f'180')  # TX Time-out Time[s]
		output.append(f'0')  # TOT Re-key Time[s]
		output.append(f'0')  # TOT Pre-Alert Time[s]
		output.append(f'180')  # CTCSS Tail Revert Option

		return output


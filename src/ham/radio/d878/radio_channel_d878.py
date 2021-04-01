from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types


class RadioChannelD878(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)
		self.name.set_alias(radio_types.D878, 'Channel Name')
		self.rx_freq.set_alias(radio_types.D878, 'Receive Frequency')
		self.digital_timeslot.set_alias(radio_types.D878, 'Slot')
		self.digital_color.set_alias(radio_types.D878, 'Color Code')
		self.tx_power.set_alias(radio_types.D878, 'Transmit Power')

	def skip_radio_csv(self):
		return False

	def headers(self):
		output = list()
		output.append(f"No.")  # "No.,"
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

	def output(self, channel_number):
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


from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types


class RadioChannelCS800(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)
		self.number.set_alias(radio_types.CS800, 'No')
		self.name.set_alias(radio_types.CS800, 'Channel Alias')
		self.rx_freq.set_alias(radio_types.CS800, 'Receive Frequency')
		self.digital_timeslot.set_alias(radio_types.CS800, 'Time Slot')
		self.digital_color.set_alias(radio_types.CS800, 'Color Code')
		self.tx_power.set_alias(radio_types.CS800, 'Power Level')

	def skip_radio_csv(self):
		return True

	def headers(self):
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

	def output(self, channel_number):
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
from src.ham.radio.d878.radio_channel_d878 import RadioChannelD878
from src.ham.radio.dmr_contact import DmrContact
from src.ham.radio.dmr_id import DmrId

from test.base_test_setup import BaseTestSetup


class D878Test(BaseTestSetup):
	def setUp(self):
		self.radio_channel = RadioChannelD878.create_empty()
		self.digital_contacts = dict()
		cols = dict()
		cols['digital_id'] = '00000'
		cols['name'] = 'Analog'
		cols['call_type'] = 'all'
		digital_contact = DmrContact(cols)
		self.digital_contacts[0] = digital_contact

		cols['digital_id'] = '54321'
		cols['name'] = 'Contact1'
		cols['call_type'] = 'group'
		digital_contact = DmrContact(cols)
		self.digital_contacts[54321] = digital_contact

		cols = dict()
		cols['radio_id'] = '12345'
		cols['name'] = 'N0CALL DMR'
		self.digital_ids = {1: DmrId(cols)}

		self.cols = dict()
		self.cols['name'] = ''
		self.cols['medium_name'] = ''
		self.cols['short_name'] = ''
		self.cols['zone_id'] = ''
		self.cols['rx_freq'] = ''
		self.cols['rx_ctcss'] = ''
		self.cols['rx_dcs'] = ''
		self.cols['rx_dcs_invert'] = ''
		self.cols['tx_power'] = ''
		self.cols['tx_offset'] = ''
		self.cols['tx_ctcss'] = ''
		self.cols['tx_dcs'] = ''
		self.cols['tx_dcs_invert'] = ''
		self.cols['digital_timeslot'] = ''
		self.cols['digital_color'] = ''
		self.cols['digital_contact_id'] = ''
		self.cols['latitude'] = ''
		self.cols['longitude'] = ''

	def test_headers(self):
		expected = [
					"No.", "Channel Name", "Receive Frequency", "Transmit Frequency", "Channel Type", "Transmit Power",
					"Band Width", "CTCSS/DCS Decode", "CTCSS/DCS Encode", "Contact", "Contact Call Type", "Contact TG/DMR ID",
					"Radio ID", "Busy Lock/TX Permit", "Squelch Mode", "Optional Signal", "DTMF ID", "2Tone ID",
					"5Tone ID", "PTT ID", "Color Code", "Slot", "Scan List", "Receive Group List", "PTT Prohibit",
					"Reverse", "Simplex TDMA", "Slot Suit", "AES Digital Encryption", "Digital Encryption", "Call Confirmation",
					"Talk Around(Simplex)", "Work Alone", "Custom CTCSS", "2TONE Decode", "Ranging", "Through Mode",
					"Digi APRS RX", "Analog APRS PTT Mode", "Digital APRS PTT Mode", "APRS Report Type",
					"Digital APRS Report Channel", "Correct Frequency[Hz]", "SMS Confirmation", "Exclude channel from roaming",
					"DMR MODE", "DataACK Disable", "R5toneBot", "R5ToneEot"
					]
		generated = self.radio_channel.headers()
		self.assertEqual(expected, generated)

	def test_simplex(self):
		self.cols['name'] = 'National 2m'
		self.cols['medium_name'] = 'Natl 2m'
		self.cols['short_name'] = 'NATL 2M'
		self.cols['rx_freq'] = '146.52'
		self.cols['tx_power'] = 'High'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)

		result = channel.output(1)
		expected = [
					"1", "National 2m", "146.52000", "146.52000", "A-Analog", "High", "12.5K", "Off", "Off", "Analog",
					"All Call", "12345", "N0CALL DMR", "Off", "Carrier", "Off", "1", "1", "1", "Off", "1", "1", "None",
					"None", "Off", "Off", "Off", "Off", "Normal Encryption", "Off", "Off", "Off", "Off", "251.1", "0",
					"Off", "Off", "Off", "Off", "Off", "Off", "1", "0", "Off", "0", "0", "0", "0", "0"
					]
		self.assertEqual(
			expected, result
		)

	def test_uhf_simplex(self):
		self.cols['name'] = 'National 70cm'
		self.cols['medium_name'] = 'Natl 70c'
		self.cols['short_name'] = 'NATL 70'
		self.cols['rx_freq'] = '446.0'
		self.cols['tx_power'] = 'High'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)

		result = channel.output(1)
		expected = [
					"1", "National 70cm", "446.00000", "446.00000", "A-Analog", "High", "12.5K", "Off", "Off", "Analog",
					"All Call", "12345", "N0CALL DMR", "Off", "Carrier", "Off", "1", "1", "1", "Off", "1", "1", "None",
					"None", "Off", "Off", "Off", "Off", "Normal Encryption", "Off", "Off", "Off", "Off", "251.1", "0",
					"Off", "Off", "Off", "Off", "Off", "Off", "1", "0", "Off", "0", "0", "0", "0", "0"
					]
		self.assertEqual(
			expected, result
		)

	def test_vhf_repeater(self):
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '145.310'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '-0.6'
		self.cols['tx_ctcss'] = '100.0'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)
		result = channel.output(3)
		self.assertEqual(
			[
				'3', 'Some Repeater', '145.31000', '144.71000', 'A-Analog', 'High', '12.5K', 'Off', '100.0', 'Analog',
				'All Call', '12345', 'N0CALL DMR', 'Off', 'Carrier', 'Off', '1', '1', '1', 'Off', '1', '1', 'None',
				'None', 'Off', 'Off', 'Off', 'Off', 'Normal Encryption', 'Off', 'Off', 'Off', 'Off', '251.1', '0', 'Off',
				'Off', 'Off', 'Off', 'Off', 'Off', '1', '0', 'Off', '0', '0', '0', '0', '0',
			]
			, result
		)

	def test_positive_offset(self):
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '442.125'
		self.cols['rx_ctcss'] = '127.3'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '5.0'
		self.cols['tx_ctcss'] = '100.0'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)
		result = channel.output(4)

		self.assertEqual(
			[
				'4', 'Some Repeater', '442.12500', '447.12500', 'A-Analog', 'High', '12.5K', '127.3', '100.0', 'Analog',
				'All Call', '12345', 'N0CALL DMR', 'Off', 'Carrier', 'Off', '1', '1', '1', 'Off', '1', '1', 'None',
				'None', 'Off', 'Off', 'Off', 'Off', 'Normal Encryption', 'Off', 'Off', 'Off', 'Off', '251.1', '0', 'Off',
				'Off', 'Off', 'Off', 'Off', 'Off', '1', '0', 'Off', '0', '0', '0', '0', '0',
			], result
		)

	def test_dcs_repeater(self):
		self.cols['name'] = 'Dcs Repeater'
		self.cols['medium_name'] = 'Dcs Rpt'
		self.cols['short_name'] = 'DCS RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['rx_dcs'] = '165'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '-5'
		self.cols['tx_dcs'] = '165'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)
		result = channel.output(5)
		self.assertEqual(
			[
				'5', 'Dcs Repeater', '447.07500', '442.07500', 'A-Analog', 'High', '12.5K', 'D165N', 'D165N', 'Analog',
				'All Call', '12345', 'N0CALL DMR', 'Off', 'Carrier', 'Off', '1', '1', '1', 'Off', '1', '1', 'None',
				'None', 'Off', 'Off', 'Off', 'Off', 'Normal Encryption', 'Off', 'Off', 'Off', 'Off', '251.1', '0', 'Off',
				'Off', 'Off', 'Off', 'Off', 'Off', '1', '0', 'Off', '0', '0', '0', '0', '0',
			], result
		)

	def test_dcs_invert(self):
		self.cols['name'] = 'Dcs Repeater'
		self.cols['medium_name'] = 'Dcs Rpt'
		self.cols['short_name'] = 'DCS RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['rx_dcs'] = '23'
		self.cols['rx_dcs_invert'] = 'true'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '-5'
		self.cols['tx_dcs'] = '23'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)
		result = channel.output(6)
		self.assertEqual(
			[
				'6', 'Dcs Repeater', '447.07500', '442.07500', 'A-Analog', 'High', '12.5K', 'D023I', 'D023N', 'Analog',
				'All Call', '12345', 'N0CALL DMR', 'Off', 'Carrier', 'Off', '1', '1', '1', 'Off', '1', '1', 'None',
				'None', 'Off', 'Off', 'Off', 'Off', 'Normal Encryption', 'Off', 'Off', 'Off', 'Off', '251.1', '0', 'Off',
				'Off', 'Off', 'Off', 'Off', 'Off', '1', '0', 'Off', '0', '0', '0', '0', '0',
			], result
		)

	def test_dmr(self):
		self.cols['name'] = 'Dmr Repeater'
		self.cols['medium_name'] = 'Dmr Rpt'
		self.cols['short_name'] = 'DMR RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '-5'
		self.cols['digital_timeslot'] = '2'
		self.cols['digital_color'] = '3'
		self.cols['digital_contact_id'] = '54321'
		channel = RadioChannelD878(self.cols, self.digital_contacts, self.digital_ids)
		result = channel.output(6)
		self.assertEqual(
			[
				'6', 'Dmr Repeater', '447.07500', '442.07500', 'D-Digital', 'High', '12.5K', 'Off', 'Off', 'Contact1',
				'Group Call', '54321', 'N0CALL DMR', 'Always', 'Carrier', 'Off', '1', '1', '1', 'Off', '3', '2', 'None',
				'None', 'Off', 'Off', 'Off', 'Off', 'Normal Encryption', 'Off', 'On', 'Off', 'Off', '251.1', '0', 'Off',
				'Off', 'Off', 'Off', 'Off', 'Off', '1', '0', 'Off', '0', '1', '0', '0', '0',
			], result
		)

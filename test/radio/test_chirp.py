from src.ham.radio.chirp.radio_channel_chirp import RadioChannelChirp
from test.base_test_setup import BaseTestSetup


class ChirpTest(BaseTestSetup):
	def setUp(self):
		self.radio_channel = RadioChannelChirp.create_empty()

	def test_headers(self):
		result = self.radio_channel.headers()
		self.assertEqual(
			[
				"Location", "Name", "Frequency", "Duplex", "Offset", "Tone", "rToneFreq", "cToneFreq",
				"DtcsCode", "DtcsPolarity", "Mode", "TStep", "Skip", "Comment", "URCALL", "RPT1CALL",
				"RPT2CALL", "DVCODE",
			], result
		)

	def test_simplex(self):
		cols = dict()
		cols['name'] = 'National 2m'
		cols['medium_name'] = 'Natl 2m'
		cols['short_name'] = 'NATL 2M'
		cols['zone_id'] = ''
		cols['rx_freq'] = '146.52'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = ''
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = ''
		cols['tx_offset'] = ''
		cols['tx_ctcss'] = ''
		cols['tx_dcs'] = ''
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		channel = RadioChannelChirp(cols, None, None)
		result = channel.output(1)
		self.assertEqual(
			[
				'0', 'NATL 2M', '146.520000', '', '0.000000', '', '67.0', '67.0',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_uhf_simplex(self):
		cols = dict()
		cols['name'] = 'National 70cm'
		cols['medium_name'] = 'Natl 70c'
		cols['short_name'] = 'NATL 70'
		cols['zone_id'] = ''
		cols['rx_freq'] = '446.0'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = ''
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = ''
		cols['tx_offset'] = ''
		cols['tx_ctcss'] = ''
		cols['tx_dcs'] = ''
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		channel = RadioChannelChirp(cols, None, None)
		result = channel.output(2)
		self.assertEqual(
			[
				'1', 'NATL 70', '446.000000', '', '0.000000', '', '67.0', '67.0',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_vhf_repeater(self):
		cols = dict()
		cols['name'] = 'Some Repeater'
		cols['medium_name'] = 'Some Rpt'
		cols['short_name'] = 'SOMERPT'
		cols['zone_id'] = ''
		cols['rx_freq'] = '145.310'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = ''
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = ''
		cols['tx_offset'] = '-0.6'
		cols['tx_ctcss'] = '100.0'
		cols['tx_dcs'] = ''
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		result = RadioChannelChirp(cols, None, None).output(3)
		self.assertEqual(
			[
				'2', 'SOMERPT', '145.310000', '-', '0.600000', 'Tone', '100.0', '67.0',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_positive_offset(self):
		cols = dict()
		cols['name'] = 'Some Repeater'
		cols['medium_name'] = 'Some Rpt'
		cols['short_name'] = 'SOMERPT'
		cols['zone_id'] = ''
		cols['rx_freq'] = '442.125'
		cols['rx_ctcss'] = '127.3'
		cols['rx_dcs'] = ''
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = ''
		cols['tx_offset'] = '5.0'
		cols['tx_ctcss'] = '100.0'
		cols['tx_dcs'] = ''
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		result = RadioChannelChirp(cols, None, None).output(4)
		self.assertEqual(
			[
				'3', 'SOMERPT', '442.125000', '+', '5.000000', 'TSQL', '100.0', '127.3',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_dcs_repeater(self):
		cols = dict()
		cols['name'] = 'Dcs Repeater'
		cols['medium_name'] = 'Dcs Rpt'
		cols['short_name'] = 'DCS RPT'
		cols['zone_id'] = ''
		cols['rx_freq'] = '447.075'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = '165'
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = ''
		cols['tx_offset'] = '-5'
		cols['tx_ctcss'] = ''
		cols['tx_dcs'] = '165'
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		result = RadioChannelChirp(cols, None, None).output(6)
		self.assertEqual(
			[
				'5', 'DCS RPT', '447.075000', '-', '5.000000', 'DTCS', '67.0', '67.0',
				'165', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_dcs_invert(self):
		cols = dict()
		cols['name'] = 'Dcs Repeater'
		cols['medium_name'] = 'Dcs Rpt'
		cols['short_name'] = 'DCS RPT'
		cols['zone_id'] = ''
		cols['rx_freq'] = '447.075'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = '23'
		cols['rx_dcs_invert'] = 'true'
		cols['tx_power'] = ''
		cols['tx_offset'] = '-5'
		cols['tx_ctcss'] = ''
		cols['tx_dcs'] = '23'
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		result = RadioChannelChirp(cols, None, None).output(6)
		self.assertEqual(
			[
				'5', 'DCS RPT', '447.075000', '-', '5.000000', 'DTCS', '67.0', '67.0',
				'023', 'RN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)
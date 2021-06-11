from src.ham.radio.chirp.radio_channel_chirp import RadioChannelChirp
from test.base_test_setup import BaseTestSetup


class ChirpTest(BaseTestSetup):
	def setUp(self):
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
		self.cols['name'] = 'National 2m'
		self.cols['medium_name'] = 'Natl 2m'
		self.cols['short_name'] = 'NATL 2M'
		self.cols['rx_freq'] = '146.52'

		channel = RadioChannelChirp(self.cols, None, None)
		result = channel.output(1)
		self.assertEqual(
			[
				'0', 'NATL 2M', '146.520000', '', '0.000000', '', '67.0', '67.0',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_uhf_simplex(self):
		self.cols['name'] = 'National 70cm'
		self.cols['medium_name'] = 'Natl 70c'
		self.cols['short_name'] = 'NATL 70'
		self.cols['rx_freq'] = '446.0'
		channel = RadioChannelChirp(self.cols, None, None)
		result = channel.output(2)
		self.assertEqual(
			[
				'1', 'NATL 70', '446.000000', '', '0.000000', '', '67.0', '67.0',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_vhf_repeater(self):
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '145.310'
		self.cols['tx_offset'] = '-0.6'
		self.cols['tx_ctcss'] = '100.0'
		result = RadioChannelChirp(self.cols, None, None).output(3)
		self.assertEqual(
			[
				'2', 'SOMERPT', '145.310000', '-', '0.600000', 'Tone', '100.0', '67.0',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_positive_offset(self):
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '442.125'
		self.cols['rx_ctcss'] = '127.3'
		self.cols['tx_offset'] = '5.0'
		self.cols['tx_ctcss'] = '100.0'
		result = RadioChannelChirp(self.cols, None, None).output(4)
		self.assertEqual(
			[
				'3', 'SOMERPT', '442.125000', '+', '5.000000', 'TSQL', '100.0', '127.3',
				'023', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_dcs_repeater(self):
		self.cols['name'] = 'Dcs Repeater'
		self.cols['medium_name'] = 'Dcs Rpt'
		self.cols['short_name'] = 'DCS RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['rx_dcs'] = '165'
		self.cols['tx_offset'] = '-5'
		self.cols['tx_dcs'] = '165'
		result = RadioChannelChirp(self.cols, None, None).output(6)
		self.assertEqual(
			[
				'5', 'DCS RPT', '447.075000', '-', '5.000000', 'DTCS', '67.0', '67.0',
				'165', 'NN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)

	def test_dcs_invert(self):
		self.cols['name'] = 'Dcs Repeater'
		self.cols['medium_name'] = 'Dcs Rpt'
		self.cols['short_name'] = 'DCS RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['rx_dcs'] = '23'
		self.cols['rx_dcs_invert'] = 'true'
		self.cols['tx_offset'] = '-5'
		self.cols['tx_dcs'] = '23'
		result = RadioChannelChirp(self.cols, None, None).output(6)
		self.assertEqual(
			[
				'5', 'DCS RPT', '447.075000', '-', '5.000000', 'DTCS', '67.0', '67.0',
				'023', 'RN', 'FM', '5.00', '', '', '', '', '', '',
			], result
		)
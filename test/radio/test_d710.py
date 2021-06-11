from src.ham.radio.d710.radio_channel_d710 import RadioChannelD710
from test.base_test_setup import BaseTestSetup


class D710Test(BaseTestSetup):
	def setUp(self):
		self.radio_channel = RadioChannelD710.create_empty()
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
		expected = """KENWOOD MCP FOR AMATEUR MOBILE TRANSCEIVER
[Export Software]=MCP-2A Version 3.22
[Export File Version]=1
[Type]=K
[Language]=English

// Comments
!!Comments=

// Memory Channels
!!Ch,Rx Freq.,Rx Step,Offset,T/CT/DCS,TO Freq.,CT Freq.,DCS Code,Shift/Split,Rev.,L.Out,Mode,Tx Freq.,Tx Step,M.Name"""
		generated = self.radio_channel.headers()
		self.assertEqual(expected, generated)

	def test_simplex(self):
		self.cols['name'] = 'National 2m'
		self.cols['medium_name'] = 'Natl 2m'
		self.cols['short_name'] = 'NATL 2M'
		self.cols['rx_freq'] = '146.52'
		channel = RadioChannelD710(self.cols, None, None)
		result = channel.output(1)
		self.assertEqual(
			'0000,00146.520000,005.00,00.000000,Off,88.5,88.5,023, ,Off,Off,FM,146.520000,005.00,NATL 2M', result
		)

	def test_uhf_simplex(self):
		self.cols['name'] = 'National 70cm'
		self.cols['medium_name'] = 'Natl 70c'
		self.cols['short_name'] = 'NATL 70'
		self.cols['rx_freq'] = '446.0'
		channel = RadioChannelD710(self.cols, None, None)
		result = channel.output(2)
		self.assertEqual(
			'0001,00446.000000,025.00,00.000000,Off,88.5,88.5,023, ,Off,Off,FM,446.000000,025.00,NATL 70C', result
		)

	def test_vhf_repeater(self):
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '145.310'
		self.cols['tx_offset'] = '-0.6'
		self.cols['tx_ctcss'] = '100.0'
		result = RadioChannelD710(self.cols, None, None).output(3)
		self.assertEqual(
			'0002,00145.310000,005.00,00.600000,T,100.0,88.5,023,-,Off,Off,FM,145.310000,005.00,SOME RPT', result
		)

	def test_positive_offset(self):
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '442.125'
		self.cols['rx_ctcss'] = '127.3'
		self.cols['tx_offset'] = '5.0'
		self.cols['tx_ctcss'] = '100.0'
		result = RadioChannelD710(self.cols, None, None).output(4)

		self.assertEqual(
			'0003,00442.125000,025.00,05.000000,CT,100.0,127.3,023,+,Off,Off,FM,442.125000,025.00,SOME RPT', result
		)

	def test_dcs_repeater(self):
		self.cols['name'] = 'Dcs Repeater'
		self.cols['medium_name'] = 'Dcs Rpt'
		self.cols['short_name'] = 'DCS RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['rx_dcs'] = '165'
		self.cols['tx_offset'] = '-5'
		self.cols['tx_dcs'] = '165'
		result = RadioChannelD710(self.cols, None, None).output(6)
		self.assertEqual(
			'0005,00447.075000,025.00,05.000000,DCS,88.5,88.5,165,-,Off,Off,FM,447.075000,025.00,DCS RPT', result
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
		result = RadioChannelD710(self.cols, None, None).output(6)
		self.assertEqual(
			'0005,00447.075000,025.00,05.000000,DCS,88.5,88.5,047,-,Off,Off,FM,447.075000,025.00,DCS RPT', result
		)















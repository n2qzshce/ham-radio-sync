from src.ham.radio.d710.radio_channel_d710 import RadioChannelD710
from test.base_test_setup import BaseTestSetup


class D710Test(BaseTestSetup):
	def setUp(self):
		self.radio_channel = RadioChannelD710.create_empty()

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
		self.assertEquals(expected, generated)

	def test_simplex(self):
		cols = dict()
		cols['number'] = '1'
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
		channel = RadioChannelD710(cols, None, None)
		result = channel.output(1)
		self.assertEqual(
			'0000,00146.520000,005.00,00.000000,Off,88.5,88.5,023, ,Off,Off,FM,146.520000,005.00,Natl 2m', result
		)
















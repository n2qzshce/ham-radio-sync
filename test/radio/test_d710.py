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
		self.assertEqual(expected, generated)

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

	def test_vhf_simplex(self):
		cols = dict()
		cols['number'] = '2'
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
		channel = RadioChannelD710(cols, None, None)
		result = channel.output(2)
		self.assertEqual(
			'0001,00446.000000,025.00,00.000000,Off,88.5,88.5,023, ,Off,Off,FM,446.000000,025.00,Natl 70c', result
		)

	def test_vhf_repeater(self):
		cols = dict()
		cols['number'] = '3'
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
		result = RadioChannelD710(cols, None, None).output(3)
		self.assertEqual(
			'0002,00145.310000,005.00,00.600000,T,100.0,88.5,023,-,Off,Off,FM,145.310000,005.00,Some Rpt', result
		)

	def test_pos_offset(self):
		cols = dict()
		cols['number'] = '4'
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
		result = RadioChannelD710(cols, None, None).output(4)

		self.assertEqual(
			'0003,00442.125000,025.00,05.000000,CT,100.0,127.3,023,+,Off,Off,FM,442.125000,025.00,Some Rpt', result
		)

	def test_dcs_repeater(self):
		cols = dict()
		cols['number'] = '6'
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
		result = RadioChannelD710(cols, None, None).output(3)
		self.assertEqual(
			'0005,00447.075000,025.00,05.000000,DCS,88.5,88.5,165,-,Off,Off,FM,447.075000,025.00,Dcs Rpt', result
		)

	def test_dcs_invert(self):
		cols = dict()
		cols['number'] = '6'
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
		result = RadioChannelD710(cols, None, None).output(3)
		self.assertEqual(
			'0005,00447.075000,025.00,05.000000,DCS,88.5,88.5,047,-,Off,Off,FM,447.075000,025.00,Dcs Rpt', result
		)















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

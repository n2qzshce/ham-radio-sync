from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types


class RadioChannelD710(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)

		self.number.set_alias(radio_types.D710, 'Ch')
		self.rx_freq.set_alias(radio_types.D710, 'Rx Freq.')
		self.tx_offset.set_alias(radio_types.D710, 'Offset')
		self.tx_ctcss.set_alias(radio_types.D710, 'TO Freq.')
		self.rx_ctcss.set_alias(radio_types.D710, 'CT Freq.')
		self.rx_dcs.set_alias(radio_types.D710, 'DCS Code')
		self.medium_name.set_alias(radio_types.D710, 'M.Name')

	def skip_radio_csv(self):
		return True

	def headers(self):
		result = """KENWOOD MCP FOR AMATEUR MOBILE TRANSCEIVER
[Export Software]=MCP-2A Version 3.22
[Export File Version]=1
[Type]=K
[Language]=English

// Comments
!!Comments=

// Memory Channels
!!"""
		result += f"{self.number.get_alias(radio_types.D710)},"
		result += f"{self.rx_freq.get_alias(radio_types.D710)},"
		result += f"Rx Step,"
		result += f"{self.tx_offset.get_alias(radio_types.D710)},"
		result += f"T/CT/DCS,"
		result += f"{self.tx_ctcss.get_alias(radio_types.D710)},"
		result += f"{self.rx_ctcss.get_alias(radio_types.D710)},"
		result += f"{self.rx_dcs.get_alias(radio_types.D710)},"
		result += f"Shift/Split,"
		result += f"Rev.,"
		result += f"L.Out,"
		result += f"Mode,"
		result += f"Tx Freq.,"
		result += f"Tx Step,"
		result += f"{self.medium_name.get_alias(radio_types.D710)}"
		return result

	def output(self, channel_number):
		output = ""
		output += f""
		return

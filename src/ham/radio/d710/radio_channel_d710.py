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
		rx_step = 5.0
		if self.rx_freq.fmt_val() > 400:
			rx_step = 25.0

		ct_mode = 'Off'
		if self.tx_ctcss.fmt_val() is not None:
			ct_mode = 'T'
			if self.rx_ctcss.fmt_val() is not None:
				ct_mode = 'CT'
		if self.rx_dcs.fmt_val() is not None:
			ct_mode = 'DCS'

		dcs_code = self.rx_dcs.fmt_val(23)
		if self.rx_dcs_invert.fmt_val(False):
			dcs_code = radio_types.dcs_codes_inverses[dcs_code]

		shift_split = ' '
		if self.tx_offset.fmt_val() is not None:
			if self.tx_offset.fmt_val() < 0:
				shift_split = '-'
			else:
				shift_split = '+'

		output = ""
		output += f"{self.number.fmt_val()-1:04d},"
		output += f"{self.rx_freq.fmt_val():012.06f},"
		output += f"{rx_step:06.02f},"
		output += f"{abs(self.tx_offset.fmt_val(0.0)):09.06f},"
		output += f"{ct_mode},"
		output += f"{self.tx_ctcss.fmt_val(88.5)},"
		output += f"{self.rx_ctcss.fmt_val(88.5)},"
		output += f"{dcs_code:03d},"
		output += f"{shift_split},"
		output += f"Off,"
		output += f"Off,"
		output += f"FM,"
		output += f"{self.rx_freq.fmt_val():010.06f},"
		output += f"{rx_step:06.02f},"
		output += f"{self.medium_name.fmt_val():.8s}"
		return output

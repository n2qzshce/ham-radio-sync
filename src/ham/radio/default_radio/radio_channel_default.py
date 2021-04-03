from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types


class RadioChannelDefault(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)

	def skip_radio_csv(self):
		return False

	def headers(self):
		output = list()
		output.append(f"{self.name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.medium_name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.short_name.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.zone_id.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_power.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_freq.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_ctcss.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_dcs.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.rx_dcs_invert.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_offset.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_ctcss.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_dcs.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.tx_dcs_invert.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.digital_timeslot.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.digital_color.get_alias(radio_types.DEFAULT)}")
		output.append(f"{self.digital_contact_id.get_alias(radio_types.DEFAULT)}")
		return output

	def output(self, channel_number):
		output = list()
		output.append(f"{self.name.fmt_val('')}")
		output.append(f"{self.medium_name.fmt_val('')}")
		output.append(f"{self.short_name.fmt_val('')}")
		output.append(f"{self.zone_id.fmt_val('')}")
		output.append(f"{self.tx_power.fmt_val('')}")
		output.append(f"{self.rx_freq.fmt_val('')}")
		output.append(f"{self.rx_ctcss.fmt_val('')}")
		output.append(f"{self.rx_dcs.fmt_val('')}")
		output.append(f"{self.rx_dcs_invert.fmt_val('')}")
		output.append(f"{self.tx_offset.fmt_val('')}")
		output.append(f"{self.tx_ctcss.fmt_val('')}")
		output.append(f"{self.tx_dcs.fmt_val('')}")
		output.append(f"{self.tx_dcs_invert.fmt_val('')}")
		output.append(f"{self.digital_timeslot.fmt_val('')}")
		output.append(f"{self.digital_color.fmt_val('')}")
		output.append(f"{self.digital_contact_id.fmt_val('')}")
		return output

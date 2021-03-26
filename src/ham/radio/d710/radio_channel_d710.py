from src.ham.radio.radio_channel import RadioChannel


class RadioChannelD710(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)

	def skip_radio_csv(self):
		return True

	def headers(self):
		return

	def output(self, channel_number):
		return

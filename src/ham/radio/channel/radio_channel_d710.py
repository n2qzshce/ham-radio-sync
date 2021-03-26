from src.ham.radio.radio_channel import RadioChannel


class RadioChannelD710(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)

	def skip_radio_csv(self, style):
		return True

	def headers(self, style):
		return

	def output(self, style, channel_number):
		return

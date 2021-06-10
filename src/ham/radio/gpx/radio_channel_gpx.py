from src.ham.radio.radio_channel import RadioChannel


class RadioChannelGpx(RadioChannel):
	def __init__(self, cols, digital_contacts, dmr_ids):
		super().__init__(cols, digital_contacts, dmr_ids)

	def skip_radio_csv(self):
		return True

	def headers(self):
		output = list()
		return output

	def output(self, channel_number):
		output = list()
		return output

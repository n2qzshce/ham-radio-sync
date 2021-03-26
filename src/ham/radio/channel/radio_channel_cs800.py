from src.ham.radio.radio_channel import RadioChannel


class RadioChannelCS800(RadioChannel):
	def skip_radio_csv(self, style):
		return False

	def headers(self, style):
		return

	def output(self, style, channel_number):
		return

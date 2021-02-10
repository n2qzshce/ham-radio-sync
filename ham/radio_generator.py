import logging

from ham import radio_channel
from ham.radio_channel import RadioChannel


class RadioGenerator:
	radio_list = []

	def __init__(self, radio_list):
		self.radio_list = radio_list

	def generate_all_declared(self):
		switch = {
			'default': radio_channel.DEFAULT,
			'baofeng': radio_channel.BAOFENG
		}

		for radio in self.radio_list:
			logging.info(f"Generating for radio type `{radio}`")
			self.generate(switch[radio])
		return

	def generate(self, radio_type):
		output = open(f"out/{radio_type}.csv", "w+")
		feed = open("in/input.csv", "r")

		headers = feed.readline()
		file_headers = RadioChannel(headers).output(radio_type, True)
		output.write(file_headers+'\n')

		for feed_line in feed.readlines():
			channel = RadioChannel(feed_line)
			feed_out = channel.output(radio_type, False)
			output.write(feed_out+'\n')
		output.close()
		return

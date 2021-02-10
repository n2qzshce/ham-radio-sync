import logging

from ham import radio_channel
from ham.radio_channel import RadioChannel


class RadioGenerator:
	radio_list = []

	def __init__(self, radio_list):
		self.radio_list = radio_list

	def generate_all_declared(self):
		feed = open("in/input.csv", "r")

		headers = feed.readline().replace('\n', '').split(',')

		radio_files = dict()
		headers_gen = RadioChannel.make_empty()
		for radio in self.radio_list:
			logging.info(f"Generating for radio type `{radio}`")
			output = open(f"out/{radio}.csv", "w+")
			file_headers = headers_gen.headers(radio)
			output.write(file_headers+'\n')
			radio_files[radio] = output

		for line in feed.readlines():
			col_vals = dict()
			cols = line.replace('\n', '').split(",")
			for i in range(0, len(headers) - 1):
				col_vals[headers[i]] = cols[i]

			radio_cls = RadioChannel(col_vals)

			for radio in self.radio_list:
				input_data = radio_cls.output(radio)
				radio_files[radio].write(input_data+'\n')
		return

	def generate(self, radio_type):
		output = open(f"out/{radio_type}.csv", "w+")

		# throw headers away
		file_headers = feed.readline().split(",")
		output.write(file_headers+'\n')

		for feed_line in feed.readlines():
			channel = RadioChannel(feed_line)
			feed_out = channel.output(radio_type)
			output.write(feed_out+'\n')
		output.close()
		return

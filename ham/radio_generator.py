import logging

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
			column_values = dict()
			cols = line.replace('\n', '').split(",")
			for i in range(0, len(headers) - 1):
				column_values[headers[i]] = cols[i]

			radio_channel = RadioChannel(column_values)

			for radio in self.radio_list:
				input_data = radio_channel.output(radio)
				radio_files[radio].write(input_data+'\n')
		return

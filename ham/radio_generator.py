import logging

from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.radio_channel import RadioChannel


class RadioGenerator:
	radio_list = []

	def __init__(self, radio_list):
		self.radio_list = radio_list

	def generate_all_declared(self):
		digital_contacts = self._generate_digital_contact_data()
		dmr_ids = self._generate_dmr_id_data()

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
			column_values = self._line_to_dict(line, headers)

			radio_channel = RadioChannel(column_values, digital_contacts)

			for radio in self.radio_list:
				input_data = radio_channel.output(radio)
				radio_files[radio].write(input_data+'\n')
		return

	def _generate_digital_contact_data(self):
		feed = open("in/digital_contacts.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')
		digital_contacts = dict()
		for line in feed.readlines():
			cols = self._line_to_dict(line, headers)
			contact = DmrContact(cols)
			digital_contacts[contact.radio_id] = contact

		return digital_contacts

	def _generate_dmr_id_data(self):
		feed = open("in/dmr_id.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')
		dmr_ids = dict()
		for line in feed.readlines():
			cols = self._line_to_dict(line, headers)
			id = DmrId(cols)
			dmr_ids[id.number] = id

		return dmr_ids

	def _line_to_dict(self, line, headers):
		column_values = dict()
		cols = line.replace('\n', '').split(",")
		for i in range(0, len(headers) - 1):
			column_values[headers[i]] = cols[i]
		return column_values

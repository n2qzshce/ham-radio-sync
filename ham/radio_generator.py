import logging

from ham import radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.radio_additional import RadioAdditionalData
from ham.radio_channel import RadioChannel
from ham.wizard import Wizard


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
		wizard = Wizard()
		wizard.safe_create_dir('out')

		channel_numbers = dict()
		for radio in self.radio_list:
			wizard.safe_create_dir(f'out/{radio}')
			logging.info(f"Generating for radio type `{radio}`")
			output = open(f"out/{radio}/{radio}_channels.csv", "w+")
			file_headers = headers_gen.headers(radio)
			output.write(file_headers+'\n')
			radio_files[radio] = output
			channel_numbers[radio] = 1

		for line in feed.readlines():
			column_values = self._line_to_dict(line, headers)

			radio_channel = RadioChannel(column_values, digital_contacts, dmr_ids)
			for radio in self.radio_list:
				if not radio_types.supports_dmr(radio) and radio_channel.is_digital():
					continue

				input_data = radio_channel.output(radio, channel_numbers[radio])
				radio_files[radio].write(input_data+'\n')
				channel_numbers[radio] += 1

		additional_data = RadioAdditionalData(dmr_ids, digital_contacts)
		for radio in self.radio_list:
			additional_data.output(radio)
		return

	def _generate_digital_contact_data(self):
		feed = open("in/digital_contacts.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')
		digital_contacts = dict()
		for line in feed.readlines():
			cols = self._line_to_dict(line, headers)
			contact = DmrContact(cols)
			digital_contacts[contact.radio_id.fmt_val()] = contact

		return digital_contacts

	def _generate_dmr_id_data(self):
		feed = open("in/dmr_id.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')
		dmr_ids = dict()
		for line in feed.readlines():
			cols = self._line_to_dict(line, headers)
			dmr_id = DmrId(cols)
			dmr_ids[dmr_id.number.fmt_val()] = dmr_id

		return dmr_ids

	def _line_to_dict(self, line, headers):
		column_values = dict()
		cols = line.replace('\n', '').split(",")
		for i in range(0, len(headers) - 1):
			column_values[headers[i]] = cols[i]
		return column_values

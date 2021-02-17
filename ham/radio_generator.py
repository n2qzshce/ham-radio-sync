import logging

from ham import radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.dmr.dmr_user import DmrUser
from ham.file_util import FileUtil
from ham.radio_additional import RadioAdditionalData
from ham.radio_channel import RadioChannel
from ham.radio_zone import RadioZone


class RadioGenerator:
	radio_list = []

	def __init__(self, radio_list):
		self.radio_list = radio_list

	def generate_all_declared(self):
		digital_contacts = self._generate_digital_contact_data()
		dmr_ids = self._generate_dmr_id_data()
		zones = self._generate_zone_data()
		user = self._generate_user_data()

		feed = open("in/input.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')

		radio_files = dict()
		headers_gen = RadioChannel.create_empty()
		FileUtil.safe_create_dir('out')

		channel_numbers = dict()
		for radio in self.radio_list:
			FileUtil.safe_create_dir(f'out/{radio}')
			logging.info(f"Generating for radio type `{radio}`")
			output = open(f"out/{radio}/{radio}_channels.csv", "w+")
			file_headers = headers_gen.headers(radio)
			output.write(file_headers+'\n')
			radio_files[radio] = output
			channel_numbers[radio] = 1

		for line in feed.readlines():
			column_values = FileUtil.line_to_dict(line, headers)

			radio_channel = RadioChannel(column_values, digital_contacts, dmr_ids)
			if radio_channel.zone_id.fmt_val(None) is not None:
				zones[radio_channel.zone_id.fmt_val()].add_channel(radio_channel)
			for radio in self.radio_list:
				if not radio_types.supports_dmr(radio) and radio_channel.is_digital():
					continue

				input_data = radio_channel.output(radio, channel_numbers[radio])
				radio_files[radio].write(input_data+'\n')
				channel_numbers[radio] += 1

		additional_data = RadioAdditionalData(dmr_ids, digital_contacts, zones, user)
		for radio in self.radio_list:
			additional_data.output(radio)
		return

	def _generate_digital_contact_data(self):
		feed = open("in/digital_contacts.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')
		digital_contacts = dict()
		for line in feed.readlines():
			cols = FileUtil.line_to_dict(line, headers)
			contact = DmrContact(cols)
			digital_contacts[contact.radio_id.fmt_val()] = contact

		return digital_contacts

	def _generate_dmr_id_data(self):
		feed = open("in/dmr_id.csv", "r")
		headers = feed.readline().replace('\n', '').split(',')
		dmr_ids = dict()
		for line in feed.readlines():
			cols = FileUtil.line_to_dict(line, headers)
			dmr_id = DmrId(cols)
			dmr_ids[dmr_id.number.fmt_val()] = dmr_id

		return dmr_ids

	def _generate_zone_data(self):
		feed = open('in/zones.csv', 'r')
		headers = feed.readline().replace('\n', '').split(',')
		zones = dict()
		for line in feed.readlines():
			cols = FileUtil.line_to_dict(line, headers)
			zone = RadioZone(cols)
			zones[zone.number.fmt_val()] = zone

		return zones

	def _generate_user_data(self):
		feed = open('in/user.csv', 'r')
		headers = feed.readline().replace('\n', '').split(',')
		users = dict()
		for line in feed.readlines():
			cols = FileUtil.line_to_dict(line, headers)
			zone = DmrUser(cols)
			users[zone.radio_id.fmt_val()] = zone

		return users

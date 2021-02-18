import logging
import csv

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
		csv_reader = csv.DictReader(feed)

		radio_files = dict()
		radio_channels = dict()
		headers_gen = RadioChannel.create_empty()
		FileUtil.safe_create_dir('out')

		channel_numbers = dict()
		for radio in self.radio_list:
			FileUtil.safe_create_dir(f'out/{radio}')
			logging.info(f"Generating for radio type `{radio}`")

			if RadioChannel.skip_radio_csv(radio):
				logging.info(f"`{radio}` uses special output style. Skipping channels csv")
				continue
			output_file = open(f"out/{radio}/{radio}_channels.csv", "w+")
			output = csv.writer(output_file, delimiter=',', lineterminator='\n')
			file_headers = headers_gen.headers(radio)
			output.writerow(file_headers)
			radio_files[radio] = output
			channel_numbers[radio] = 1

		logging.info("Processing radio channels")
		for line in csv_reader:
			radio_channel = RadioChannel(line, digital_contacts, dmr_ids)
			radio_channels[radio_channel.number] = radio_channel
			if radio_channel.zone_id.fmt_val(None) is not None:
				zones[radio_channel.zone_id.fmt_val()].add_channel(radio_channel)
			for radio in self.radio_list:
				if not radio_types.supports_dmr(radio) and radio_channel.is_digital():
					continue
				if radio not in radio_files.keys():
					continue

				input_data = radio_channel.output(radio, channel_numbers[radio])
				radio_files[radio].writerow(input_data)
				channel_numbers[radio] += 1

		additional_data = RadioAdditionalData(radio_channels, dmr_ids, digital_contacts, zones, user)
		for radio in self.radio_list:
			additional_data.output(radio)
		return

	def _generate_digital_contact_data(self):
		logging.info("Processing digital contacts")
		feed = open("in/digital_contacts.csv", "r")
		csv_feed = csv.DictReader(feed)
		digital_contacts = dict()
		for line in csv_feed:
			contact = DmrContact(line)
			digital_contacts[contact.radio_id.fmt_val()] = contact

		return digital_contacts

	def _generate_dmr_id_data(self):
		logging.info("Processing dmr ids")
		feed = open("in/dmr_id.csv", "r")
		csv_feed = csv.DictReader(feed)
		dmr_ids = dict()
		for line in csv_feed:
			dmr_id = DmrId(line)
			dmr_ids[dmr_id.number.fmt_val()] = dmr_id

		return dmr_ids

	def _generate_zone_data(self):
		logging.info("Processing zones")
		feed = open('in/zones.csv', 'r')
		csv_feed = csv.DictReader(feed)
		zones = dict()
		for line in csv_feed:
			zone = RadioZone(line)
			zones[zone.number.fmt_val()] = zone

		return zones

	def _generate_user_data(self):
		logging.info("Processing dmr IDs. This step can take a while.")
		feed = open('in/user.csv', 'r', encoding='utf-8')
		csv_feed = csv.DictReader(feed)
		users = dict()

		rows_processed = 0
		for line in csv_feed:
			zone = DmrUser(line)
			users[zone.radio_id.fmt_val()] = zone
			rows_processed += 1
			if rows_processed % 1000 == 0:
				logging.info(f"Processed {rows_processed} DMR users")

		return users

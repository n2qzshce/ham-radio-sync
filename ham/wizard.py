import logging
import os

from ham import radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.dmr.dmr_user import DmrUser
from ham.file_util import FileUtil
from ham.radio_channel import RadioChannel
from ham.radio_zone import RadioZone


class Wizard(object):
	_first_cols = ""

	def bootstrap(self, is_forced):
		if os.path.exists('in'):
			logging.warning("INPUT DIRECTORY ALREADY EXISTS!! Input files will be overwritten. Continue? (y/n)[n]")
			if not is_forced:
				prompt = input()
				if prompt != 'y':
					logging.info("Wizard cancelled")
					return
			else:
				logging.warning('FORCED YES')

		self._create_input(is_forced)
		self._create_output()

	def _create_input(self, is_forced):
		FileUtil.safe_create_dir('in')
		create_files = {
			'channels': self._create_channel_file,
			'digital_contacts': self._create_dmr_data,
			'zones': self._create_zone_data,
			'user': self._create_dmr_user_data,
		}

		for key in create_files:
			if not os.path.exists(f"in/{key}.csv") or is_forced:
				create_files[key]()
			else:
				logging.info(f"`{key}.csv` already exists! Skipping.")

	def _create_channel_file(self):
		channel_file = open('in/input.csv', 'w+')
		first_channel = RadioChannel({
			'number': '1',
			'name': 'National 2m',
			'medium_name': 'Natl 2m',
			'short_name': 'NATL 2M',
			'zone_id': '',
			'rx_freq': '146.520',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_power': '',
			'tx_offset': '',
			'tx_ctcss': '',
			'tx_dcs': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact_id': '',
		}, digital_contacts=None, dmr_ids=None)
		second_channel = RadioChannel({
			'number': '2',
			'name': 'Colcon Denver',
			'medium_name': 'ConDenvr',
			'short_name': 'CONDENV',
			'zone_id': '1',
			'rx_freq': '145.310',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_power': '',
			'tx_offset': '-0.600',
			'tx_ctcss': '88.5',
			'tx_dcs': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact_id': '',
		}, digital_contacts=None, dmr_ids=None)
		channel_file.write(RadioChannel.create_empty().headers(radio_types.DEFAULT) + '\n')
		channel_file.write(first_channel.output(radio_types.DEFAULT, 1) + '\n')
		channel_file.write(second_channel.output(radio_types.DEFAULT, 2) + '\n')
		channel_file.close()

	def _create_dmr_data(self):
		dmr_id_file = open('in/dmr_id.csv', 'w+')
		dmr_id = DmrId({
			'number': 1,
			'radio_id': '00000',
			'name': 'DMR',
		})
		dmr_id_file.write(DmrId.create_empty().headers(radio_types.DEFAULT)+'\n')
		dmr_id_file.write(dmr_id.output(radio_types.DEFAULT)+'\n')
		dmr_id_file.close()

		digital_contacts_file = open('in/digital_contacts.csv', 'w+')
		analog_contact = DmrContact({
			'number': 1,
			'digital_id':  dmr_id.radio_id.fmt_val(),
			'name': 'Analog',
			'call_type': 'all',
		})
		group_contact = DmrContact({
			'number': 2,
			'digital_id':  99999,
			'name': 'Some Repeater',
			'call_type': 'group',
		})
		digital_contacts_file.write(DmrContact.create_empty().headers(radio_types.DEFAULT) + '\n')
		digital_contacts_file.write(analog_contact.output(radio_types.DEFAULT) + '\n')
		digital_contacts_file.write(group_contact.output(radio_types.DEFAULT) + '\n')
		digital_contacts_file.close()

	def _create_zone_data(self):
		zone_id_file = open('in/zones.csv', 'w+')
		zone = RadioZone({
			'number': 1,
			'name': 'Zone 1',
		})
		zone_id_file.write(RadioZone.create_empty().headers(radio_types.DEFAULT)+'\n')
		zone_id_file.write(zone.output(radio_types.DEFAULT)+'\n')
		zone_id_file.close()

	def _create_dmr_user_data(self):
		user_file = open('in/user.csv', 'w+')
		dmr_user = DmrUser({
			'RADIO_ID': '00000',
			'CALLSIGN': 'N0CALL',
			'FIRST_NAME': 'Sample',
			'LAST_NAME': 'User',
			'CITY': 'Somewhere',
			'STATE': 'Stateville',
			'COUNTRY': 'Theremany',
			'REMARKS': 'Sample Entry',
		})
		user_file.write(DmrUser.create_empty().headers(radio_types.DEFAULT)+'\n')
		user_file.write(dmr_user.output(radio_types.DEFAULT)+'\n')
		user_file.close()
		return

	def _create_output(self):
		FileUtil.safe_create_dir('out')
		return

	def cleanup(self):
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')

	def readme(self):
		return

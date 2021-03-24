import logging
import os

from src.ham.util import radio_types
from src.ham.dmr.dmr_contact import DmrContact
from src.ham.dmr.dmr_id import DmrId
from src.ham.dmr.dmr_user import DmrUser
from src.ham.util.file_util import FileUtil, RadioWriter
from src.ham.radio.radio_channel import RadioChannel
from src.ham.radio.radio_zone import RadioZone


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
		channel_file = RadioWriter('in/input.csv', '\n')
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
			'name': 'Basic Repeater',
			'medium_name': 'BasicRpt',
			'short_name': 'BASRPTR',
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
		channel_file.writerow(RadioChannel.create_empty().headers(radio_types.DEFAULT))
		channel_file.writerow(first_channel.output(radio_types.DEFAULT, 1))
		channel_file.writerow(second_channel.output(radio_types.DEFAULT, 2))
		channel_file.close()

	def _create_dmr_data(self):
		dmr_id_file = RadioWriter('in/dmr_id.csv', '\n')
		dmr_id = DmrId({
			'number': 1,
			'radio_id': '00000',
			'name': 'DMR',
		})
		dmr_id_file.writerow(DmrId.create_empty().headers(radio_types.DEFAULT))
		dmr_id_file.writerow(dmr_id.output(radio_types.DEFAULT))
		dmr_id_file.close()

		digital_contacts_file = RadioWriter('in/digital_contacts.csv', '\n')
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
		digital_contacts_file.writerow(DmrContact.create_empty().headers(radio_types.DEFAULT))
		digital_contacts_file.writerow(analog_contact.output(radio_types.DEFAULT))
		digital_contacts_file.writerow(group_contact.output(radio_types.DEFAULT))
		digital_contacts_file.close()

	def _create_zone_data(self):
		zone_id_file = RadioWriter('in/zones.csv', '\n')
		zone = RadioZone({
			'number': 1,
			'name': 'Zone 1',
		})
		zone_id_file.writerow(RadioZone.create_empty().headers(radio_types.DEFAULT))
		zone_id_file.writerow(zone.output(radio_types.DEFAULT))
		zone_id_file.close()

	def _create_dmr_user_data(self):
		user_file = RadioWriter('in/user.csv', '\n')
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
		user_file.writerow(DmrUser.create_empty().headers(radio_types.DEFAULT))
		user_file.writerow(dmr_user.output(radio_types.DEFAULT))
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

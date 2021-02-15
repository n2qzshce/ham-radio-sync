import logging
import os
import shutil

from ham import radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.radio_channel import RadioChannel


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

		self.create_input(is_forced)
		self.create_output()

	def create_input(self, is_forced):
		self.safe_create_dir('in')

		if not os.path.exists('in/channels.csv') or is_forced:
			self.create_channel_file()
		else:
			logging.info("`channels.csv` already exists! Skipping")

		if not os.path.exists('in/digital_contacts.csv') or is_forced:
			self.create_dmr_data()
		else:
			logging.info("`groups.csv` already exists! Skipping")
		return

	def create_channel_file(self):
		channel_file = open('in/input.csv', 'w+')
		first_channel = RadioChannel({
			'number': '1',
			'name': 'National 2m',
			'medium_name': 'Natl 2m',
			'short_name': 'NATL 2M',
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
		channel_file.write(RadioChannel.make_empty().headers(radio_types.DEFAULT) + '\n')
		channel_file.write(first_channel.output(radio_types.DEFAULT) + '\n')
		channel_file.write(second_channel.output(radio_types.DEFAULT) + '\n')
		channel_file.close()

	def create_dmr_data(self):
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

	def create_output(self):
		self.safe_create_dir('out')
		return

	def safe_create_dir(self, dir_name):
		if not os.path.exists(dir_name):
			logging.info(f'Creating directory `{dir_name}`')
			os.mkdir(dir_name)
		else:
			logging.info(f'`{dir_name}` exists, skipping.')

	def cleanup(self):
		self.safe_delete_dir('in')
		self.safe_delete_dir('out')

	def safe_delete_dir(self, dir_name):
		try:
			shutil.rmtree(f'{dir_name}')
			logging.info(f'`{dir_name}` directory deleted')
		except OSError:
			logging.info(f'No `{dir_name}` directory to delete')

	def readme(self):
		return

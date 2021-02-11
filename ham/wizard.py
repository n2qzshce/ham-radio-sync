import logging
import os
import shutil

import ham.radio_channel as radio_channel
from ham.radio_channel import Group
from ham.radio_channel import RadioChannel


class Wizard(object):
	_first_cols = ""

	def bootstrap(self, is_forced):
		if os.path.exists('in'):
			logging.warning("INPUT DIRECTORY ALREADY EXISTS!! Continue? (y/n)[n]")
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

		if not os.path.exists('in/groups.csv') or is_forced:
			''
			# self.create_group_file()
		else:
			logging.info("`groups.csv` already exists! Skipping")
		return

	def create_channel_file(self):
		channel_file = open('in/input.csv', 'w+')
		first_channel = RadioChannel({
			'number': '1',
			'name': 'National 2m',
			'short_name': 'NATL 2M',
			'group_id': '1',
			'rx_freq': '146.520',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_offset': '',
			'tx_ctcss': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact': '',
		})
		second_channel = RadioChannel({
			'number': '2',
			'name': 'Colcon Denver',
			'short_name': 'CONDENV',
			'group_id': '1',
			'rx_freq': '145.310',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_offset': '-0.600',
			'tx_ctcss': '88.5',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact': '',
		})
		channel_file.write(RadioChannel.make_empty().headers(radio_channel.DEFAULT)+'\n')
		channel_file.write(first_channel.output(radio_channel.DEFAULT)+'\n')
		channel_file.write(second_channel.output(radio_channel.DEFAULT)+'\n')
		channel_file.close()

	def create_group_file(self):
		group_file = open('in/groups.csv', 'w+')
		first_group = Group('1,My First Group')
		group_file.write(first_group.output(radio_channel.DEFAULT)+'\n')
		group_file.write(first_group.output(radio_channel.DEFAULT)+'\n')
		group_file.close()

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

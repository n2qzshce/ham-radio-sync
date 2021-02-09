import os
import logging
import shutil

import ham.radio_channel as radio_channel
from ham.radio_channel import RadioChannel
from ham.radio_channel import Group


class Wizard(object):
	_first_cols = ""

	def bootstrap(self, is_forced):
		if os.path.exists('in'):
			logging.warning("INPUT DIRECTORY ALREADY EXISTS!! Continue? (y/n)[n]")
			prompt = input()
			if prompt != 'y':
				logging.info("Wizard cancelled")
				return

		self.create_input(is_forced)
		self.create_output()

	def create_input(self, is_forced):
		self.safe_create_dir('in')

		if os.path.exists('in/input.csv'):
			logging.info("`input.csv` already exists! Skipping")
			return

		self.create_channel_file()
		self.create_group_file()
		return

	def create_channel_file(self):
		channel_file = open('in/input.csv', 'w+')
		first_channel = RadioChannel('1,ColCon Denver,CONDEN,1,145.310,,,,-0.600,88.5,,False,,,,12.5')
		channel_file.write(first_channel.output(radio_channel.DEFAULT, True)+'\n')
		channel_file.write(first_channel.output(radio_channel.DEFAULT, False)+'\n')
		channel_file.close()

	def create_group_file(self):
		group_file = open('in/groups.csv', 'w+')
		first_group = Group('1,My First Group')
		group_file.write(first_group.output(radio_channel.DEFAULT, True)+'\n')
		group_file.write(first_group.output(radio_channel.DEFAULT, False)+'\n')
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

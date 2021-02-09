import os
import logging


class Wizard(object):
	logger = logging.getLogger()
	_first_cols = ""

	def bootstrap(self):
		self.create_input()
		self.create_output()

	def create_input(self):
		self.safe_create_dir('in')
		f=open('in/input.csv', 'w+')

		f.close()
		return

	def create_output(self):
		self.safe_create_dir('out')
		return

	def safe_create_dir(self, dir_name):
		if not os.path.exists(dir_name):
			self.logger.info(f'Creating directory `{dir_name}`')
			os.mkdir(dir_name)
		else:
			self.logger.info(f'`{dir_name}` exists, skipping.')

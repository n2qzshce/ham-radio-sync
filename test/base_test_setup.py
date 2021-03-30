import logging
import os
import sys
import unittest


class BaseTestSetup(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		logger = logging.getLogger()
		formatter = logging.Formatter(
			fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename)20s:%(lineno)3s:  %(message)s',
			datefmt="%Y-%m-%d %H:%M:%S")

		handler = logging.StreamHandler(stream=sys.stdout)
		handler.setFormatter(formatter)

		logger.setLevel(logging.INFO)
		if 'CI' in os.environ.keys():
			logger.setLevel(logging.ERROR)
		logger.addHandler(handler)

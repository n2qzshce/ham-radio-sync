import unittest

from src import radio_sync_version


class VersionTest(unittest.TestCase):
	def test_version_present(self):
		self.assertIsNotNone(radio_sync_version.version)

	def test_version_ci(self):
		self.assertNotEqual(radio_sync_version.version, 'DEVELOPMENT')

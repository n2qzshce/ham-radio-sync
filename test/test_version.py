import logging
import os
import unittest

import requests
from semantic_version import Version

from src import radio_sync_version


class VersionTest(unittest.TestCase):
	def test_version_present(self):
		self.assertIsNotNone(radio_sync_version.version)

	def test_version_ci(self):
		self.assertNotEqual(radio_sync_version.version, 'DEVELOPMENT')
		logging.critical(f"Version found: {radio_sync_version.version}")

	def test_version_incremented(self):
		ref = os.environ['GITHUB_REF']
		logging.info(f"Current ref is `{ref}`")
		is_master = ref == 'refs/heads/version-check-fix'
		if is_master:
			logging.info("Skipping version increment check on master.")
		endpoint = "https://api.github.com/repos/n2qzshce/ham-radio-sync/tags"
		result = requests.get(endpoint)
		latest_version = result.json()[0]['name']
		latest = Version.coerce(latest_version)
		current = Version.coerce(radio_sync_version.version)
		self.assertGreater(current, latest, "Version has not been incremented.")
		pass

import logging

import requests
from semantic_version import Version

from src.radio_sync_version import version


def check_version():
	endpoint = "https://api.github.com/repos/n2qzshce/ham-radio-sync/tags"
	try:
		result = requests.get(endpoint)
		latest_version = result.json()[0]['name']
		latest = Version.coerce(latest_version)
		current = Version.coerce(version)
	except Exception as e:
		logging.info("Unable to fetch version info.")
		logging.debug("Unable to fetch version info", e)
		return

	if latest > current:
		logging.warning(f"You are running version `{version}`. Latest is `{latest_version}`")
		logging.info(f"Update at: `https://github.com/n2qzshce/ham-radio-sync/releases`")
	else:
		logging.info("You are on the latest version")
	return

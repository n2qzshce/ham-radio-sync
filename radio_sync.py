import argparse
import asyncio
import logging
import os
import sys

from src.ham.util.file_util import GlobalConstants


def setup_logger():
	os.environ["KIVY_NO_CONSOLELOG"] = "1"
	os.environ["KIVY_NO_FILELOG"] = "1"
	logger = logging.getLogger('radio_sync')
	formatter = GlobalConstants.logging_formatter

	handler = logging.StreamHandler(stream=sys.stdout)
	handler.setFormatter(formatter)

	logger.setLevel(logging.DEBUG)
	logger.addHandler(handler)
	logging.root = logger


async def main():
	from src.ui.app_window import AppWindow

	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--debug',
		action='store_true',
		default=False,
		required=False,
		help='Enable debug logging.',
	)
	arg_values = parser.parse_args()

	if arg_values.debug:
		AppWindow.force_debug = True

	setup_logger()
	app_window = AppWindow()
	try:
		await app_window.async_run()
		logging.info("---APP EXIT SUCCESSFULLY---")
	except Exception as e:
		logging.error("---FATAL ERROR ENCOUNTERED. APP EXITED.---", e)
	return


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

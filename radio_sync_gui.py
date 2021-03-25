import argparse
import asyncio
import logging
import os
import sys


os.environ['KIVY_NO_ARGS'] = '1'


def setup_logger():
	os.environ["KIVY_NO_CONSOLELOG"] = "1"
	os.environ["KIVY_NO_FILELOG"] = "1"
	logger = logging.getLogger('radio_sync')
	formatter = logging.Formatter(
								fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename).6s:%(lineno)3s:  %(message)s',
								datefmt="%Y-%m-%d %H:%M:%S"
	)

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
	await app_window.async_run()

	return


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

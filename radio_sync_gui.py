import asyncio
import logging
import os
import sys

from src.ui.app_window import AppWindow


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
	setup_logger()
	app_window = AppWindow()
	await app_window.async_run()

	return


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())

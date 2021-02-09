import argparse
import logging
import sys

from ham.wizard import Wizard


def main():
	logger = logging.getLogger()
	formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

	handler = logging.StreamHandler(stream=sys.stdout)
	handler.setFormatter(formatter)

	logger.setLevel(logging.INFO)
	logger.addHandler(handler)

	parser = argparse.ArgumentParser(
		prog='Ham Radio channel wizard',
		description='''Convert a ham channel list to various radio formats. All of these options can be chained
					to run multiple steps simultaneously.''')
	parser.add_argument(
		'wizard',
		nargs='?',
		default=False,
	)

	arg_values = parser.parse_args()
	run_wizard = arg_values.wizard is not False

	logger.info("Wizard!")

	if run_wizard:
		wizard = Wizard()
		wizard.bootstrap()

	return


main()

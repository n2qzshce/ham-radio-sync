import argparse
import logging
import sys

from ham.wizard import Wizard


def main():
	logger = logging.getLogger()
	formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)s %(filename).6s:%(lineno)s:  %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

	handler = logging.StreamHandler(stream=sys.stdout)
	handler.setFormatter(formatter)

	logger.setLevel(logging.INFO)
	logger.addHandler(handler)

	parser = argparse.ArgumentParser(
		prog='Ham Radio channel wizard',
		description='''Convert a ham channel list to various radio formats. All of these options can be chained
					to run multiple steps simultaneously.''')

	parser.add_argument(
		'--clean', '-c',
		action='store_true',
		default=False,
		required=False,
		help='Destroys `in` and `out` directories along with all their contents.',
	)

	parser.add_argument(
		'--wizard', '-w',
		action='store_true',
		default=False,
		required=False,
		help='Runs the setup wizard and creates minimum needed files',
	)

	parser.add_argument(
		'--force', '-f',
		action='store_true',
		default=False,
		required=False,
		help="Defaults to 'yes' for all prompts (DANGEROUS)",
	)

	arg_values = parser.parse_args()

	if arg_values.force:
		logging.warning("FORCE HAS BEEN SET. ALL PROMPTS WILL DEFAULT YES. Files may be destroyed.")

	if arg_values.clean:
		wizard = Wizard()
		wizard.cleanup()

	if arg_values.wizard:
		wizard = Wizard()
		wizard.bootstrap(arg_values.force)

	return


main()

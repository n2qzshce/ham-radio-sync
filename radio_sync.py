import argparse
import logging
import sys

from ham.radio_generator import RadioGenerator
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

	parser.add_argument(
		'--radios', '-r',
		choices=['default', 'baofeng'],
		default=[],
		nargs='+',
		help="Name of target radios to create."
	)

	parser.add_argument(
		'--debug',
		action='store_true',
		default=False,
		required=False,
		help='Enable debug logging.',
	)

	arg_values = parser.parse_args()

	op_performed = False

	if arg_values.debug:
		logger.setLevel(logging.DEBUG)

	if arg_values.force:
		logging.warning("FORCE HAS BEEN SET. ALL PROMPTS WILL DEFAULT YES. Files may be destroyed.")

	if arg_values.clean:
		logging.info("Running cleanup.")
		wizard = Wizard()
		wizard.cleanup()
		op_performed = True

	if arg_values.wizard:
		logging.info("Running wizard.")
		wizard = Wizard()
		wizard.bootstrap(arg_values.force)
		op_performed = True

	if len(arg_values.radios) > 0:
		logging.info("Running radio generator.")
		radio_generator = RadioGenerator(arg_values.radios)
		radio_generator.generate_all_declared()
		op_performed = True

	if not op_performed:
		parser.print_usage()

	return


main()

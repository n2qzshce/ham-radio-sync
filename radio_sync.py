import argparse
import logging
import sys

import src.ham.util.radio_types
from src.ham.migration.migration_manager import MigrationManager
from src.ham.radio_generator import RadioGenerator
from src.ham.wizard import Wizard


def main():
	logger = logging.getLogger()
	formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename).6s:%(lineno)3s:  %(message)s', datefmt="%Y-%m-%d %H:%M:%S")

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
		'--migrate', '-m',
		action='store_true',
		default=False,
		required=False,
		help='Safely updates your input files to the latest version.',
	)

	parser.add_argument(
		'--migrate_cleanup',
		action='store_true',
		default=False,
		required=False,
		help='Removes .bak files created during migration process.',
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
		choices=src.ham.util.radio_types.radio_choices(),
		default=[],
		nargs='+',
		help=f"""Name of target radios to create.
		{src.ham.util.radio_types.DEFAULT} -- This is a replication of the input, primarily used for validation/testing.
		{src.ham.util.radio_types.BAOFENG} -- Baofeng UV-5R and F8-HP via CHiRP
		{src.ham.util.radio_types.CS800} -- Connect Systems CS800D
		{src.ham.util.radio_types.D710} -- Kenwood TM-D710 Series
		{src.ham.util.radio_types.D878} -- Anytone D878 or D868
		{src.ham.util.radio_types.FTM400} -- Yaesu FTM-400 via RT Systems app 
		"""
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

	if arg_values.migrate:
		logging.info("Running migration")
		migrations = MigrationManager()
		migrations.migrate()
		op_performed = True

	if arg_values.migrate_cleanup:
		logging.info("Running migration")
		migrations = MigrationManager()
		migrations.remove_backups()
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

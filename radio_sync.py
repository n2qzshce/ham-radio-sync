import argparse
import logging
import sys

import src.ham.util.radio_types
import src.radio_sync_version_check
from src import radio_sync_version
from src.ham.migration.migration_manager import MigrationManager
from src.ham.radio_generator import RadioGenerator
from src.ham.util.path_manager import PathManager
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
					to run multiple steps in order.''')

	parser.add_argument(
		'--clean', '-c',
		action='store_true',
		default=False,
		required=False,
		help='Destroys input and output directories along with all their contents.',
	)

	parser.add_argument(
		'--migrate-check',
		action='store_true',
		default=False,
		required=False,
		help='Checks for outdated columns.',
	)

	parser.add_argument(
		'--migrate', '-m',
		action='store_true',
		default=False,
		required=False,
		help='Safely updates your input files to the latest version.',
	)

	parser.add_argument(
		'--migrate-cleanup',
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
		help=f"""Target radios to create."""
	)

	parser.add_argument(
		'--version',
		action='store_true',
		default=False,
		required=False,
		help='Display app version.',
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
		logging.debug("Logging level set to debug.")

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

		if PathManager.input_path_exists(''):
			logging.info(f"Your input directory is located at: `{PathManager.get_input_path()}`")
			logging.warning("INPUT DIRECTORY ALREADY EXISTS!! Input files will be overwritten. Continue? (y/n)[n]")
			prompt = input()
			if prompt != 'y':
				logging.info("Wizard cancelled")
				return
			else:
				logging.warning('Input directory will be overwritten')
		wizard.bootstrap(arg_values.force)
		op_performed = True

	if arg_values.migrate_check:
		logging.info("Running migration check")
		migrations = MigrationManager()
		migrations.log_check_migrations()
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

	if arg_values.version:
		logging.info(f"App version {src.radio_sync_version.version}")
		src.radio_sync_version_check.check_version()
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

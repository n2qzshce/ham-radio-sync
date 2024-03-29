import base64
import logging
import threading
import webbrowser

import src.radio_sync_version_check
from src.ham.migration.migration_manager import MigrationManager
from src.ham.radio.radio_importer import RadioImporter
from src.ham.radio_generator import RadioGenerator
from src.ham.util import radio_types
from src.ham.util.file_util import GlobalConstants
from src.ham.util.path_manager import PathManager
from src.ham.wizard import Wizard


class AsyncWrapper:
	dangerous_operations_snippet = '''Dangerous Operations:
				'Create Radio Plugs' can be run repeatedly without risk, this is not true for dangerous operations.
				Dangerous operations tamper with the `input` folder, and may delete or alter your input csv files.'''

	def __init__(self):
		self.buttons = []
		self.dangerous_buttons = []
		self._wizard = Wizard()
		self._migrations = MigrationManager()
		self.dangerous_ops_toggle = None
		self._buttons_disabled = False
		self.radio_buttons = dict()
		self.debug_toggle = None
		self._file_logger = None
		self._radio_importer = RadioImporter()
		return

	def arm_dangerous(self, *args):
		if self.dangerous_ops_toggle.state == 'down':
			logging.warning(
							f'''Dangerous operations enabled.
		This may destroy/delete input files.
		Have you backed up your input folder contents?
		{self.dangerous_operations_snippet}
		See `Getting Started` for more info.'''
			)
		else:
			logging.info('Dangerous operations disabled')
		self._refresh_buttons()

	def _set_buttons_disabled(self, bool_val):
		self._buttons_disabled = bool_val
		self._refresh_buttons()
		return

	def _refresh_buttons(self):
		for button in self.buttons:
			button.disabled = self._buttons_disabled

		for button in self.dangerous_buttons:
			button.disabled = self._buttons_disabled or not self.dangerous_ops_toggle.state == 'down'

	def _submit_blocking_task(self, task_func):
		logging.debug('Submitting blocking task')
		threading.Thread(target=self._async_blocking_task, args=(task_func,), daemon=True).start()
		logging.debug('Submitted blocking task')
		return

	def _async_blocking_task(self, task_func):
		logging.info('---Starting task---')
		self._set_buttons_disabled(True)
		try:
			task_func()
		except Exception as e:
			logging.error(f'''Fatal error while processing task. PLEASE send this to the project owners.
				Contact info is available under `Help / Getting Started`''', exc_info=True)
		logging.info('---Task finished---')
		self.dangerous_ops_toggle.state = 'normal'
		self._set_buttons_disabled(False)

	def radio_generator(self, event):
		self._submit_blocking_task(self._radio_generator_async)

	def _radio_generator_async(self):
		gen_list = []

		for radio in self.radio_buttons.keys():
			if self.radio_buttons[radio].active:
				gen_list.append(radio)

		radio_generator = RadioGenerator(gen_list)
		radio_generator.generate_all_declared()

	def display_start_info(self, event):
		self._submit_blocking_task(self._display_start_info_async)

	def _display_start_info_async(self):
		RadioGenerator.info(self.dangerous_operations_snippet)

	def wizard_cleanup(self, event):
		self._submit_blocking_task(self._wizard_cleanup_async)

	def _wizard_cleanup_async(self):
		self._wizard.cleanup()

	def wizard_bootstrap(self, button):
		self._submit_blocking_task(self._wizard_bootstrap_async)

	def _wizard_bootstrap_async(self):
		self._wizard.bootstrap()

	def check_migrations(self, event):
		self._submit_blocking_task(self._check_migrations_async)

	def _check_migrations_async(self):
		self._migrations.log_check_migrations()

	def migrations(self, event):
		self._submit_blocking_task(self._migrations_async)

	def _migrations_async(self):
		self._migrations.migrate()

	def migration_backups(self, event):
		self._submit_blocking_task(self._migration_backups_async)

	def _migration_backups_async(self):
		self._migrations.remove_backups()

	def check_version(self, event):
		self._submit_blocking_task(self._check_version_async)

	def _check_version_async(self):
		src.radio_sync_version_check.check_version()
		
	def import_file(self):
		self._submit_blocking_task(self._import_file_async)
		
	def _import_file_async(self):
		path = PathManager.get_import_path()

		channels = []
		try:
			channels = self._radio_importer.run_import(radio_types.CHIRP, path)
		except Exception as e:
			logging.error(f'Failed to import {path}. Exception: {e.__class__}')

		if len(channels) > 0:
			self._radio_importer.channels_to_file(channels)

	def toggle_file_log(self, value):
		if value.state == 'down':
			logger = logging.getLogger('radio_sync')
			handler = logging.FileHandler('ham-radio-sync.log')
			handler.setFormatter(GlobalConstants.logging_formatter)
			logger.addHandler(handler)
			self._file_logger = handler
		else:
			logger = logging.getLogger('radio_sync')
			handler = self._file_logger
			logger.removeHandler(handler)

	def log_level(self, value):
		if value.state == 'down':
			logging.root.setLevel(logging.DEBUG)
			logging.debug('Debug logging enabled.')
		else:
			logging.root.setLevel(logging.INFO)
			logging.debug('Debug logging disabled')
			logging.info('Debug logging disabled')

	def contact_info(self, value):
		email_enc = 'c3cuYXUrZ2l0aHViQHBtLm1l'
		decode_bytes = base64.b64decode(email_enc)
		email_dec = str(decode_bytes, 'utf-8')
		logging.info(f'''
For feature requests, you can contact the repository owners here: 
Email: {email_dec}
A draft email will now attempt to open...''')
		webbrowser.open(f'mailto:{email_dec}?subject=radio_sync%20sFeature%20srequest', new=2)

	def compatible_radios(self, value):
		radio_list = f''''''
		for radio in radio_types.compatible_radios.keys():
			radio_list += f'''\n\t\t{radio_types.pretty_name(radio):30s} | {radio_types.compatible_radios[radio]}'''

		logging.info(f'''These are the known radios that are compatible, as well as what program the output file is
			designed to use. If this list is inaccurate, please contact the author!
			{radio_list}
			''')

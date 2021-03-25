import asyncio
import logging
import threading

from src.ham.migration.migration_manager import MigrationManager
from src.ham.radio_generator import RadioGenerator
from src.ham.util import radio_types
from src.ham.wizard import Wizard


class AsyncWrapper:
	def __init__(self):
		self.buttons = []
		self.dangerous_buttons = []
		self._wizard = Wizard()
		self._migrations = MigrationManager()
		self._radio_generator = RadioGenerator([radio_types.DEFAULT])
		self.dangerous_ops_toggle = None
		self._buttons_disabled = False
		self.radio_buttons = dict()
		return

	def arm_dangerous(self, *args):
		if self.dangerous_ops_toggle.state == 'down':
			logging.warning("Dangerous operations enabled. Have you backed up your input CSVs?")
		else:
			logging.info("Dangerous operations disabled")
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
		logging.debug("Submitting blocking task")
		# task = asyncio.create_task(self._async_blocking_task(task_func))
		threading.Thread(target=task_func, daemon=True).start()
		# task.add_done_callback(self._check_exceptions)
		logging.debug("Submitted blocking task")
		return

	def _check_exceptions(self, task: asyncio.Task):
		try:
			task.result()
		except Exception as e:
			logging.error(f"Fatal error while processing task. PLEASE send this to the project owners.", exc_info=True)

	def _async_blocking_task(self, task_func):
		logging.info("---Starting task---")
		self._set_buttons_disabled(True)
		try:
			task_func()
		except Exception as e:
			logging.error(f"Fatal error while processing task. PLEASE send this to the project owners.", exc_info=True)
		logging.info("---Task finished---")
		self.dangerous_ops_toggle.active = False
		self._set_buttons_disabled(False)

	def display_about_info(self, event):
		self._submit_blocking_task(self._display_about_info_async)

	def _display_about_info_async(self):
		self._radio_generator.info()

	def wizard_cleanup(self, event):
		self._submit_blocking_task(self._wizard_cleanup_async)

	def _wizard_cleanup_async(self):
		self._wizard.cleanup()

	def wizard_bootstrap(self, button):
		self._submit_blocking_task(self._wizard_bootstrap_async)

	def _wizard_bootstrap_async(self):
		self._wizard.bootstrap(True)

	def migrations(self, event):
		self._submit_blocking_task(self._migrations_async)

	def _migrations_async(self):
		self._migrations.migrate()

	def migration_backups(self, event):
		self._submit_blocking_task(self._migration_backups_async)

	def _migration_backups_async(self):
		self._migrations.remove_backups()

	def radio_generator(self, event):
		self._submit_blocking_task(self._radio_generator_async)

	def _radio_generator_async(self):
		gen_list = []

		for radio in self.radio_buttons.keys():
			if self.radio_buttons[radio].active:
				gen_list.append(radio)

		self._radio_generator.radio_list = gen_list
		self._radio_generator.generate_all_declared()

	def log_level(self, _, value):
		if value:
			logging.root.setLevel(logging.DEBUG)
			logging.debug("Debug logging enabled.")
		else:
			logging.root.setLevel(logging.INFO)
			logging.debug("Debug logging disabled")
			logging.info("Debug logging disabled")

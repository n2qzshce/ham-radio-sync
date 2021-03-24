import asyncio
import logging
import threading
from abc import ABC
from typing import TextIO

from PySimpleGUI import PySimpleGUI, TIMEOUT_EVENT

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
		self.dangerous_ops_checkbox = None
		self._buttons_disabled = False
		self.radio_buttons = dict()
		self.debug_toggle = None
		return

	def arm_dangerous(self, _):
		if self.dangerous_ops_checkbox.get():
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
			button.update(disabled=self._buttons_disabled)

		for button in self.dangerous_buttons:
			button.update(disabled=self._buttons_disabled or not self.dangerous_ops_checkbox.get())

	def _submit_blocking_task(self, task_func):
		logging.info("---Starting task---")
		self._set_buttons_disabled(True)
		try:
			task_func()
		except Exception as e:
			logging.error(f"Fatal error while processing task. PLEASE send this to the project owners.", exc_info=True)
		logging.info("---Task finished---")
		self.dangerous_ops_checkbox.Update(value=False)
		self._set_buttons_disabled(False)

	def display_about_info(self, event):
		self._submit_blocking_task(self._display_about_info_async)

	def _display_about_info_async(self):
		self._radio_generator.info()

	def wizard_cleanup(self, event):
		self._submit_blocking_task(self._wizard_cleanup_async)

	def _wizard_cleanup_async(self):
		self._wizard.cleanup()

	def wizard_bootstrap(self, event):
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
			if self.radio_buttons[radio].get():
				gen_list.append(radio)

		self._radio_generator.radio_list = gen_list
		self._radio_generator.generate_all_declared()

	def log_level(self, event):
		value = self.debug_toggle.get()

		if value:
			logging.root.setLevel(logging.DEBUG)
			logging.debug("Debug logging enabled.")
		else:
			logging.root.setLevel(logging.INFO)
			logging.debug("Debug logging disabled")
			logging.info("Debug logging disabled")


class AppWindow:
	def __init__(self):
		self._event_handler = EventHandler()
		self._async_wrapper = AsyncWrapper()
		PySimpleGUI.theme('DarkGrey6')

		button_pool_rows = []
		layout = []
		menu = [
			['File', ['Exit']],
			['Help', ['About...']]
		]
		layout.append([PySimpleGUI.Menu(menu_definition=menu)])
		self._event_handler.add_hook('About...', self._async_wrapper.display_about_info)

		buttons = []
		dangerous_buttons = []

		radio_header = PySimpleGUI.Text(text='Radio List')
		button_pool_rows.append([radio_header])

		radio_checkboxes = dict()
		radios = [
			radio_types.DEFAULT,
			radio_types.FTM400,
			radio_types.D878,
			radio_types.CS800,
			radio_types.BAOFENG,
		]

		radio_button_list = []
		for radio in radios:
			radio_checkbox = PySimpleGUI.Checkbox(
				text=radio_types.pretty_name(radio),
				default=radio == radio_types.DEFAULT,
				tooltip=f"Generate codeplug files for {radio_types.pretty_name(radio)}",
			)
			radio_checkboxes[radio] = radio_checkbox
			radio_button_list.append([radio_checkbox])

		self._async_wrapper.radio_buttons = radio_checkboxes

		button_pool_rows += radio_button_list

		horizontal_divider = PySimpleGUI.HorizontalSeparator(color='black', pad=(0, (0, 50)))
		button_pool_rows.append([horizontal_divider])

		arm_dangerous_checkbox = PySimpleGUI.Checkbox(
			text='Enable Dangerous Operations',
			default=False,
			enable_events=True,
			key='Enable Dangerous Operations',
			tooltip='Allows destructive operations to be run.'
		)
		self._event_handler.add_hook(arm_dangerous_checkbox.Key, self._async_wrapper.arm_dangerous)
		button_pool_rows.append([arm_dangerous_checkbox])
		self._async_wrapper.dangerous_ops_checkbox = arm_dangerous_checkbox

		cleanup_button = PySimpleGUI.Button(
			button_text='Run Cleanup',
			size=(20, 2), enable_events=True,
			disabled=True,
			tooltip='Removes existing "in" and "out" folders.'
		)
		self._event_handler.add_hook(cleanup_button.get_text(), self._async_wrapper.wizard_cleanup)
		button_pool_rows.append([cleanup_button])
		buttons.append(cleanup_button)
		dangerous_buttons.append(cleanup_button)

		wizard_button = PySimpleGUI.Button(
			button_text='Run Setup Wizard',
			size=(20, 2),
			enable_events=True,
			disabled=True,
			tooltip='Generates "in" and "out" folders, as well as some sample data.'
		)
		self._event_handler.add_hook(wizard_button.get_text(), self._async_wrapper.wizard_bootstrap)
		button_pool_rows.append([wizard_button])
		buttons.append(wizard_button)
		dangerous_buttons.append(wizard_button)

		migrations_button = PySimpleGUI.Button(
			button_text='Migrate CSV to Latest',
			size=(20, 2),
			enable_events=True,
			disabled=True,
			tooltip='Adds and renames columns and files for the latest input version.'
		)
		self._event_handler.add_hook(migrations_button.get_text(), self._async_wrapper.migrations)
		button_pool_rows.append([migrations_button])
		buttons.append(migrations_button)
		dangerous_buttons.append(migrations_button)

		migration_backups_button = PySimpleGUI.Button(
			button_text='Remove Migration Backups',
			size=(20, 2),
			enable_events=True,
			disabled=True,
			tooltip='Removes .bak file extensions from the "in" directory.'
		)
		self._event_handler.add_hook(migration_backups_button.get_text(), self._async_wrapper.migration_backups)
		button_pool_rows.append([migration_backups_button])
		buttons.append(migration_backups_button)
		dangerous_buttons.append(migration_backups_button)

		generate_button = PySimpleGUI.Button(
			button_text='Create Radio Plugs',
			size=(20, 2),
			enable_events=True,
			tooltip='Generates CSVs to import into your radio program.'
		)
		self._event_handler.add_hook(generate_button.get_text(), self._async_wrapper.radio_generator)
		button_pool_rows.append([generate_button])
		buttons.append(generate_button)

		debug_logging_checkbox = PySimpleGUI.Checkbox(
			text='Enable Debug Logging',
			key='Enable Debug Logging',
			default=False,
			enable_events=True,
			tooltip="More logging. You generally don't need this."
		)
		self._event_handler.add_hook(debug_logging_checkbox.Key, self._async_wrapper.log_level)
		self._async_wrapper.debug_toggle = debug_logging_checkbox
		button_pool_rows.append([debug_logging_checkbox])

		text_box = PySimpleGUI.Multiline(default_text='', disabled=True, size=(150, 25), font=('Courier', 10))
		self.text_log = text_box

		logger = logging.getLogger('radio_sync')
		formatter = logging.Formatter(
			fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename).6s:%(lineno)3s:  %(message)s',
			datefmt="%Y-%m-%d %H:%M:%S"
		)
		text_box_logger = TextBoxHandler(self.text_log)
		handler = logging.StreamHandler(stream=text_box_logger)
		handler.setFormatter(formatter)
		logger.setLevel(logging.INFO)
		logger.addHandler(handler)

		button_pool = PySimpleGUI.Column(layout=button_pool_rows, expand_y=True, vertical_alignment='center')
		layout.append([button_pool, text_box])

		self._async_wrapper.buttons = buttons
		self._async_wrapper.dangerous_buttons = dangerous_buttons
		self._layout = layout
		self.window = None

	_cycle_time = 0.001

	async def async_run(self):
		self.window = PySimpleGUI.Window(title='Ham Radio Sync', layout=self._layout, finalize=True)
		logging.info(f"Welcome to the ham radio sync app.")

		while True:
			event, values = self.window.read()
			if event == PySimpleGUI.WIN_CLOSED or event == 'Exit':  # if user closes window or clicks cancel
				break
			else:
				logging.debug(event)

			threading.Thread(target=self._event_handler.run_hook, args=(event, values), daemon=True).start()

		self.window.close()
		return

	async def window_read(self):
		return self.window.read(timeout=self._cycle_time * 1000)

	async def window_refresh(self, window):
		while True:
			await asyncio.sleep(0.01)
			window.refresh()


class EventHandler:
	def __init__(self):
		self._events = dict()

	def add_hook(self, hook_name, func):
		self._events[hook_name] = func

	def run_hook(self, hook_name, event_data):
		if hook_name == TIMEOUT_EVENT:
			return
		logging.debug(f"Running hook `{hook_name}`")
		if hook_name in self._events.keys():
			self._events[hook_name](event_data)


class TextBoxHandler(TextIO, ABC):
	def __init__(self, text_log):
		self._text_log = text_log
		self.lock = None

	def write(self, record):
		self._text_log.print(record, end='')
		return

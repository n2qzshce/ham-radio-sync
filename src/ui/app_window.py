import asyncio
import logging
from abc import ABC
from typing import TextIO

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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
		return

	def arm_dangerous(self, *args):
		if self.dangerous_ops_checkbox.active:
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
			button.disabled = self._buttons_disabled or not self.dangerous_ops_checkbox.active

	def _submit_blocking_task(self, task_func):
		task = asyncio.create_task(self._async_blocking_task(task_func))
		task.add_done_callback(self._check_exceptions)
		return

	def _check_exceptions(self, task: asyncio.Task):
		try:
			task.result()
		except Exception as e:
			logging.error(f"Fatal error while processing task. PLEASE send this to the project owners.", exc_info=True)

	async def _async_blocking_task(self, task_func):
		logging.info("---Starting task---")
		self._set_buttons_disabled(True)
		await task_func()
		logging.info("---Task finished---")
		self.dangerous_ops_checkbox.active = False
		self._set_buttons_disabled(False)

	def display_about_info(self, event):
		self._submit_blocking_task(self._display_about_info_async)

	async def _display_about_info_async(self):
		self._radio_generator.info()

	def wizard_cleanup(self, event):
		self._submit_blocking_task(self._wizard_cleanup_async)

	async def _wizard_cleanup_async(self):
		self._wizard.cleanup()

	def wizard_bootstrap(self, button):
		self._submit_blocking_task(self._wizard_bootstrap_async)

	async def _wizard_bootstrap_async(self):
		self._wizard.bootstrap(True)

	def migrations(self, event):
		self._submit_blocking_task(self._migrations_async)

	async def _migrations_async(self):
		self._migrations.migrate()

	def migration_backups(self, event):
		self._submit_blocking_task(self._migration_backups_async)

	async def _migration_backups_async(self):
		self._migrations.remove_backups()

	def radio_generator(self, event):
		self._submit_blocking_task(self._radio_generator_async)

	async def _radio_generator_async(self):
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


class AppWindow(App):
	text_log = None
	_async_wrapper = None

	def build(self):
		# debug logging
		# cleanup
		# wizard bootstrap
		# generate all declared
		# help page
		# Window.clearcolor = (0.15, 0.15, 0.15, 1)
		buttons = []
		dangerous_buttons = []
		self._async_wrapper = AsyncWrapper()

		layout = BoxLayout(orientation='horizontal')

		button_pool = BoxLayout(spacing=10, orientation='vertical', size_hint=(0.2, 1), padding=[15, 15, 15, 15])
		button_pool.size_hint_min_x = 200
		button_pool.size_hint_max_x = 250

		radio_select_buttons = dict()
		radios = [
			radio_types.DEFAULT,
			radio_types.D878,
			radio_types.BAOFENG,
			radio_types.CS800,
			radio_types.FTM400,
		]

		radio_header = Label(text='Radio List', size_hint=(0.8, 0.125), font_size=15, bold=True, halign='left')
		radio_header.text_size = [150, None]
		radio_header.size_hint_min_x = 150

		button_pool.add_widget(radio_header)
		for radio in radios:
			radio_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

			radio_label = Label(text=radio_types.pretty_name(radio), size_hint=(0.8, 1), font_size=11, halign='left')
			radio_label.size_hint_min_x = 150
			radio_checkbox = CheckBox(size_hint=(0.2, 1))
			radio_checkbox.active = radio == radio_types.DEFAULT

			radio_layout.add_widget(radio_label)
			radio_layout.add_widget(radio_checkbox)

			radio_select_buttons[radio] = radio_checkbox
			button_pool.add_widget(radio_layout)

			radio_label.text_size = [150, None]

		self._async_wrapper.radio_buttons = radio_select_buttons
		empty_buffer = BoxLayout(orientation='horizontal', size_hint=(1, 0.25))
		button_pool.add_widget(empty_buffer)

		arm_dangerous_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.125))
		arm_dangerous_label = Label(text='Enable Dangerous Operations', size_hint=(0.8, 1), font_size=11)
		arm_dangerous_checkbox = CheckBox(size_hint=(0.2, 1))
		arm_dangerous_layout.add_widget(arm_dangerous_label)
		arm_dangerous_layout.add_widget(arm_dangerous_checkbox)
		button_pool.add_widget(arm_dangerous_layout)

		cleanup_button = Button(text='Run Cleanup', size_hint=(1, 0.125), on_press=self._async_wrapper.wizard_cleanup)
		button_pool.add_widget(cleanup_button)
		buttons.append(cleanup_button)
		dangerous_buttons.append(cleanup_button)

		wizard = Button(text='Run Setup Wizard', size_hint=(1, 0.125), on_press=self._async_wrapper.wizard_bootstrap)
		button_pool.add_widget(wizard)
		buttons.append(wizard)
		dangerous_buttons.append(wizard)

		migrate = Button(text='Migrate CSV to Latest', size_hint=(1, 0.125), on_press=self._async_wrapper.migrations)
		button_pool.add_widget(migrate)
		buttons.append(migrate)
		dangerous_buttons.append(migrate)

		migrate_del_backups = Button(text='Remove Migration Backups', size_hint=(1, 0.125), on_press=self._async_wrapper.migration_backups)
		button_pool.add_widget(migrate_del_backups)
		buttons.append(migrate_del_backups)
		dangerous_buttons.append(migrate_del_backups)

		generate = Button(text='Create radio plugs', size_hint=(1, 0.125), on_press=self._async_wrapper.radio_generator)
		button_pool.add_widget(generate)
		buttons.append(generate)

		help_btn = Button(text='Help', size_hint=(1, 0.125), on_press=self._async_wrapper.display_about_info)
		button_pool.add_widget(help_btn)
		buttons.append(help_btn)

		log_output = AnchorLayout(size_hint=(0.8, 1))

		text_log = TextInput(font_name='RobotoMono-Regular', text='', size_hint=(1, 1), readonly=True, font_size=11)
		log_output.add_widget(text_log)

		layout.add_widget(button_pool)
		layout.add_widget(log_output)

		self.text_log = text_log

		logger = logging.getLogger('radio_sync')
		formatter = logging.Formatter(
			fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename).6s:%(lineno)3s:  %(message)s',
			datefmt="%Y-%m-%d %H:%M:%S"
		)

		text_box_logger = TextBoxHandler(self.text_log)
		handler = logging.StreamHandler(stream=text_box_logger)
		handler.setFormatter(formatter)

		debugger_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

		debugger_label = Label(text='Verbose logging', size_hint=(0.8, 1), font_size=11, halign='left')
		debugger_checkbox = CheckBox(size_hint=(0.2, 1))
		debugger_checkbox.bind(active=self._async_wrapper.log_level)
		debugger_checkbox.active = False

		debugger_layout.add_widget(debugger_label)
		debugger_layout.add_widget(debugger_checkbox)
		button_pool.add_widget(debugger_layout)

		logger.setLevel(logging.INFO)
		logger.addHandler(handler)
		Window.size = (1200, 500)
		logging.info("Welcome to the ham radio sync app.")
		self._async_wrapper.dangerous_ops_checkbox = arm_dangerous_checkbox
		self._async_wrapper.buttons = buttons
		self._async_wrapper.dangerous_buttons = dangerous_buttons
		arm_dangerous_checkbox.bind(active=self._async_wrapper.arm_dangerous)

		self._async_wrapper.dangerous_ops_checkbox = arm_dangerous_checkbox
		self._async_wrapper.arm_dangerous(None)
		return layout


class TextBoxHandler(TextIO, ABC):
	def __init__(self, text_log):
		self._text_log = text_log
		self.lock = None

	def write(self, record):
		self._text_log.text += record
		return


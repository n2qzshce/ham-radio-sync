import logging
import os
import sys
from abc import ABC
from typing import TextIO

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from src.ham.util import radio_types
from src.ui.async_wrapper import AsyncWrapper

kv = """
BoxLayout:
	orientation: "vertical"
	ActionBar:
		ActionView:
			ActionPrevious:
				title: 'Ham Radio Sync'
				with_previous: False
				enabled: False
				app_icon: 'radio_sync.ico'
			ActionButton:
				id: create_radio_plugs
				text: "Create Radio Plugs"
			ActionToggleButton:
				id: enable_dangerous
				text: "Enable Dangerous Operations"
			ActionSeparator:
				important: True
			ActionGroup:
				text: "File"
				mode: "spinner"
				ActionButton:
					id: exit_button
					text: "Exit"
			ActionGroup:
				text: "Dangerous Operations"
				mode: "spinner"
				id: dangerous_operations
				dropdown_width: 225
				ActionButton:
					id: dangerous_operations.cleanup
					text: "Cleanup"
				ActionButton:
					id: dangerous_operations.wizard
					text: "Wizard"
				ActionButton:
					id: dangerous_operations.migrate
					text: "Migrate to latest format"
				ActionButton:
					id: dangerous_operations.delete_migrate
					text: "Remove migration backups"
			ActionGroup:
				text: "Help"
				mode: "spinner"
				dropdown_width: 150
				ActionToggleButton:
					id: debug_toggle
					text: "Debug logging"
				ActionButton:
					id: about
					text: "About..."
	BoxLayout:
		orientation: "horizontal"
		StackLayout:
			id: button_pool
			spacing: 10
			size_hint: (0.2, 1)
			padding: [15, 15, 15, 15]
			size_hint_min_x: 200
			size_hint_max_x: 250
			Label:
				id: radio_header
				text: "Radios"
				size_hint: (1.0, 0.1)
				font_size: 15
				bold: True
			BoxLayout:
				id: radio_labels
				orientation: "vertical"
				spacing: 10
				size_hint: (1, 0.4)
			BoxLayout:
				id: buffer
				orientation: "vertical"
				size_hint: (1, 0.2)
		AnchorLayout:
			size_hint: (0.8, 1)
			TextInput:
				id: log_output
				font_name: 'RobotoMono-Regular'
				text: ''
				size_hint: (1, 1)
				readonly: True
				font_size: 11
"""


class AppWindow(App):
	text_log = None
	_async_wrapper = None
	force_debug = False

	def build(self):

		self.icon = './radio_sync.ico'
		if hasattr(sys, '_MEIPASS'):
			logging.info("Has _MEIPASS")
			resource_add_path(os.path.join(sys._MEIPASS))
			self.icon = os.path.join(sys._MEIPASS, 'radio_sync.ico')

		self._async_wrapper = AsyncWrapper()
		layout = Builder.load_string(kv)
		Window.size = (1200, 500)
		Window.clearcolor = (0.15, 0.15, 0.15, 1)

		self.title = 'Ham Radio Sync'

		self._bind_radio_menu(layout)
		self._bind_console_log(layout)
		self._bind_file_menu(layout)
		self._bind_dangerous_ops_menu(layout)
		self._bind_help_menu(layout)

		create_radio_button = layout.ids['create_radio_plugs']
		dangerous_ops_button = layout.ids['enable_dangerous']
		dangerous_ops_menu = layout.ids['dangerous_operations']
		buttons = [create_radio_button, dangerous_ops_button, dangerous_ops_menu]
		self._async_wrapper.buttons = buttons

		logging.info("Welcome to the ham radio sync app.")
		return layout

	def _bind_radio_menu(self, layout):
		button_pool = layout.ids['radio_labels']

		radio_select_buttons = dict()
		radios = [
			radio_types.DEFAULT,
			radio_types.D878,
			radio_types.BAOFENG,
			radio_types.CS800,
			radio_types.FTM400,
		]

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

		create_button = layout.ids['create_radio_plugs']
		create_button.bind(on_press=self._async_wrapper.radio_generator)

	def _bind_console_log(self, layout):
		text_log = layout.ids['log_output']
		self.text_log = text_log

		logger = logging.getLogger('radio_sync')
		formatter = logging.Formatter(
			fmt='%(asctime)s.%(msecs)03d %(levelname)7s %(filename).6s:%(lineno)3s:  %(message)s',
			datefmt="%Y-%m-%d %H:%M:%S"
		)

		text_box_logger = TextBoxHandler(self.text_log)
		handler = logging.StreamHandler(stream=text_box_logger)
		handler.setFormatter(formatter)

		logger.setLevel(logging.INFO)
		if self.force_debug:
			logger.setLevel(logging.DEBUG)

		logger.addHandler(handler)

	def _bind_file_menu(self, layout):
		exit_button = layout.ids['exit_button']
		exit_button.bind(on_press=self.stop)

	def _bind_dangerous_ops_menu(self, layout):
		dangerous_ops_button = layout.ids['enable_dangerous']
		dangerous_ops_button.bind(on_press=self._async_wrapper.arm_dangerous)
		self._async_wrapper.dangerous_ops_toggle = dangerous_ops_button

		dangerous_ops_menu = layout.ids['dangerous_operations']
		self._async_wrapper.dangerous_buttons = [dangerous_ops_menu]
		dangerous_ops_menu.disabled = True

		cleanup_button = layout.ids['dangerous_operations.cleanup']
		cleanup_button.bind(on_press=self._async_wrapper.wizard_cleanup)

		wizard_button = layout.ids['dangerous_operations.wizard']
		wizard_button.bind(on_press=self._async_wrapper.wizard_bootstrap)

		migrate_button = layout.ids['dangerous_operations.migrate']
		migrate_button.bind(on_press=self._async_wrapper.migrations)

		delete_migrate_button = layout.ids['dangerous_operations.delete_migrate']
		delete_migrate_button.bind(on_press=self._async_wrapper.migration_backups)

	def _bind_help_menu(self, layout):
		debug_button = layout.ids['debug_toggle']
		self._async_wrapper.debug_toggle = debug_button
		debug_button.bind(on_press=self._async_wrapper.log_level)

		about_button = layout.ids['about']
		about_button.bind(on_press=self._async_wrapper.display_about_info)


class TextBoxHandler(TextIO, ABC):
	def __init__(self, text_log):
		self._text_log = text_log
		self.lock = None

	def write(self, record):
		self._text_log.text += record
		return


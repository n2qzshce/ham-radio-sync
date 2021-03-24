import logging
from abc import ABC
from typing import TextIO

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
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
					text: "Exit"
			ActionGroup:
				text: "Dangerous Operations"
				mode: "spinner"
				dropdown_width: 225
				ActionButton:
					text: "Cleanup"
				ActionButton:
					text: "Wizard"
				ActionButton:
					text: "Migrate to latest format"
				ActionButton:
					text: "Remove migration backups"
			ActionGroup:
				text: "Help"
				mode: "spinner"
				ActionButton:
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
				text: 'lorem\\nipsum'
				size_hint: (1, 1)
				readonly: True
				font_size: 11
"""


class AppWindow(App):
	text_log = None
	_async_wrapper = None

	def build(self):
		self._async_wrapper = AsyncWrapper()
		layout = Builder.load_string(kv)
		Window.size = (1200, 500)
		Window.clearcolor = (0.15, 0.15, 0.15, 1)

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
		logger.addHandler(handler)

		return layout

	def build_old(self):
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


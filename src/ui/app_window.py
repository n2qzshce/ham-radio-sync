import logging
import os
import sys
from abc import ABC
from typing import TextIO

from kivy import metrics
from kivy.app import App
from kivy.base import EventLoop
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.resources import resource_add_path
from kivy.resources import resource_paths
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from src import radio_sync_version
from src.ham.util import radio_types
from src.ham.util.path_manager import PathManager
from src.ui.async_wrapper import AsyncWrapper

Config.set('input', 'mouse', 'mouse,disable_multitouch')


class RightClickTextInput(TextInput):
	def on_touch_down(self, touch):

		super().on_touch_down(touch)

		if not self.focused:
			return

		if touch.button == 'right':
			logging.debug("right mouse clicked")
			pos = self.to_local(*self._long_touch_pos, relative=False)
			pos = (pos[0], pos[1] - metrics.inch(.25))
			self._show_cut_copy_paste(
				pos, EventLoop.window, mode='paste')


class LayoutIds:
	action_previous = 'action_previous'
	buffer = 'buffer'
	button_pool = 'button_pool'
	create_radio_plugs = 'create_radio_plugs'
	cant_find_radio = 'cant_find_radio'
	check_migrations = 'check_migrations'
	clear_log = 'clear_log'
	debug_toggle = 'debug_toggle'
	dangerous_operations = 'dangerous_operations'
	dangerous_operation__delete_migrate = 'dangerous_operation__delete_migrate'
	dangerous_operation__migrate = 'dangerous_operation__migrate'
	dangerous_operation__wizard = 'dangerous_operation__wizard'
	dangerous_operation__cleanup = 'dangerous_operation__cleanup'
	enable_dangerous = 'enable_dangerous'
	exit_button = 'exit_button'
	feature_request = 'feature_request'
	getting_started = 'getting_started'
	input_folder = 'input_folder'
	input_folder_select = 'input_folder_select'
	output_folder = 'output_folder'
	output_folder_select = 'output_folder_select'
	log_output = 'log_output'
	radio_descriptions = 'radio_descriptions'
	radio_header = 'radio_header'
	radio_labels = 'radio_labels'


kv = f"""
BoxLayout:
	orientation: "vertical"
	ActionBar:
		ActionView:
			ActionPrevious:
				id: {LayoutIds.action_previous}
				title: 'Ham Radio Sync'
				with_previous: False
				enabled: False
			ActionButton:
				id: {LayoutIds.create_radio_plugs}
				text: "Create Radio Plugs"
				background_normal:''
				background_down: ''
				background_color: [0.00,0.40,0.13,1.0]
			ActionToggleButton:
				id: {LayoutIds.enable_dangerous}
				text: "Enable Dangerous Operations"
			ActionSeparator:
				important: True
			ActionGroup:
				text: "File"
				mode: "spinner"
				dropdown_width: dp(225)
				ActionButton:
					id: {LayoutIds.check_migrations}
					text: "Check for needed migrations"
				ActionButton:
					id: {LayoutIds.input_folder_select}
					text: "Set input directory"
				ActionButton:
					id: {LayoutIds.output_folder_select}
					text: "Set output directory"
				ActionButton:
					id: {LayoutIds.clear_log}
					text: "Clear screen log"
				ActionButton:
					id: {LayoutIds.exit_button}
					text: "Exit"
			ActionGroup:
				text: "Dangerous Operations"
				mode: "spinner"
				id: {LayoutIds.dangerous_operations}
				dropdown_width: dp(225)
				ActionButton:
					id: {LayoutIds.dangerous_operation__delete_migrate}
					text: "Remove migration backups"
				ActionButton:
					id: {LayoutIds.dangerous_operation__migrate}
					text: "Migrate to latest format"
				ActionButton:
					id: {LayoutIds.dangerous_operation__wizard}
					text: "Wizard"
				ActionButton:
					id: {LayoutIds.dangerous_operation__cleanup}
					text: "Cleanup"
			ActionGroup:
				text: "Help / Getting Started"
				mode: "spinner"
				dropdown_width: dp(250)
				ActionButton:
					id: {LayoutIds.getting_started}
					text: "About/Getting started..."
				ActionButton:
					id: {LayoutIds.radio_descriptions}
					text: "Radio model/program list"
				ActionButton:
					id: {LayoutIds.cant_find_radio}
					text: "My radio isn't here"
				ActionButton:
					id: {LayoutIds.feature_request}
					text: "Feature request/bug report"
				ActionToggleButton:
					id: {LayoutIds.debug_toggle}
					text: "Debug logging"
	BoxLayout:
		orientation: "horizontal"
		StackLayout:
			id: {LayoutIds.button_pool}
			spacing: dp(10)
			size_hint: (0.2, 1)
			padding: [dp(20), dp(20), dp(20), dp(20)]
			size_hint_min_x: dp(225)
			size_hint_max_x: dp(275)
			Label:
				id: {LayoutIds.radio_header}
				text: "Radios to Generate"
				size_hint: (1.0, 0.1)
				font_size: dp(15)
				bold: True
			BoxLayout:
				id: {LayoutIds.radio_labels}
				orientation: "vertical"
				spacing: dp(10)
				size_hint: (1, 0.4)
			BoxLayout:
				id: {LayoutIds.buffer}
				orientation: "vertical"
				size_hint: (1, 0.2)
		BoxLayout:
			orientation: "vertical"
			size_hint: (0.8, 1)
			Label:
				id: {LayoutIds.input_folder}
				text: "Input folder: None"
				valign: 'middle'
				size_hint: (1, 0.1)
				text_size: self.size
			Label:
				id: {LayoutIds.output_folder}
				text: "Output folder: None"
				valign: 'middle'
				size_hint: (1, 0.1)
				text_size: self.size
			RightClickTextInput:
				id: {LayoutIds.log_output}
				font_name: 'RobotoMono-Regular'
				text: ''
				size_hint: (1, 1)
				readonly: True
				font_size: dp(11)
				use_bubble: True
"""


class AppWindow(App):
	text_log = None
	_async_wrapper = None
	force_debug = False
	popup_manager = None

	def build(self):
		icon_path = './images/radio_sync.ico'
		action_icon_path = './images/radio_sync.png'
		if hasattr(sys, '_MEIPASS'):
			logging.debug("Has _MEIPASS")
			logging.debug(os.listdir(sys._MEIPASS))
			icon_path = os.path.join(sys._MEIPASS, 'images/radio_sync.ico')
			action_icon_path = os.path.join(sys._MEIPASS, 'images/radio_sync.png')
			logging.debug(f"Icon path: `{icon_path}`")
			if os.path.exists(icon_path):
				logging.debug("Icon path exists")
			resource_add_path(os.path.join(sys._MEIPASS, 'images'))
		else:
			resource_add_path('images')

		self.icon = icon_path
		logging.debug(f"Resource paths: `{resource_paths}`")

		self._async_wrapper = AsyncWrapper()
		layout = Builder.load_string(kv)
		Window.size = (dp(1200), dp(550))
		Window.clearcolor = (0.15, 0.15, 0.15, 1)
		Window.bind(on_keyboard=self.key_handler)

		self.title = f'Ham Radio Sync v{radio_sync_version.version}'

		action_previous = layout.ids[LayoutIds.action_previous]
		action_previous.app_icon = action_icon_path

		self._bind_radio_menu(layout)
		self._bind_console_log(layout)
		self._bind_file_menu(layout)
		self._bind_dangerous_ops_menu(layout)
		self._bind_help_menu(layout)

		create_radio_button = layout.ids[LayoutIds.create_radio_plugs]
		dangerous_ops_button = layout.ids[LayoutIds.enable_dangerous]
		dangerous_ops_menu = layout.ids[LayoutIds.dangerous_operations]
		buttons = [create_radio_button, dangerous_ops_button, dangerous_ops_menu]
		self._async_wrapper.buttons = buttons

		logging.info("Welcome to the ham radio sync app.")
		self._async_wrapper.check_version(None)
		return layout

	def key_handler(self, window, keycode1, keycode2, text, modifiers):
		if keycode1 == 27 or keycode1 == 1001:
			return True
		return False

	def _bind_radio_menu(self, layout):
		button_pool = layout.ids[LayoutIds.radio_labels]

		radio_select_buttons = dict()
		radios = radio_types.radio_choices()

		for radio in radios:
			radio_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

			radio_label = Label(text=radio_types.pretty_name(radio), size_hint=(0.9, 1), font_size=dp(11), halign='left')
			radio_checkbox = CheckBox(size_hint=(0.1, 1))
			radio_checkbox.active = radio == radio_types.DEFAULT
			radio_label.bind(size=radio_label.setter('text_size'))

			radio_layout.add_widget(radio_label)
			radio_layout.add_widget(radio_checkbox)

			radio_select_buttons[radio] = radio_checkbox

			button_pool.add_widget(radio_layout)

		self._async_wrapper.radio_buttons = radio_select_buttons

		create_button = layout.ids[LayoutIds.create_radio_plugs]
		create_button.bind(on_press=self._async_wrapper.radio_generator)

	def _bind_console_log(self, layout):
		text_log = layout.ids[LayoutIds.log_output]
		self.text_log = text_log

		input_folder = layout.ids[LayoutIds.input_folder]
		output_folder = layout.ids[LayoutIds.output_folder]

		PathManager.input_folder_label = input_folder
		PathManager.output_folder_label = output_folder
		PathManager.set_input_path('./in')
		PathManager.set_output_path('./out')

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
		check_migrations_button = layout.ids[LayoutIds.check_migrations]
		check_migrations_button.bind(on_press=self._async_wrapper.check_migrations)

		clear_console_button = layout.ids[LayoutIds.clear_log]
		clear_console_button.bind(on_press=self._clear_console)

		self.popup_manager = PopupManager()
		input_folder_button = layout.ids[LayoutIds.input_folder_select]
		input_folder_button.bind(on_press=self.popup_manager.select_input_folder_dialog)

		output_folder_button = layout.ids[LayoutIds.output_folder_select]
		output_folder_button.bind(on_press=self.popup_manager.select_output_folder_dialog)

		exit_button = layout.ids[LayoutIds.exit_button]
		exit_button.bind(on_press=self.stop)

	def _bind_dangerous_ops_menu(self, layout):
		dangerous_ops_button = layout.ids[LayoutIds.enable_dangerous]
		dangerous_ops_button.bind(on_press=self._async_wrapper.arm_dangerous)
		self._async_wrapper.dangerous_ops_toggle = dangerous_ops_button

		dangerous_ops_menu = layout.ids[LayoutIds.dangerous_operations]
		self._async_wrapper.dangerous_buttons = [dangerous_ops_menu]
		dangerous_ops_menu.disabled = True

		cleanup_button = layout.ids[LayoutIds.dangerous_operation__cleanup]
		cleanup_button.bind(on_press=self._async_wrapper.wizard_cleanup)

		wizard_button = layout.ids[LayoutIds.dangerous_operation__wizard]
		wizard_button.bind(on_press=self._async_wrapper.wizard_bootstrap)

		migrate_button = layout.ids[LayoutIds.dangerous_operation__migrate]
		migrate_button.bind(on_press=self._async_wrapper.migrations)

		delete_migrate_button = layout.ids[LayoutIds.dangerous_operation__delete_migrate]
		delete_migrate_button.bind(on_press=self._async_wrapper.migration_backups)

	def _bind_help_menu(self, layout):
		debug_button = layout.ids[LayoutIds.debug_toggle]
		self._async_wrapper.debug_toggle = debug_button
		debug_button.bind(on_press=self._async_wrapper.log_level)

		contact_button = layout.ids[LayoutIds.cant_find_radio]
		contact_button.bind(on_press=self._async_wrapper.contact_info)

		feature_request_button = layout.ids[LayoutIds.feature_request]
		feature_request_button.bind(on_press=self._async_wrapper.contact_info)

		getting_started_button = layout.ids[LayoutIds.getting_started]
		getting_started_button.bind(on_press=self._async_wrapper.display_start_info)

		compatible_radios_button = layout.ids[LayoutIds.radio_descriptions]
		compatible_radios_button.bind(on_press=self._async_wrapper.compatible_radios)

	def _clear_console(self, event):
		self.text_log.text = ''
		logging.info("Console has been cleared.")

	def right_click_down(self, touch):
		if touch.button == 'right':
			print("right mouse clicked")
			pos = touch.to_local(*self._long_touch_pos, relative=True)

			self._show_cut_copy_paste(
				pos, EventLoop.window, mode='paste')


class PopupIds:
	cancel_button = "cancel_button"
	file_chooser = "file_chooser"
	file_path = "file_path"
	load_button = "load_button"
	mode = "mode"


load_dialog = f"""
BoxLayout:
	size: root.size
	pos: root.pos
	orientation: "vertical"
	Label:
		id: {PopupIds.mode}
		size_hint_y: 0
		text: "mode"
	TextInput:
		size_hint: (1, 0.1)
		id: {PopupIds.file_path}
		text: "None"
		multiline: False
	FileChooserListView:
		size_hint: (1, 0.9)
		id: {PopupIds.file_chooser}
		dirselect: True
		filters: ["!*"]

	BoxLayout:
		size_hint_y: None
		height: 30

		Button:
			id: {PopupIds.load_button}
			text: "Load"
		Button:
			id: {PopupIds.cancel_button}
			text: "Cancel"
"""


class PopupManager:
	def select_input_folder_dialog(self, event):
		self._select_folder_dialog(event, 'Set input directory', PathManager.get_input_path(), self._select_input_folder)

	def select_output_folder_dialog(self, event):
		self._select_folder_dialog(event, 'Set output directory', PathManager.get_output_path(), self._select_output_folder)

	def _select_folder_dialog(self, event, title, starting_path, load_button_action):
		dialog_content = Builder.load_string(load_dialog)
		file_chooser = dialog_content.ids[PopupIds.file_chooser]
		file_chooser.path = starting_path
		file_chooser.bind(selection=self._update_display_path)

		file_label = dialog_content.ids[PopupIds.file_path]
		file_label.text = file_chooser.path

		self._popup = Popup(title=title, content=dialog_content, size_hint=(0.9, 0.9))
		dialog_content.ids[PopupIds.cancel_button].bind(on_press=self._dismiss_popup)

		dialog_content.ids[PopupIds.load_button].bind(on_press=load_button_action)

		self._popup.open()
		return

	def _select_input_folder(self, event):
		path = self._get_selected_path()
		PathManager.set_input_path(path)
		self._dismiss_popup(None)

	def _select_output_folder(self, event):
		path = self._get_selected_path()
		PathManager.set_output_path(path)
		self._dismiss_popup(None)

	def _dismiss_popup(self, event):
		self._popup.dismiss()

	def _update_display_path(self, *args):
		file_label = self._popup.content.ids[PopupIds.file_path]
		file_label.text = self._get_selected_path()

	def _get_selected_path(self):
		file_chooser = self._popup.content.ids[PopupIds.file_chooser]

		result = file_chooser.path
		if len(file_chooser.selection) == 1:
			result = file_chooser.selection[0]
		return result


class TextBoxHandler(TextIO, ABC):
	def __init__(self, text_log):
		self._text_log = text_log
		self.lock = None

	def write(self, record):
		self._text_log.text += record
		return

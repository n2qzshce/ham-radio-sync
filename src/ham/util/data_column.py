import logging

from src.ham.util import radio_types


class DataColumn:
	_alias_names = dict()
	_fmt_val = None
	shape = None

	def __init__(self, fmt_name=None, fmt_val=None, shape=None):
		if shape is None:
			logging.error("Shape is null! Bad things will happen.")
		self._fmt_val = fmt_val
		self._alias_names = dict()
		self._alias_names[radio_types.DEFAULT] = fmt_name
		self.shape = shape

	def set_alias(self, style, name):
		self._alias_names[style] = name

	def get_alias(self, style):
		if style not in self._alias_names.keys():
			logging.error(f"Cannot find alias for style: `{style}` of `{self._alias_names[radio_types.DEFAULT]}`")
		return self._alias_names[style]

	def fmt_val(self, none_val=None):
		if self._fmt_val == '':
			return none_val

		return self.shape(self._fmt_val)

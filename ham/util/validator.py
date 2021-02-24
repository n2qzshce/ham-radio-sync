import logging

from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.dmr.dmr_user import DmrUser
from ham.radio.radio_channel import RadioChannel
from ham.radio.radio_zone import RadioZone
from ham.util import radio_types
from ham.util.data_column import DataColumn
from ham.util.validation_error import ValidationError


class Validator:
	def __init__(self):
		self._radio_channel_template = RadioChannel.create_empty()
		self._digital_contact_template = DmrContact.create_empty()
		self._dmr_id_template = DmrId.create_empty()
		self._zone_template = RadioZone.create_empty()
		self._dmr_user_template = DmrUser.create_empty()

		self._short_names = dict()
		self._medium_names = dict()
		self._long_names = dict()
		return

	def validate_dmr_user(self, cols, line_num, file_name):
		needed_cols_dict_gen = dict(self._dmr_user_template.__dict__)
		return self._validate_generic(cols, line_num, file_name, needed_cols_dict_gen)

	def validate_radio_zone(self, cols, line_num, file_name):
		needed_cols_dict_gen = dict(self._zone_template.__dict__)
		return self._validate_generic(cols, line_num, file_name, needed_cols_dict_gen)

	def validate_dmr_id(self, cols, line_num, file_name):
		needed_cols_dict_gen = dict(self._dmr_id_template.__dict__)
		return self._validate_generic(cols, line_num, file_name, needed_cols_dict_gen)

	def validate_digital_contact(self, cols, line_num, file_name):
		needed_cols_dict_gen = dict(self._digital_contact_template.__dict__)
		return self._validate_generic(cols, line_num, file_name, needed_cols_dict_gen)

	def validate_radio_channel(self, cols, line_num, file_name):
		needed_cols_dict_gen = dict(self._radio_channel_template.__dict__)
		errors = self._validate_generic(cols, line_num, file_name, needed_cols_dict_gen)
		if len(errors) > 0:
			return errors

		channel = RadioChannel(cols, None, None)
		if channel.short_name.fmt_val() in self._short_names.keys():
			err = ValidationError(
							f"Collision in {channel.short_name.get_alias(radio_types.DEFAULT)} "
							f"(value: `{channel.short_name.fmt_val()}`) found with line"
							f" {self._short_names[channel.short_name.fmt_val()]}."
							f" Codeplug applications do not handle this well.", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		else:
			self._short_names[channel.short_name.fmt_val()] = line_num

		if channel.medium_name.fmt_val() in self._medium_names.keys():
			err = ValidationError(
							f"Collision in {channel.medium_name.get_alias(radio_types.DEFAULT)} "
							f"(value: `{channel.medium_name.fmt_val()}`) found with line"
							f" {self._medium_names[channel.medium_name.fmt_val()]}."
							f" Codeplug applications do not handle this well.", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		else:
			self._medium_names[channel.medium_name.fmt_val()] = line_num

		if channel.name.fmt_val() in self._long_names.keys():
			err = ValidationError(
							f"Collision in {channel.name.get_alias(radio_types.DEFAULT)} "
							f"(value: `{channel.name.fmt_val()}`) found with line"
							f" {self._long_names[channel.name.fmt_val()]}."
							f" Codeplug applications do not handle this well.", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		else:
			self._long_names[channel.name.fmt_val()] = line_num

		return errors

	def _validate_generic(self, cols, line_num, file_name, needed_cols_dict_gen):
		errors = []
		needed_cols = dict()

		for val in needed_cols_dict_gen.values():
			if not isinstance(val, DataColumn):
				logging.debug(f"Skipping adding `{val}` to needed cols")
				continue
			needed_cols[val.get_alias(radio_types.DEFAULT)] = val

		ignored_cols = []
		for col in cols.keys():
			if col not in needed_cols.keys():
				ignored_cols.append(col)

		for ignored in ignored_cols:
			cols.pop(ignored)

		for key in cols.keys():
			if key not in needed_cols.keys():
				err = ValidationError(f"`{key}` missing from entry.", line_num, file_name)
				errors.append(err)
				continue
			data_column = needed_cols[key]

			if cols[key] == '':
				continue

			try:
				data_column.shape(cols[key])
			except ValueError:
				shape_name = str(data_column.shape).replace("<class '", '').replace("'>", '')
				err = ValidationError(
										f"Error parsing `{cols[key]}` in column `{key}` as `{shape_name}`",
										line_num,
										file_name
									)
				logging.debug(err.message)
				errors.append(err)
		return errors

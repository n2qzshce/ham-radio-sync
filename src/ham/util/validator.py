import logging
import operator

from src.ham.radio.default_radio.dmr_contact_default import DmrContactDefault
from src.ham.radio.default_radio.dmr_id_default import DmrIdDefault
from src.ham.radio.default_radio.dmr_user_default import DmrUserDefault
from src.ham.radio.default_radio.radio_channel_default import RadioChannelDefault
from src.ham.radio.default_radio.radio_zone_default import RadioZoneDefault
from src.ham.radio.radio_channel import RadioChannel
from src.ham.util import radio_types
from src.ham.util.data_column import DataColumn
from src.ham.util.path_manager import PathManager
from src.ham.util.validation_error import ValidationError


class Validator:
	MAX_MEDIUM_NAME_LENGTH = 8
	MAX_SHORT_NAME_LENGTH = 7

	def __init__(self):
		self._radio_channel_template = RadioChannelDefault.create_empty()
		self._digital_contact_template = DmrContactDefault.create_empty()
		self._dmr_id_template = DmrIdDefault.create_empty()
		self._zone_template = RadioZoneDefault.create_empty()
		self._dmr_user_template = DmrUserDefault.create_empty()

		self._short_names = None
		self._medium_names = None
		self._long_names = None
		return

	def flush_names(self):
		self._short_names = dict()
		self._medium_names = dict()
		self._long_names = dict()

	@classmethod
	def validate_files_exist(cls):
		errors = []

		files_list = ['input.csv', 'digital_contacts.csv', 'dmr_id.csv', 'zones.csv', 'user.csv']
		for file_name in files_list:
			if not PathManager.input_path_exists(file_name):
				err = ValidationError(f"Cannot open file: `{file_name}`", None, file_name)
				errors.append(err)

		if len(errors) > 0:
			logging.error("--- FILE MISSING ERRORS, CANNOT CONTINUE ---")
			logging.info(f"Checked `{PathManager.get_input_path()}`")
			for err in errors:
				logging.error(f"\t\t{err.message}")
			logging.info("Have you run `Wizard (new)` or `Migrations (update)` under `Dangerous Operations`?")
		else:
			logging.info("All necessary files found")

		return errors

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

	def validate_radio_channel(self, cols, line_num, file_name, digital_contacts, zones):
		needed_cols_dict_gen = dict(self._radio_channel_template.__dict__)
		errors = self._validate_generic(cols, line_num, file_name, needed_cols_dict_gen)
		if len(errors) > 0:
			return errors

		channel = RadioChannel(cols, None, None)

		if len(channel.medium_name.fmt_val()) > self.MAX_MEDIUM_NAME_LENGTH:
			err = ValidationError(f"Line {line_num} '{channel.medium_name.get_alias(radio_types.DEFAULT)}' greater than {self.MAX_MEDIUM_NAME_LENGTH} characters in length", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		if len(channel.short_name.fmt_val()) > self.MAX_SHORT_NAME_LENGTH:
			err = ValidationError(f"Line {line_num} '{channel.short_name.get_alias(radio_types.DEFAULT)}' greater than {self.MAX_MEDIUM_NAME_LENGTH} characters in length", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)

		if channel.short_name.fmt_val() is None:
			err = ValidationError(f"'medium_name' column cannot be empty", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		elif channel.short_name.fmt_val().lower() in self._short_names.keys():
			err = ValidationError(
							f"Collision in {channel.short_name.get_alias(radio_types.DEFAULT)} "
							f"(value: `{channel.short_name.fmt_val()}`) found with line"
							f" {self._short_names[channel.short_name.fmt_val().lower()]}."
							f" Codeplug applications do not handle this well.", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		else:
			self._short_names[channel.short_name.fmt_val().lower()] = line_num

		if channel.medium_name.fmt_val() is None:
			err = ValidationError(f"'medium_name' column cannot be empty", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		elif channel.medium_name.fmt_val().lower() in self._medium_names.keys():
			err = ValidationError(
							f"Collision in {channel.medium_name.get_alias(radio_types.DEFAULT)} "
							f"(value: `{channel.medium_name.fmt_val()}`) found with line"
							f" {self._medium_names[channel.medium_name.fmt_val().lower()]}."
							f" Codeplug applications do not handle this well.", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		else:
			self._medium_names[channel.medium_name.fmt_val().lower()] = line_num

		if channel.name.fmt_val() is None:
			err = ValidationError(f"'name' column cannot be empty", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		elif channel.name.fmt_val().lower() in self._long_names.keys():
			err = ValidationError(
							f"Collision in {channel.name.get_alias(radio_types.DEFAULT)} "
							f"(value: `{channel.name.fmt_val()}`) found with line"
							f" {self._long_names[channel.name.fmt_val().lower()]}."
							f" Codeplug applications do not handle this well.", line_num, file_name)
			logging.debug(err.message)
			errors.append(err)
		else:
			self._long_names[channel.name.fmt_val().lower()] = line_num

		if channel.rx_dcs.fmt_val(23) not in radio_types.dcs_codes_inverses.keys():
			err = ValidationError(
							f"Invalid RX DCS code `{channel.rx_dcs.fmt_val()}` specified.", line_num, file_name
			)
			errors.append(err)
		if channel.tx_dcs.fmt_val(23) not in radio_types.dcs_codes_inverses.keys():
			err = ValidationError(
							f"Invalid RX DCS code `{channel.rx_dcs.fmt_val()}` specified.", line_num, file_name
			)
			errors.append(err)

		if channel.is_digital() and channel.digital_contact_id.fmt_val() not in digital_contacts.keys():
			err = ValidationError(
							f"Cannot find digital contact `{channel.digital_contact_id.fmt_val()}` specified in "
							f"digital contacts.", line_num, file_name
			)
			errors.append(err)

		acceptable_tx_powers = ["Low", "Medium", "High"]
		if channel.tx_power.fmt_val() is None or channel.tx_power.fmt_val() not in acceptable_tx_powers:
			err = ValidationError(
							f"Transmit power (`tx_power`) invalid: `{channel.digital_contact_id.fmt_val()}`. Valid values "
							f"are {acceptable_tx_powers}"
							, line_num, file_name
			)
			errors.append(err)

		if channel.zone_id.fmt_val() is not None and channel.zone_id.fmt_val() not in zones.keys():
			err = ValidationError(
							f"Zone ID not found: `{channel.zone_id.fmt_val()}`. in `zones.csv` and was not left empty."
							, line_num, file_name
			)
			errors.append(err)

		if operator.xor(channel.latitude.fmt_val() is None, channel.longitude.fmt_val() is None):
			err = ValidationError(
							f"Only one of latitude or longitude provided. Lat: `{channel.latitude.fmt_val()}` "
							f"Long: `{channel.longitude.fmt_val()}"
							, line_num, file_name
			)
			errors.append(err)

		if channel.latitude.fmt_val() is not None and not -90 <= channel.latitude.fmt_val() <= 90:
			err = ValidationError(
							f"Latitude must be between -90 and 90. Lat: `{channel.latitude.fmt_val()}`"
							, line_num, file_name
			)
			errors.append(err)

		if channel.longitude.fmt_val() is not None and not -180 <= channel.longitude.fmt_val() <= 180:
			err = ValidationError(
							f"Longitude must be between -180 and 180. Lat: `{channel.longitude.fmt_val()}`"
							, line_num, file_name
			)
			errors.append(err)

		return errors

	def _validate_generic(self, cols, line_num, file_name, needed_cols_dict_gen):
		errors = []
		needed_cols = dict()

		for val in needed_cols_dict_gen.values():
			if not isinstance(val, DataColumn):
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

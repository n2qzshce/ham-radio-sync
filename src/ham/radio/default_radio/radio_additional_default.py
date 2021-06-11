import csv
import logging

from src.ham.radio.default_radio.dmr_contact_default import DmrContactDefault
from src.ham.radio.default_radio.dmr_id_default import DmrIdDefault
from src.ham.radio.default_radio.dmr_user_default import DmrUserDefault
from src.ham.radio.default_radio.radio_zone_default import RadioZoneDefault
from src.ham.radio.radio_additional import RadioAdditional
from src.ham.radio.radio_casted_builder import DmrIdBuilder, RadioZoneBuilder, DmrContactBuilder, DmrUserBuilder
from src.ham.util import radio_types
from src.ham.util.path_manager import PathManager


class RadioAdditionalDefault(RadioAdditional):
	def __init__(self, channels, dmr_ids, digital_contacts, zones, users):
		super().__init__(channels, dmr_ids, digital_contacts, zones, users)

	def output(self):
		self._output_radioids()
		self._output_contacts()
		self._output_zones()
		self._output_user()

	def _output_radioids(self):
		if self._dmr_ids is None:
			logging.error(f"No DMR ids found for {radio_types.DEFAULT}.")
			return

		writer = PathManager.open_output_file(f'{radio_types.DEFAULT}/{radio_types.DEFAULT}_radioid.csv', 'w+')
		radio_id_file = csv.writer(writer, lineterminator='\n')

		headers = DmrIdDefault.create_empty()
		radio_id_file.writerow(headers.headers())
		number = 1
		for dmr_id in self._dmr_ids.values():
			casted_id = DmrIdBuilder.casted(dmr_id, radio_types.DEFAULT)
			radio_id_file.writerow(casted_id.output(None))
			number += 1

		writer.close()
		return

	def _output_zones(self):
		if self._zones is None:
			logging.error(f"No zones list found for {radio_types.DEFAULT}.")
			return

		writer = PathManager.open_output_file(f'{radio_types.DEFAULT}/{radio_types.DEFAULT}_zone.csv', 'w+')
		zone_file = csv.writer(writer, lineterminator='\n')

		headers = RadioZoneDefault.create_empty()
		zone_file.writerow(headers.headers())
		for zone in self._zones.values():
			casted_zone = RadioZoneBuilder.casted(zone.cols, zone._associated_channels, radio_types.DEFAULT)
			zone_file.writerow(casted_zone.output())

		writer.close()

	def _output_contacts(self):
		if self._digital_contacts is None:
			logging.error(f"No digital contacts found for {radio_types.DEFAULT}.")
			return

		writer = PathManager.open_output_file(f'{radio_types.DEFAULT}/{radio_types.DEFAULT}_contacts.csv', 'w+')
		dmr_contact_file = csv.writer(writer, lineterminator='\n')

		headers = DmrContactDefault.create_empty()
		dmr_contact_file.writerow(headers.headers())
		for dmr_contact in self._digital_contacts.values():
			casted_contact = DmrContactBuilder.casted(dmr_contact, radio_types.DEFAULT)
			row_data = casted_contact.output(None)
			dmr_contact_file.writerow(row_data)

		writer.close()

	def _output_user(self):
		if self._users is None:
			logging.error(f"No zones list found for {radio_types.DEFAULT}.")
			return

		writer = PathManager.open_output_file(f'{radio_types.DEFAULT}/{radio_types.DEFAULT}_user.csv', 'w+')
		users_file = csv.writer(writer, lineterminator='\n')

		headers = DmrUserDefault.create_empty()
		users_file.writerow(headers.headers())
		for user in self._users.values():
			casted_user = DmrUserBuilder.casted(user.cols, radio_types.DEFAULT)
			users_file.writerow(casted_user.output(None))

		writer.close()

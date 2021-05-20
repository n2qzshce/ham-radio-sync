import logging

from src.ham.radio.d878.dmr_contact_d878 import DmrContactD878
from src.ham.radio.d878.dmr_id_d878 import DmrIdD878
from src.ham.radio.d878.dmr_user_d878 import DmrUserD878
from src.ham.radio.d878.radio_zone_d878 import RadioZoneD878
from src.ham.radio.radio_additional import RadioAdditional
from src.ham.radio.radio_casted_builder import DmrContactBuilder, DmrIdBuilder, DmrUserBuilder, \
	RadioZoneBuilder
from src.ham.util import radio_types, file_util
from src.ham.util.file_util import RadioWriter


class RadioAdditionalD878(RadioAdditional):
	def __init__(self, channels, dmr_ids, digital_contacts, zones, users):
		super().__init__(channels, dmr_ids, digital_contacts, zones, users)
		
		self._style = radio_types.D878
		return

	def output(self):
		self._output_radioids()
		self._output_contacts()
		self._output_zones()
		self._output_user()

	def _output_radioids(self):
		logging.info(f"Writing {self._style} radio IDs")
		if self._dmr_ids is None:
			logging.error(f"No DMR ids found for {self._style}.")
			return

		radio_id_file = RadioWriter.output_writer(f'{self._style}/{self._style}_radioid.csv', '\r\n')

		headers = DmrIdD878.create_empty()
		radio_id_file.writerow(headers.headers())
		number = 1
		for dmr_id in self._dmr_ids.values():
			casted_id = DmrIdBuilder.casted(dmr_id, radio_types.D878)
			radio_id_file.writerow(casted_id.output(number))
			number += 1

		radio_id_file.close()
		return

	def _output_contacts(self):
		logging.info(f"Writing {self._style} contacts")
		if self._digital_contacts is None:
			logging.error(f"No digital contacts found for {self._style}.")
			return

		dmr_contact_file = RadioWriter.output_writer(f'{self._style}/{self._style}_talkgroup.csv', '\r\n')

		headers = DmrContactD878.create_empty()
		dmr_contact_file.writerow(headers.headers())
		number = 1
		for dmr_contact in self._digital_contacts.values():
			casted_contact = DmrContactBuilder.casted(dmr_contact, self._style)
			row_data = casted_contact.output(number)
			dmr_contact_file.writerow(row_data)
			number += 1

		dmr_contact_file.close()

	def _output_zones(self):
		logging.info(f"Writing {self._style} zones")
		if self._zones is None:
			logging.error(f"No zones list found for {self._style}.")
			return

		zone_file = RadioWriter.output_writer(f'{self._style}/{self._style}_zone.csv', '\r\n')

		headers = RadioZoneD878.create_empty()
		zone_file.writerow(headers.headers())
		for zone in self._zones.values():
			if not zone.has_channels():
				continue
			casted_zone = RadioZoneBuilder.casted(zone.cols, zone._associated_channels, self._style)
			zone_file.writerow(casted_zone.output())

		zone_file.close()

	def _output_user(self):
		logging.info(f"Writing {self._style} users")
		if self._users is None:
			logging.error(f"No zones list found for {self._style}.")
			return

		users_file = RadioWriter.output_writer(f'{self._style}/{self._style}_digital_contacts.csv', '\n')

		headers = DmrUserD878.create_empty()
		users_file.writerow(headers.headers())

		rows_processed = 1
		for user in self._users.values():
			casted_user = DmrUserBuilder.casted(user.cols, self._style)
			users_file.writerow(casted_user.output(None))
			rows_processed += 1
			logging.debug(f"Writing user row {rows_processed}")
			if rows_processed % file_util.USER_LINE_LOG_INTERVAL == 0:
				logging.info(f"Writing user row {rows_processed}")

		users_file.close()

import csv
import logging

import openpyxl

from src.ham.dmr.dmr_contact import DmrContact
from src.ham.dmr.dmr_id import DmrId
from src.ham.dmr.dmr_user import DmrUser
from src.ham.radio.radio_channel import RadioChannel
from src.ham.radio.radio_channel_builder import RadioChannelBuilder
from src.ham.radio.radio_zone import RadioZone
from src.ham.util import radio_types, file_util
from src.ham.util.file_util import RadioWriter


class RadioAdditionalData:
	def __init__(self, channels, dmr_ids, digital_contacts, zones, users):
		self._channels = channels
		self._dmr_ids = dmr_ids
		self._digital_contacts = digital_contacts
		self._zones = zones
		self._users = users
		return

	def output(self, style):
		switch = {
			radio_types.DEFAULT: self._output_default,
			radio_types.BAOFENG: lambda x: False,
			radio_types.FTM400: lambda x: False,
			radio_types.D878: self._output_d878,
			radio_types.CS800: self._output_cs800,
			radio_types.D710: self._output_d710,
		}

		return switch[style](style)

	def _output_default(self, style):
		self._output_radioids_default(style)
		self._output_contacts_default(style)
		self._output_zones_default(style)
		self._output_user_default(style)

	def _output_radioids_default(self, style):
		if self._dmr_ids is None:
			logging.error(f"No DMR ids found for {style}.")
			return

		writer = open(f'out/{style}/{style}_radioid.csv', 'w+', encoding='utf-8')
		radio_id_file = csv.writer(writer, lineterminator='\n')

		headers = DmrId.create_empty()
		radio_id_file.writerow(headers.headers(style))
		for dmr_id in self._dmr_ids.values():
			radio_id_file.writerow(dmr_id.output(style))

		writer.close()
		return

	def _output_contacts_default(self, style):
		if self._digital_contacts is None:
			logging.error(f"No digital contacts found for {style}.")
			return

		writer = open(f'out/{style}/{style}_contacts.csv', 'w+', encoding='utf-8')
		dmr_contact_file = csv.writer(writer, lineterminator='\n')

		headers = DmrContact.create_empty()
		dmr_contact_file.writerow(headers.headers(style))
		for dmr_contact in self._digital_contacts.values():
			dmr_contact_file.writerow(dmr_contact.output(style))

		writer.close()

	def _output_zones_default(self, style):
		if self._zones is None:
			logging.error(f"No zones list found for {style}.")
			return

		writer = open(f'out/{style}/{style}_zone.csv', 'w+', encoding='utf-8')
		zone_file = csv.writer(writer, lineterminator='\n')

		headers = RadioZone.create_empty()
		zone_file.writerow(headers.headers(style))
		for zone in self._zones.values():
			zone_file.writerow(zone.output(style))

		writer.close()

	def _output_user_default(self, style):
		if self._users is None:
			logging.error(f"No zones list found for {style}.")
			return

		writer = open(f'out/{style}/{style}_user.csv', 'w+', encoding='utf-8')
		users_file = csv.writer(writer, lineterminator='\n')

		headers = DmrUser.create_empty()
		users_file.writerow(headers.headers(style))
		for zone in self._users.values():
			users_file.writerow(zone.output(style))

		writer.close()

	def _output_d878(self, style):
		self._output_radioids_d878(style)
		self._output_contacts_d878(style)
		self._output_zones_d878(style)
		self._output_user_d878(style)

	def _output_radioids_d878(self, style):
		logging.info(f"Writing {style} radio IDs")
		if self._dmr_ids is None:
			logging.error(f"No DMR ids found for {style}.")
			return

		radio_id_file = RadioWriter(f'out/{style}/{style}_radioid.csv', '\r\n')

		headers = DmrId.create_empty()
		radio_id_file.writerow(headers.headers(style))
		for dmr_id in self._dmr_ids.values():
			radio_id_file.writerow(dmr_id.output(style))

		radio_id_file.close()
		return

	def _output_contacts_d878(self, style):
		logging.info(f"Writing {style} contacts")
		if self._digital_contacts is None:
			logging.error(f"No digital contacts found for {style}.")
			return

		dmr_contact_file = RadioWriter(f'out/{style}/{style}_talkgroup.csv', '\r\n')

		headers = DmrContact.create_empty()
		dmr_contact_file.writerow(headers.headers(style))
		for dmr_contact in self._digital_contacts.values():
			dmr_contact_file.writerow(dmr_contact.output(style))

		dmr_contact_file.close()

	def _output_zones_d878(self, style):
		logging.info(f"Writing {style} zones")
		if self._zones is None:
			logging.error(f"No zones list found for {style}.")
			return

		zone_file = RadioWriter(f'out/{style}/{style}_zone.csv', '\r\n')

		headers = RadioZone.create_empty()
		zone_file.writerow(headers.headers(style))
		for zone in self._zones.values():
			if not zone.has_channels():
				continue
			zone_file.writerow(zone.output(style))

		zone_file.close()

	def _output_user_d878(self, style):
		logging.info(f"Writing {style} users")
		if self._users is None:
			logging.error(f"No zones list found for {style}.")
			return

		users_file = RadioWriter(f'out/{style}/{style}_digital_contacts.csv', '\n')

		headers = DmrUser.create_empty()
		users_file.writerow(headers.headers(style))

		rows_processed = 1
		for user in self._users.values():
			users_file.writerow(user.output(style))
			rows_processed += 1
			logging.debug(f"Writing user row {rows_processed}")
			if rows_processed % file_util.USER_LINE_LOG_INTERVAL == 0:
				logging.info(f"Writing user row {rows_processed}")

		users_file.close()

	def _output_cs800(self, style):
		self._output_cs800_channels(style)
		self._output_cs800_user(style)

	def _output_cs800_channels(self, style):
		logging.info(f"Writing {style} channels")
		channels_workbook = openpyxl.Workbook()
		analog_sheet = channels_workbook.create_sheet('Analog Channel', 0)
		digital_sheet = channels_workbook.create_sheet('Digital Channel', 1)
		channels_workbook.remove_sheet(channels_workbook.get_sheet_by_name('Sheet'))

		header = RadioChannelBuilder.casted(RadioChannel.create_empty(), radio_types.CS800)
		header.is_digital = lambda: False
		analog_sheet.append(header.headers(radio_types.CS800))
		header.is_digital = lambda: True
		digital_sheet.append(header.headers(radio_types.CS800))

		analog_num = 1
		digital_num = 1
		for radio_channel in self._channels.values():
			casted_channel = RadioChannelBuilder.casted(radio_channel, radio_types.CS800)

			if casted_channel.is_digital():
				digital_sheet.append(casted_channel.output(radio_types.CS800, digital_num))
				digital_num += 1
			else:
				analog_sheet.append(casted_channel.output(radio_types.CS800, analog_num))
				analog_num += 1
		channels_workbook.save(f'out/{style}/{style}_channels.xlsx')
		channels_workbook.close()
		return

	def _output_cs800_user(self, style):
		logging.info(f"Writing {style} users")
		user_workbook = openpyxl.Workbook()
		dmr_contacts_sheet = user_workbook.create_sheet('DMR_Contacts', 0)
		user_workbook.remove_sheet(user_workbook.get_sheet_by_name('Sheet'))

		headers = DmrContact.create_empty().headers(radio_types.CS800)
		dmr_contacts_sheet.append(headers)

		number = 1
		for dmr_contact in self._digital_contacts.values():
			if dmr_contact.name.fmt_val() == 'Analog':
				continue
			dmr_contact.number._fmt_val = number
			dmr_contacts_sheet.append(dmr_contact.output(radio_types.CS800))
			number += 1

		logging.info(f"Writing DMR users for {style}")
		for dmr_user in self._users.values():
			dmr_user.number._fmt_val = number
			dmr_contacts_sheet.append(dmr_user.output(radio_types.CS800))
			number += 1
			logging.debug(f"Writing user row {number}")
			if number % file_util.USER_LINE_LOG_INTERVAL == 0:
				logging.info(f"Writing user row {number}")

		logging.info("Saving workbook...")
		user_workbook.save(f'out/{style}/{style}_user.xlsx')
		logging.info("Save done.")
		user_workbook.close()
		return

	def _output_d710(self, style):
		return


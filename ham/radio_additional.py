import logging

from ham import radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId
from ham.dmr.dmr_user import DmrUser
from ham.radio_zone import RadioZone


class RadioAdditionalData:
	def __init__(self, dmr_ids, digital_contacts, zones, users):
		self.dmr_ids = dmr_ids
		self.digital_contacts = digital_contacts
		self.zones = zones
		self.users = users
		return

	def output(self, style):
		switch = {
			radio_types.DEFAULT: self._output_default,
			radio_types.BAOFENG: lambda x: False,
			radio_types.FTM400: lambda x: False,
			radio_types.D878: self._output_d878,
		}

		return switch[style](style)

	def _output_default(self, style):
		self._output_radioids_default(style)
		self._output_contacts_default(style)
		self._output_zones_default(style)
		self._output_user_default(style)

	def _output_radioids_default(self, style):
		if self.dmr_ids is None:
			logging.error(f"No DMR ids found for {style}.")
			return
		radio_id_file = open(f'out/{style}/{style}_radioid.csv', 'w+')

		headers = DmrId.create_empty()
		radio_id_file.write(headers.headers(style) + '\n')
		for dmr_id in self.dmr_ids.values():
			radio_id_file.write(dmr_id.output(style) + '\n')

		radio_id_file.close()
		return

	def _output_contacts_default(self, style):
		if self.digital_contacts is None:
			logging.error(f"No digital contacts found for {style}.")
			return

		dmr_contact_file = open(f'out/{style}/{style}_contacts.csv', 'w+')

		headers = DmrContact.create_empty()
		dmr_contact_file.write(headers.headers(style) + '\n')
		for dmr_contact in self.digital_contacts.values():
			dmr_contact_file.write(dmr_contact.output(style) + '\n')

		dmr_contact_file.close()

	def _output_zones_default(self, style):
		if self.zones is None:
			logging.error(f"No zones list found for {style}.")
			return

		zone_file = open(f'out/{style}/{style}_zone.csv', 'w+')
		headers = RadioZone.create_empty()
		zone_file.write(headers.headers(style) + '\n')
		for zone in self.zones.values():
			zone_file.write(zone.output(style) + '\n')

		zone_file.close()

	def _output_user_default(self, style):
		if self.users is None:
			logging.error(f"No zones list found for {style}.")
			return

		users_file = open(f'out/{style}/{style}_user.csv', 'w+')
		headers = DmrUser.create_empty()
		users_file.write(headers.headers(style) + '\n')
		for zone in self.users.values():
			users_file.write(zone.output(style) + '\n')

		users_file.close()

	def _output_d878(self, style):
		self._output_radioids_d878(style)
		self._output_contacts_d878(style)
		self._output_zones_d878(style)
		self._output_user_d878(style)

	def _output_radioids_d878(self, style):
		if self.dmr_ids is None:
			logging.error(f"No DMR ids found for {style}.")
			return
		radio_id_file = open(f'out/{style}/{style}_radioid.csv', 'w+')

		headers = DmrId.create_empty()
		radio_id_file.write(headers.headers(style) + '\n')
		for dmr_id in self.dmr_ids.values():
			radio_id_file.write(dmr_id.output(style) + '\n')

		radio_id_file.close()
		return

	def _output_contacts_d878(self, style):
		if self.digital_contacts is None:
			logging.error(f"No digital contacts found for {style}.")
			return

		dmr_contact_file = open(f'out/{style}/{style}_talkgroup.csv', 'w+')

		headers = DmrContact.create_empty()
		dmr_contact_file.write(headers.headers(style) + '\n')
		for dmr_contact in self.digital_contacts.values():
			dmr_contact_file.write(dmr_contact.output(style) + '\n')

		dmr_contact_file.close()

	def _output_zones_d878(self, style):
		if self.zones is None:
			logging.error(f"No zones list found for {style}.")
			return

		zone_file = open(f'out/{style}/{style}_zone.csv', 'w+')
		headers = RadioZone.create_empty()
		zone_file.write(headers.headers(style) + '\n')
		for zone in self.zones.values():
			if not zone.has_channels():
				continue
			zone_file.write(zone.output(style) + '\n')

		zone_file.close()

	def _output_user_d878(self, style):
		if self.users is None:
			logging.error(f"No zones list found for {style}.")
			return

		users_file = open(f'out/{style}/{style}_user.csv', 'w+')
		headers = DmrUser.create_empty()
		users_file.write(headers.headers(style) + '\n')
		for zone in self.users.values():
			users_file.write(zone.output(style) + '\n')

		users_file.close()


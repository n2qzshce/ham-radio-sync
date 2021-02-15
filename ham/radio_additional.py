import logging

from ham import radio_types
from ham.dmr.dmr_contact import DmrContact
from ham.dmr.dmr_id import DmrId


class RadioAdditionalData:
	def __init__(self, dmr_ids, digital_contacts):
		self.dmr_ids = dmr_ids
		self.digital_contacts = digital_contacts
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

	def _output_d878(self, style):
		self._output_radioids_d878(style)
		self._output_contacts_d878(style)

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

class RadioAdditional:
	def __init__(self, channels, dmr_ids, digital_contacts, zones, users):
		self._channels = channels
		self._dmr_ids = dmr_ids
		self._digital_contacts = digital_contacts
		self._zones = zones
		self._users = users
		self._style = None
		return

	def output(self):
		raise Exception("Base method cannot be called!")

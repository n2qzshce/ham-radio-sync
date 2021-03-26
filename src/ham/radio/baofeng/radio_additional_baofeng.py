from src.ham.radio.radio_additional import RadioAdditional


class RadioAdditionalBaofeng(RadioAdditional):
	def __init__(self, channels, dmr_ids, digital_contacts, zones, users):
		super().__init__(channels, dmr_ids, digital_contacts, zones, users)
		return

	def output(self):
		pass

from src.ham.radio.chirp.radio_additional_chirp import RadioAdditionalChirp
from src.ham.radio.cs800.radio_additional_cs800 import RadioAdditionalCs800
from src.ham.radio.d710.radio_additional_d710 import RadioAdditionalD710
from src.ham.radio.d878.radio_additional_d878 import RadioAdditionalD878
from src.ham.radio.default_radio.radio_additional_default import RadioAdditionalDefault
from src.ham.radio.ftm400.radio_additional_ftm400 import RadioAdditionalFtm400
from src.ham.radio.gpx.radio_additional_gpx import RadioAdditionalGpx
from src.ham.util import radio_types


class RadioAdditionalBuilder:
	@classmethod
	def casted(cls, radio_additional_data, style):
		switch = {
			radio_types.DEFAULT: RadioAdditionalDefault(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
			radio_types.CHIRP: RadioAdditionalChirp(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
			radio_types.FTM400_RT: RadioAdditionalFtm400(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
			radio_types.D878: RadioAdditionalD878(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
			radio_types.CS800: RadioAdditionalCs800(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
			radio_types.D710: RadioAdditionalD710(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
			radio_types.GPX: RadioAdditionalGpx(
														radio_additional_data._channels
														, radio_additional_data._dmr_ids
														, radio_additional_data._digital_contacts
														, radio_additional_data._zones
														, radio_additional_data._users
														),
		}

		return switch[style]
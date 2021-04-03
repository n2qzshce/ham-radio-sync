from src.ham.radio.chirp.radio_channel_chirp import RadioChannelChirp
from src.ham.radio.cs800.dmr_contact_cs800 import DmrContactCs800
from src.ham.radio.cs800.dmr_user_cs800 import DmrUserCs800
from src.ham.radio.cs800.radio_channel_cs800 import RadioChannelCS800
from src.ham.radio.d710.radio_channel_d710 import RadioChannelD710
from src.ham.radio.d878.dmr_contact_d878 import DmrContactD878
from src.ham.radio.d878.dmr_id_d878 import DmrIdD878
from src.ham.radio.d878.dmr_user_d878 import DmrUserD878
from src.ham.radio.d878.radio_channel_d878 import RadioChannelD878
from src.ham.radio.d878.radio_zone_d878 import RadioZoneD878
from src.ham.radio.default_radio.dmr_contact_default import DmrContactDefault
from src.ham.radio.default_radio.dmr_id_default import DmrIdDefault
from src.ham.radio.default_radio.dmr_user_default import DmrUserDefault
from src.ham.radio.default_radio.radio_channel_default import RadioChannelDefault
from src.ham.radio.default_radio.radio_zone_default import RadioZoneDefault
from src.ham.radio.ftm400.radio_channel_ftm400 import RadioChannelFtm400
from src.ham.util import radio_types


class RadioChannelBuilder:
	@classmethod
	def casted(cls, radio_channel, style):
		switch = {
			radio_types.DEFAULT: RadioChannelDefault(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.CHIRP: RadioChannelChirp(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.FTM400_RT: RadioChannelFtm400(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.D878: RadioChannelD878(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.CS800: RadioChannelCS800(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.D710: RadioChannelD710(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
		}

		return switch[style]


class DmrContactBuilder:
	@classmethod
	def casted(cls, radio_channel, style):
		switch = {
			radio_types.DEFAULT: DmrContactDefault(radio_channel.cols),
			radio_types.D878: DmrContactD878(radio_channel.cols),
			radio_types.CS800: DmrContactCs800(radio_channel.cols),
		}

		return switch[style]


class DmrIdBuilder:
	@classmethod
	def casted(cls, radio_channel, style):
		switch = {
			radio_types.DEFAULT: DmrIdDefault(radio_channel.cols),
			radio_types.D878: DmrIdD878(radio_channel.cols),
		}

		return switch[style]


class DmrUserBuilder:
	@classmethod
	def casted(cls, cols, style):
		switch = {
			radio_types.DEFAULT: DmrUserDefault(cols),
			radio_types.D878: DmrUserD878(cols),
			radio_types.CS800: DmrUserCs800(cols),
		}

		return switch[style]


class RadioZoneBuilder:
	@classmethod
	def casted(cls, cols, associated_channels, style):
		switch = {
			radio_types.DEFAULT: RadioZoneDefault(cols),
			radio_types.D878: RadioZoneD878(cols)
		}
		result = switch[style]
		result._associated_channels = associated_channels
		return result

from src.ham.radio.channel.radio_channel_baofeng import RadioChannelBaofeng
from src.ham.radio.channel.radio_channel_cs800 import RadioChannelCS800
from src.ham.radio.channel.radio_channel_d710 import RadioChannelD710
from src.ham.radio.channel.radio_channel_d878 import RadioChannelD878
from src.ham.radio.channel.radio_channel_default import RadioChannelDefault
from src.ham.radio.channel.radio_channel_ftm400 import RadioChannelFtm400
from src.ham.util import radio_types


class RadioChannelBuilder:
	@classmethod
	def casted(cls, radio_channel, style):
		switch = {
			radio_types.DEFAULT: RadioChannelDefault(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.BAOFENG: RadioChannelBaofeng(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.FTM400: RadioChannelFtm400(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.D878: RadioChannelD878(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.CS800: RadioChannelCS800(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
			radio_types.D710: RadioChannelD710(radio_channel.cols, radio_channel.digital_contacts, radio_channel.dmr_ids),
		}

		return switch[style]
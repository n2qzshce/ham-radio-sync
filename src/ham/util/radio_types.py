DEFAULT = 'default'
BAOFENG = 'baofeng'
FTM400 = 'ftm400'
D710 = 'dm710'
D878 = 'd878'
CS800 = 'cs800'


def supports_dmr(radio_type):
	switch = {
		DEFAULT: True,
		BAOFENG: False,
		FTM400: False,
		D878: True,
		CS800: True,
		D710: False,
	}

	return switch[radio_type]


def pretty_name(radio_type):
	switch = {
		DEFAULT: 'Default',
		BAOFENG: 'Baofeng Radios',
		FTM400: 'Yaesu FTM-400',
		D878: 'Anytone D878',
		CS800: 'Connect Systems CS800',
		D710: 'Kenwood D710 Series',
	}

	return switch[radio_type]


def radio_choices():
	return [
		DEFAULT,
		BAOFENG,
		FTM400,
		D710,
		D878,
		CS800,
	]

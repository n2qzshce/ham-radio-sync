DEFAULT = 'default'
BAOFENG = 'baofeng'
FTM400 = 'ftm400'
D878 = 'd878'
CS800 = 'cs800'


def supports_dmr(radio_type):
	switch = {
		DEFAULT: True,
		BAOFENG: False,
		FTM400: False,
		D878: True,
		CS800: True,
	}

	return switch[radio_type]


def pretty_name(radio_type):
	switch = {
		DEFAULT: 'Default',
		BAOFENG: 'Baofeng Radios',
		FTM400: 'Yaesu FTM-400',
		D878: 'Anytone D878',
		CS800: 'Connect Systems CS800',
	}

	return switch[radio_type]

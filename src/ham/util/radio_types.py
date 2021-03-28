DEFAULT = 'default'
CHIRP = 'chirp'
FTM400_RT = 'ftm400'
D710 = 'dm710'
D878 = 'd878'
CS800 = 'cs800'


def supports_dmr(radio_type):
	switch = {
		DEFAULT: True,
		CHIRP: False,
		FTM400_RT: False,
		D878: True,
		CS800: True,
		D710: False,
	}

	return switch[radio_type]


def pretty_name(radio_type):
	switch = {
		DEFAULT: 'Default',
		CHIRP: 'CHiRP-Compatible Radios via CHiRP',
		FTM400_RT: 'Yaesu FTM-400 via RT Systems',
		D878: 'Anytone D878 via D878',
		CS800: 'Connect Systems CS800 via CPI',
		D710: 'Kenwood 71/710 Series via MCP2',
	}

	return switch[radio_type]


def radio_choices():
	return [
		DEFAULT,
		CHIRP,
		FTM400_RT,
		D710,
		D878,
		CS800,
	]

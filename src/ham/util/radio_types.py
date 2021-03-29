DEFAULT = 'default'
CHIRP = 'chirp'
FTM400_RT = 'ftm400'
D710 = 'dm710'
D878 = 'd878'
CS800 = 'cs800'

compatible_radios = {
	DEFAULT: 'Ham Radio Sync App',
	CHIRP: 'Baofeng handhelds, etc. See CHiRP supported list for more',
	FTM400_RT: 'Yaesu FTM-400DR, FTM-400XDR',
	D710: 'Kenwood TM-V71A, TM-V71E, TM-D710A, TM-D710E, RC-D710',
	D878: 'Anytone 878, 868, 578',
	CS800: 'Connect Systems CS800, CS800D',
}


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
		CHIRP: 'CHiRP-Compatible (CHiRP)',
		FTM400_RT: 'Yaesu FTM-400 (RT Systems)',
		D878: 'Anytone D878 (D878)',
		CS800: 'Connect Systems CS800 (CPI)',
		D710: 'Kenwood 71/710 Series (MCP2)',
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

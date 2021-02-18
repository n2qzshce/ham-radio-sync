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

DEFAULT = 'default'
BAOFENG = 'baofeng'
FTM400 = 'ftm400'
D878 = 'd878'


def supports_dmr(radio_type):
	switch = {
		DEFAULT: True,
		BAOFENG: False,
		FTM400: False,
		D878: True,
	}

	return switch[radio_type]

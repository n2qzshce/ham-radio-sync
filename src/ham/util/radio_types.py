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


dcs_codes_inverses = {
	23: 47,
	25: 244,
	26: 464,
	31: 627,
	32: 51,
	36: 172,
	43: 445,
	47: 23,
	51: 32,
	53: 452,
	54: 413,
	65: 271,
	71: 306,
	72: 245,
	73: 506,
	74: 174,
	114: 712,
	115: 152,
	116: 754,
	122: 225,
	125: 365,
	131: 364,
	132: 546,
	134: 223,
	143: 412,
	145: 274,
	152: 115,
	155: 731,
	156: 265,
	162: 503,
	165: 251,
	172: 36,
	174: 74,
	205: 263,
	212: 356,
	223: 134,
	225: 122,
	226: 411,
	243: 351,
	244: 25,
	245: 72,
	246: 523,
	251: 165,
	252: 462,
	255: 446,
	261: 732,
	263: 205,
	265: 156,
	266: 454,
	271: 65,
	274: 145,
	306: 71,
	311: 664,
	315: 423,
	325: 526,
	331: 465,
	332: 455,
	343: 532,
	346: 612,
	351: 243,
	356: 212,
	364: 131,
	365: 125,
	371: 734,
	411: 226,
	412: 143,
	413: 54,
	423: 315,
	431: 723,
	432: 516,
	445: 43,
	446: 255,
	452: 53,
	454: 266,
	455: 332,
	462: 252,
	464: 26,
	465: 331,
	466: 662,
	503: 162,
	506: 73,
	516: 432,
	523: 246,
	526: 325,
	532: 343,
	546: 132,
	565: 703,
	606: 631,
	612: 346,
	624: 632,
	627: 31,
	631: 606,
	632: 624,
	654: 743,
	662: 466,
	664: 311,
	703: 565,
	712: 114,
	723: 431,
	731: 155,
	732: 261,
	734: 371,
	743: 654,
	754: 116,
}
import argparse

def main():
	parser = argparse.ArgumentParser(
		prog='Ham Radio channel wizard',
		description='''Convert a ham channel list to various radio formats. All of these options can be chained
					to run multiple steps simultaneously.''')
	parser.add_argument(
		'wizard',
		nargs='?',
		default=False,
	)

	arg_values = parser.parse_args()
	run_wizard = arg_values.wizard is not False

	return

main()
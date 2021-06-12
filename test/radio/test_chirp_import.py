import logging

from src.ham.radio.radio_importer import RadioImporter
from src.ham.util import radio_types
from src.ham.util.path_manager import PathManager
from test.base_test_setup import BaseTestSetup


class TestChirpImport(BaseTestSetup):
	def setUp(self):
		super().setUp()
		self.importer = RadioImporter()

	def test_imports_simplex(self):
		f = open('in/import_chirp.csv', 'w+')
		f.write("""Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
0,NATL 2M,146.520000,,0.000000,,67.0,67.0,023,NN,FM,5.00,,,,,,""")
		f.close()
		PathManager.set_import_file('in/import_chirp.csv', radio_types.CHIRP)

		channel = self.importer.run_import(radio_types.CHIRP, 'in/import_chirp.csv')[0]
		self.assertEqual('NATL 2M', channel.name.fmt_val())
		self.assertEqual('NATL 2M', channel.medium_name.fmt_val())
		self.assertEqual('NATL 2M', channel.short_name.fmt_val())
		self.assertEqual(146.52, channel.rx_freq.fmt_val())
		self.assertIsNone(channel.rx_ctcss.fmt_val())
		self.assertIsNone(channel.rx_dcs.fmt_val())
		self.assertIsNone(channel.rx_dcs_invert.fmt_val())
		self.assertEqual('High', channel.tx_power.fmt_val())
		self.assertIsNone(channel.tx_offset.fmt_val())
		self.assertIsNone(channel.tx_ctcss.fmt_val())
		self.assertIsNone(channel.tx_dcs.fmt_val())
		self.assertIsNone(channel.tx_dcs_invert.fmt_val())
		self.assertIsNone(channel.digital_timeslot.fmt_val())
		self.assertIsNone(channel.digital_color.fmt_val())
		self.assertIsNone(channel.digital_contact_id.fmt_val())
		self.assertIsNone(channel.latitude.fmt_val())
		self.assertIsNone(channel.longitude.fmt_val())

	def test_imports_ctcs_repeater(self):
		f = open('in/import_chirp.csv', 'w+')
		f.write("""Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
0,RPTR1,146.410000,-,0.600000,Tone,88.5,67.0,023,NN,FM,5.00,,,,,,""")
		f.close()
		PathManager.set_import_file('in/import_chirp.csv', radio_types.CHIRP)

		channel = self.importer.run_import(radio_types.CHIRP, 'in/import_chirp.csv')[0]
		self.assertEqual('RPTR1', channel.name.fmt_val())
		self.assertEqual('RPTR1', channel.medium_name.fmt_val())
		self.assertEqual('RPTR1', channel.short_name.fmt_val())
		self.assertEqual(146.410, channel.rx_freq.fmt_val())
		self.assertIsNone(channel.rx_ctcss.fmt_val())
		self.assertIsNone(channel.rx_dcs.fmt_val())
		self.assertIsNone(channel.rx_dcs_invert.fmt_val())
		self.assertEqual('High', channel.tx_power.fmt_val())
		self.assertEqual(-0.6, channel.tx_offset.fmt_val())
		self.assertEqual(88.5, channel.tx_ctcss.fmt_val())
		self.assertIsNone(channel.tx_dcs.fmt_val())
		self.assertIsNone(channel.tx_dcs_invert.fmt_val())
		self.assertIsNone(channel.digital_timeslot.fmt_val())
		self.assertIsNone(channel.digital_color.fmt_val())
		self.assertIsNone(channel.digital_contact_id.fmt_val())
		self.assertIsNone(channel.latitude.fmt_val())
		self.assertIsNone(channel.longitude.fmt_val())

	def test_imports_tone_repeater(self):
		f = open('in/import_chirp.csv', 'w+')
		f.write("""Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
0,TSQLRP,449.825000,-,5.000000,TSQL,103.5,103.5,023,NN,FM,5.00,,,,,,
0,DCSRPT,447.075000,-,5.000000,DTCS,67.0,67.0,165,NN,FM,5.00,,,,,,""")
		f.close()
		PathManager.set_import_file('in/import_chirp.csv', radio_types.CHIRP)

		channel = self.importer.run_import(radio_types.CHIRP, 'in/import_chirp.csv')[0]
		self.assertEqual('TSQLRP', channel.name.fmt_val())
		self.assertEqual('TSQLRP', channel.medium_name.fmt_val())
		self.assertEqual('TSQLRP', channel.short_name.fmt_val())
		self.assertEqual(449.825, channel.rx_freq.fmt_val())
		self.assertEqual(103.5, channel.rx_ctcss.fmt_val())
		self.assertIsNone(channel.rx_dcs.fmt_val())
		self.assertIsNone(channel.rx_dcs_invert.fmt_val())
		self.assertEqual('High', channel.tx_power.fmt_val())
		self.assertEqual(-5, channel.tx_offset.fmt_val())
		self.assertEqual(103.5, channel.tx_ctcss.fmt_val())
		self.assertIsNone(channel.tx_dcs.fmt_val())
		self.assertIsNone(channel.tx_dcs_invert.fmt_val())
		self.assertIsNone(channel.digital_timeslot.fmt_val())
		self.assertIsNone(channel.digital_color.fmt_val())
		self.assertIsNone(channel.digital_contact_id.fmt_val())
		self.assertIsNone(channel.latitude.fmt_val())
		self.assertIsNone(channel.longitude.fmt_val())

	def test_imports_dcs_repeater(self):
		f = open('in/import_chirp.csv', 'w+')
		f.write("""Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
0,DCSRPT,447.075000,-,5.000000,DTCS,67.0,67.0,165,NN,FM,5.00,,,,,,""")
		f.close()

		channel = self.importer.run_import(radio_types.CHIRP, 'in/import_chirp.csv')[0]
		self.assertEqual('DCSRPT', channel.name.fmt_val())
		self.assertEqual('DCSRPT', channel.medium_name.fmt_val())
		self.assertEqual('DCSRPT', channel.short_name.fmt_val())
		self.assertEqual(447.075, channel.rx_freq.fmt_val())
		self.assertIsNone(channel.rx_ctcss.fmt_val())
		self.assertEqual(165, channel.rx_dcs.fmt_val())
		self.assertIsNone(channel.rx_dcs_invert.fmt_val())
		self.assertEqual('High', channel.tx_power.fmt_val())
		self.assertEqual(-5, channel.tx_offset.fmt_val())
		self.assertIsNone(channel.tx_ctcss.fmt_val())
		self.assertEqual(165, channel.tx_dcs.fmt_val())
		self.assertIsNone(channel.tx_dcs_invert.fmt_val())
		self.assertIsNone(channel.digital_timeslot.fmt_val())
		self.assertIsNone(channel.digital_color.fmt_val())
		self.assertIsNone(channel.digital_contact_id.fmt_val())
		self.assertIsNone(channel.latitude.fmt_val())
		self.assertIsNone(channel.longitude.fmt_val())

	def test_exception_on_invalid(self):
		f = open('in/import_chirp.csv', 'w+')
		f.write("""Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
0,RPTR1,the bad value is here,-,0.600000,Tone,88.5,67.0,023,NN,FM,5.00,,,,,,""")
		f.close()

		with self.assertRaises(BaseException) as e:
			channel = self.importer.run_import(radio_types.CHIRP, 'in/import_chirp.csv')[0]
			logging.info(f'Output channel: {channel}')

		self.assertEqual('Cannot import file.', e.exception.args[0])


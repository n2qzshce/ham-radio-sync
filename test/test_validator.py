import logging

from src.ham.radio.dmr_contact import DmrContact
from src.ham.util.file_util import FileUtil
from src.ham.util.validator import Validator
from test.base_test_setup import BaseTestSetup


class ValidatorTest(BaseTestSetup):
	def setUp(self):
		self.validator = Validator()
		self.validator.flush_names()
		logging.getLogger().setLevel(logging.CRITICAL)
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')

		FileUtil.safe_create_dir('in')
		FileUtil.safe_create_dir('out')

	def test_validate_no_files_exist(self):
		errors = Validator.validate_files_exist()
		self.assertEqual(5, len(errors))

	def test_validate_files_exist(self):
		files = ["in/input.csv", "in/digital_contacts.csv", "in/dmr_id.csv", 'in/zones.csv', 'in/user.csv']
		for filename in files:
			f = FileUtil.open_file(filename, 'w+')
			f.close()
		errors = Validator.validate_files_exist()
		self.assertEqual(0, len(errors))

	def test_only_some_files_exist(self):
		f = FileUtil.open_file("in/input.csv", 'w+')
		f.close()
		errors = Validator.validate_files_exist()
		self.assertEqual(4, len(errors))

	def test_validate_radio_channel_name_dupe(self):
		cols = dict()
		cols['number'] = '1'
		cols['name'] = 'National 2m'
		cols['medium_name'] = 'Natl 2m'
		cols['short_name'] = 'NATL 2M'
		cols['zone_id'] = ''
		cols['rx_freq'] = '146.52'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = ''
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = ''
		cols['tx_offset'] = ''
		cols['tx_ctcss'] = ''
		cols['tx_dcs'] = ''
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		errors = self.validator.validate_radio_channel(cols, 1, "FILE_NO_EXIST_UNITTEST", )
		self.assertEqual(len(errors), 0)
		errors = self.validator.validate_radio_channel(cols, 2, "FILE_NO_EXIST_UNITTEST", )
		self.assertEqual(len(errors), 3)

		short_found = False
		medium_found = False
		long_found = False
		for err in errors:
			short_found = err.args[0].find('Collision in short_name') or short_found
			medium_found = err.args[0].find('Collision in medium_name') or medium_found
			long_found = err.args[0].find('Collision in name') or long_found

		self.assertTrue(short_found)
		self.assertTrue(medium_found)
		self.assertTrue(long_found)

	def test_validate_missing_contact(self):
		radio_cols = dict()
		radio_cols['number'] = '1'
		radio_cols['name'] = 'Test channel'
		radio_cols['medium_name'] = 'TestChan'
		radio_cols['short_name'] = 'TestChn'
		radio_cols['zone_id'] = ''
		radio_cols['rx_freq'] = '146.52'
		radio_cols['rx_ctcss'] = ''
		radio_cols['rx_dcs'] = ''
		radio_cols['rx_dcs_invert'] = ''
		radio_cols['tx_power'] = ''
		radio_cols['tx_offset'] = '0.6'
		radio_cols['tx_ctcss'] = ''
		radio_cols['tx_dcs'] = ''
		radio_cols['tx_dcs_invert'] = ''
		radio_cols['digital_timeslot'] = '1'
		radio_cols['digital_color'] = '2'
		radio_cols['digital_contact_id'] = '314'

		digital_contact_cols = dict()
		digital_contact_cols['number'] = '1'
		digital_contact_cols['digital_id'] = '314'
		digital_contact_cols['name'] = 'Digi Contact'
		digital_contact_cols['call_type'] = 'Group'
		digital_contacts = {
			314: DmrContact(digital_contact_cols),
		}
		errors = self.validator.validate_radio_channel(radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', digital_contacts)
		self.assertEqual(len(errors), 0)
		self.validator.flush_names()

		errors = self.validator.validate_radio_channel(radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Cannot find digital contact')
		self.assertEqual(found, 0)



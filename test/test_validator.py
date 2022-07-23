import logging

from src.ham.radio.dmr_contact import DmrContact
from src.ham.radio.radio_zone import RadioZone
from src.ham.util.file_util import FileUtil
from src.ham.util.path_manager import PathManager
from src.ham.util.validator import Validator
from test.base_test_setup import BaseTestSetup


class ValidatorTest(BaseTestSetup):
	def setUp(self):
		super().setUp()
		self.validator = Validator()
		self.validator.flush_names()
		logging.getLogger().setLevel(logging.CRITICAL)
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')
		FileUtil.safe_create_dir('in')
		FileUtil.safe_create_dir('out')

		cols = dict()
		cols['name'] = 'National 2m'
		cols['medium_name'] = 'Natl 2m'
		cols['short_name'] = 'NATL 2M'
		cols['zone_id'] = ''
		cols['rx_freq'] = '146.52'
		cols['rx_ctcss'] = ''
		cols['rx_dcs'] = ''
		cols['rx_dcs_invert'] = ''
		cols['tx_power'] = 'High'
		cols['tx_offset'] = ''
		cols['tx_ctcss'] = ''
		cols['tx_dcs'] = ''
		cols['tx_dcs_invert'] = ''
		cols['digital_timeslot'] = ''
		cols['digital_color'] = ''
		cols['digital_contact_id'] = ''
		cols['latitude'] = ''
		cols['longitude'] = ''
		self.radio_cols = cols

	def test_validate_no_files_exist(self):
		errors = Validator.validate_files_exist()
		self.assertEqual(5, len(errors))

	def test_validate_files_exist(self):
		files = ['input.csv', 'digital_contacts.csv', 'dmr_id.csv', 'zones.csv', 'user.csv']
		for filename in files:
			f = PathManager.open_input_file(filename, 'w+')
			f.close()
		errors = Validator.validate_files_exist()
		self.assertEqual(0, len(errors))

	def test_only_some_files_exist(self):
		f = PathManager.open_input_file('input.csv', 'w+')
		f.close()
		errors = Validator.validate_files_exist()
		self.assertEqual(4, len(errors))

	def test_validate_radio_channel_name_dupe(self):
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, {})
		self.assertEqual(len(errors), 0)
		errors = self.validator.validate_radio_channel(self.radio_cols, 2, 'FILE_NO_EXIST_UNITTEST', {}, {})
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
		radio_cols['tx_power'] = 'High'
		radio_cols['tx_offset'] = '0.6'
		radio_cols['tx_ctcss'] = ''
		radio_cols['tx_dcs'] = ''
		radio_cols['tx_dcs_invert'] = ''
		radio_cols['digital_timeslot'] = '1'
		radio_cols['digital_color'] = '2'
		radio_cols['digital_contact_id'] = '314'
		radio_cols['latitude'] = ''
		radio_cols['longitude'] = ''

		digital_contact_cols = dict()
		digital_contact_cols['number'] = '1'
		digital_contact_cols['digital_id'] = '314'
		digital_contact_cols['name'] = 'Digi Contact'
		digital_contact_cols['call_type'] = 'Group'
		digital_contacts = {
			314: DmrContact(digital_contact_cols),
		}
		errors = self.validator.validate_radio_channel(radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', digital_contacts, {})
		self.assertEqual(len(errors), 0)
		self.validator.flush_names()

		errors = self.validator.validate_radio_channel(radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Cannot find digital contact')
		self.assertEqual(found, 0)

	def test_ignore_extra_column(self):
		self.radio_cols['foo'] = '1'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, {})
		self.assertEqual(len(errors), 0)

	def test_validate_tx_power(self):
		self.radio_cols['tx_power'] = 'mega'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Transmit power (`tx_power`) invalid')
		self.assertEqual(found, 0)

	def test_validate_tx_power_not_present(self):
		self.radio_cols['tx_power'] = ''
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Transmit power (`tx_power`) invalid')
		self.assertEqual(found, 0)

	def test_validate_zone_not_present(self):
		self.radio_cols['zone_id'] = '1'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Zone ID not found:')
		self.assertEqual(found, 0)

	def test_validate_zone_present(self):
		self.radio_cols['zone_id'] = '1'
		zone = RadioZone({
			'number': 1,
			'name': 'Zone 1',
		})
		zones = {1: zone}
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'FILE_NO_EXIST_UNITTEST', {}, zones)
		self.assertEqual(len(errors), 0)

	def test_validate_lat_long_present(self):
		self.radio_cols['latitude'] = '0.0'
		self.radio_cols['longitude'] = '0.0'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 0)

	def test_validate_lat_long_not_present(self):
		self.radio_cols['latitude'] = ''
		self.radio_cols['longitude'] = ''
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 0)

	def test_validate_lat_only_present(self):
		self.radio_cols['latitude'] = '0.0'
		self.radio_cols['longitude'] = ''
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Only one of latitude or longitude provided')
		self.assertEqual(found, 0)

	def test_validate_long_only_present(self):
		self.radio_cols['latitude'] = ''
		self.radio_cols['longitude'] = '0.0'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Only one of latitude or longitude provided')
		self.assertEqual(found, 0)

	def test_validate_bad_lat(self):
		self.radio_cols['latitude'] = '-91.0'
		self.radio_cols['longitude'] = '0.0'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Latitude must be between')
		self.assertEqual(found, 0)

	def test_validate_bad_long(self):
		self.radio_cols['latitude'] = '0.0'
		self.radio_cols['longitude'] = '-181.0'
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)
		found = errors[0].args[0].find('Longitude must be between')
		self.assertEqual(found, 0)

	def test_name_missing(self):
		self.radio_cols['name'] = ''
		errors = self.validator.validate_radio_channel(self.radio_cols, 1, 'LAT_LONG_UNITTEST', {}, {})
		self.assertEqual(len(errors), 1)


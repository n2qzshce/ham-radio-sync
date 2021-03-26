from src.ham.util.file_util import FileUtil
from src.ham.util.validator import Validator
from test.base_test_setup import BaseTestSetup


class ValidatorTest(BaseTestSetup):
	def setUp(self):
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')

		FileUtil.safe_create_dir('in')
		FileUtil.safe_create_dir('out')

	def test_validate_no_files_exist(self):
		errors = Validator.validate_files_exist()
		self.assertEquals(5, len(errors))

	def test_validate_files_exist(self):
		files = ["in/input.csv", "in/digital_contacts.csv", "in/dmr_id.csv", 'in/zones.csv', 'in/user.csv']
		for filename in files:
			f = FileUtil.open_file(filename, 'w+')
			f.close()
		errors = Validator.validate_files_exist()
		self.assertEquals(0, len(errors))

	def test_only_some_files_exist(self):
		f = FileUtil.open_file("in/input.csv", 'w+')
		f.close()
		errors = Validator.validate_files_exist()
		self.assertEquals(4, len(errors))

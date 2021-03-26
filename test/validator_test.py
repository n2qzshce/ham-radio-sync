import unittest

from src.ham.util.file_util import FileUtil


class ValidatorTest(unittest.TestCase):
	def setUp(self):
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')

	def test_validate_files_exist(self):
		self.assertTrue(True)
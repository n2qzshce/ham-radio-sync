import logging
import os
import shutil

from src.ham.migration.migration_manager import MigrationManager
from src.ham.util.file_util import FileUtil
from test.base_test_setup import BaseTestSetup


class FileUtilTest(BaseTestSetup):
	def setUp(self):
		logging.getLogger().setLevel(logging.ERROR)
		try:
			shutil.rmtree('./in')
		except Exception:
			pass

		try:
			shutil.rmtree('./out')
		except Exception:
			pass

		try:
			shutil.rmtree('./rm_test')
		except Exception:
			pass

		self.manager = MigrationManager()

	def test_create_dir(self):
		self.assertFalse(os.path.exists('./in'))
		FileUtil.safe_create_dir('./in')
		self.assertTrue(os.path.exists('./in'))

	def test_no_exception(self):
		self.assertFalse(os.path.exists('./in'))
		FileUtil.safe_create_dir('./in')
		FileUtil.safe_create_dir('./in')
		self.assertTrue(os.path.exists('./in'))

	def test_delete_dir(self):
		os.mkdir('del_test')
		self.assertTrue(os.path.exists('del_test'))
		FileUtil.safe_delete_dir('del_test')
		self.assertFalse(os.path.exists('del_test'))

	def test_delete_no_exception(self):
		os.mkdir('del_test')
		self.assertTrue(os.path.exists('del_test'))
		FileUtil.safe_delete_dir('del_test')
		FileUtil.safe_delete_dir('del_test')
		self.assertFalse(os.path.exists('del_test'))

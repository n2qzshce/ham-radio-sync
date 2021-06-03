import logging
import os

from src.ham.migration.migration_manager import MigrationManager
from src.ham.util.file_util import FileUtil
from src.ham.util.path_manager import PathManager
from test.base_test_setup import BaseTestSetup


class PathManagerTest(BaseTestSetup):
	def setUp(self):
		super(PathManagerTest, self).setUp()
		logging.getLogger().setLevel(logging.ERROR)
		FileUtil.safe_delete_dir('./in')
		FileUtil.safe_delete_dir('./out')
		FileUtil.safe_delete_dir('./whoa_different')
		os.mkdir('./in')
		os.mkdir('./out')
		self.manager = MigrationManager()

	def test_path_manager(self):
		w = PathManager.open_input_file('x.tst', 'w+')
		w.write('test success')
		w.close()
		f = open('./in/x.tst', 'r')
		line = f.readline()
		self.assertEqual(line, 'test success')

	def test_sets_different_path(self):
		os.mkdir('./whoa_different')
		PathManager.set_input_path('whoa_different')
		w = PathManager.open_input_file('x.tst', 'w+')
		w.write('different test success')
		w.close()
		f = open('./whoa_different/x.tst', 'r')
		line = f.readline()
		f.close()
		self.assertEqual(line, 'different test success')

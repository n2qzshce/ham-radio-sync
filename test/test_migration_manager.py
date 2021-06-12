import logging
import os
from csv import DictReader

from src.ham.migration.migration_manager import MigrationManager
from src.ham.util.file_util import FileUtil
from src.ham.util.path_manager import PathManager
from test.base_test_setup import BaseTestSetup


class MigrationTest(BaseTestSetup):
	def setUp(self):
		super().setUp()
		logging.getLogger().setLevel(logging.ERROR)
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')
		self.manager = MigrationManager()

	def test_migration_one(self):
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')
		self.manager._migrate_one()

		self.assertTrue(os.path.exists('in'))
		self.assertTrue(os.path.exists('out'))

	def test_migration_two(self):
		self.manager._migrate_one()

		self.assertFalse(os.path.exists('in/input.csv'))
		self.assertFalse(os.path.exists('in/digital_contacts.csv'))
		self.assertFalse(os.path.exists('in/zones.csv'))
		self.assertFalse(os.path.exists('in/user.csv'))

		self.manager._migrate_two()

		self.assertTrue(os.path.exists('in/input.csv'))
		self.assertTrue(os.path.exists('in/digital_contacts.csv'))
		self.assertTrue(os.path.exists('in/zones.csv'))
		self.assertTrue(os.path.exists('in/user.csv'))

	def test_migration_three(self):
		self.manager._migrate_one()
		self.manager._migrate_two()
		self.manager._migrate_three()

		f = PathManager._open_file('in/input.csv', 'r')
		first_line = f.readline()
		self.assertEqual(
							'number,'
							'name,'
							'medium_'
							'name,'
							'short_'
							'name,zone_id,'
							'rx_freq,'
							'rx_ctcss,'
							'rx_dcs,rx_'
							'dcs_invert,'
							'tx_power,'
							'tx_offset,'
							'tx_ctcss,'
							'tx_dcs,'
							'tx_dcs_invert,'
							'digital_timeslot,'
							'digital_color,'
							'digital_contact_id\n', first_line)
		next_line = f.readline()
		self.assertEqual('', next_line)
		f.close()

	def test_three_does_not_stomp(self):
		logging.getLogger().setLevel(logging.CRITICAL)
		self.manager._migrate_one()
		self.manager._migrate_two()

		f = PathManager.open_input_file('input.csv', 'w+')
		f.write('foo\nspecial')
		f.close()

		self.manager._migrate_three()

		f = PathManager.open_input_file('input.csv.bak', 'r')
		contents = f.read()
		self.assertEqual('foo\nspecial', contents)
		f.close()

		f = PathManager.open_input_file('input.csv', 'r')
		dict_reader = DictReader(f)
		first_row = dict_reader.__next__()
		self.assertTrue('foo' in first_row.keys())
		self.assertEqual(first_row['foo'], 'special')
		f.close()

	def test_remove_backups(self):
		self.manager._migrate_one()
		self.manager._migrate_two()
		self.manager._migrate_three()

		self.assertTrue(os.path.exists('in/input.csv.bak'))

		self.manager.remove_backups()

		self.assertFalse(os.path.exists('in/input.csv.bak'))

	def test_migrate_with_no_files(self):
		self.assertFalse(os.path.exists('in'))
		self.assertFalse(os.path.exists('out'))
		self.manager.migrate()

		self.assertTrue(True)

	def test_migrate_four(self):
		self.manager._migrate_one()
		self.manager._migrate_two()
		self.manager._migrate_three()
		self.manager._migrate_four()

		f = PathManager.open_input_file('input.csv', 'r')
		dict_reader = DictReader(f)
		self.assertFalse('number' in dict_reader.fieldnames)
		f.close()

	def test_migrate_five(self):
		self.manager._migrate_one()
		self.manager._migrate_two()
		self.manager._migrate_three()
		self.manager._migrate_four()
		self.manager._migrate_five()

		f = PathManager.open_input_file('input.csv', 'r')
		dict_reader = DictReader(f)
		self.assertTrue('latitude' in dict_reader.fieldnames)
		self.assertTrue('longitude' in dict_reader.fieldnames)
		f.close()
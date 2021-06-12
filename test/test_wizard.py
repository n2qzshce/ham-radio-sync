import os

from src.ham.radio_generator import RadioGenerator
from src.ham.util import radio_types
from src.ham.util.file_util import FileUtil
from src.ham.wizard import Wizard
from test.base_test_setup import BaseTestSetup


class WizardTest(BaseTestSetup):
	wizard = None

	def setUp(self):
		super().setUp()
		FileUtil.safe_delete_dir('in')
		FileUtil.safe_delete_dir('out')
		self.wizard = Wizard()

	def test_wizard_runs_successfully(self):
		self.assertFalse(os.path.exists('./in'))
		self.assertFalse(os.path.exists('./out'))

		self.wizard.bootstrap()

		self.assertTrue(os.path.exists('./in'))
		self.assertTrue(os.path.exists('./in/digital_contacts.csv'))
		self.assertTrue(os.path.exists('./in/dmr_id.csv'))
		self.assertTrue(os.path.exists('./in/input.csv'))
		self.assertTrue(os.path.exists('./in/user.csv'))
		self.assertTrue(os.path.exists('./in/zones.csv'))
		self.assertTrue(os.path.exists('./out'))

	def test_create_files_parseable(self):
		self.wizard.bootstrap()
		radio_generator = RadioGenerator([radio_types.DEFAULT])
		result = radio_generator.generate_all_declared()

		self.assertTrue(result)
		self.assertTrue(os.path.exists('./out/default/default_channels.csv'))
		self.assertTrue(os.path.exists('./out/default/default_contacts.csv'))
		self.assertTrue(os.path.exists('./out/default/default_radioid.csv'))
		self.assertTrue(os.path.exists('./out/default/default_user.csv'))
		self.assertTrue(os.path.exists('./out/default/default_zone.csv'))


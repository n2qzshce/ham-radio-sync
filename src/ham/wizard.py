import logging

from src.ham.radio.default_radio.dmr_contact_default import DmrContactDefault
from src.ham.radio.default_radio.dmr_id_default import DmrIdDefault
from src.ham.radio.default_radio.dmr_user_default import DmrUserDefault
from src.ham.radio.default_radio.radio_channel_default import RadioChannelDefault
from src.ham.radio.default_radio.radio_zone_default import RadioZoneDefault
from src.ham.radio.radio_casted_builder import RadioChannelBuilder
from src.ham.util import radio_types
from src.ham.util.file_util import FileUtil, RadioWriter
from src.ham.util.path_manager import PathManager


class Wizard(object):
	_first_cols = ''

	def bootstrap(self):
		self._create_input()
		self._create_output()
		abspath = PathManager.get_input_path()
		logging.info(f'''Wizard is complete! You may now open `input.csv` and add your radio channels.
				Input CSVs are located in `{abspath}`
				What each file does:
					input.csv: your radio channels. For best results, ONLY FILL OUT THE COLUMNS YOU NEED
					zones.csv: preset group that you would like your channel in (if radio supports multiple zones)
				DMR-ONLY FILES safe to ignore for analog radios:
					digital_contacts.csv: DMR contact IDs (e.g. Talkgroups)
					dmr_id.csv: Set your DMR id (from radioid.net)

				Be sure to check the 'help' menu for more guidance!
				
				Sample data has been added to each file as an example.''')

	def _create_input(self):
		FileUtil.safe_create_dir(PathManager.get_input_path())
		create_files = {
			'channels': self._create_channel_file,
			'digital_contacts': self._create_dmr_data,
			'zones': self._create_zone_data,
			'user': self._create_dmr_user_data,
		}

		for key in create_files:
			create_files[key]()

	def _create_channel_file(self):
		channel_file = RadioWriter.input_writer('input.csv', '\n')
		first_channel = RadioChannelDefault({
			'name': 'National 2m',
			'medium_name': 'Natl 2m',
			'short_name': 'NATL 2M',
			'zone_id': '',
			'rx_freq': '146.520',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_power': 'Low',
			'tx_offset': '',
			'tx_ctcss': '',
			'tx_dcs': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact_id': '',
			'latitude': '',
			'longitude': '',
		}, digital_contacts=None, dmr_ids=None)
		second_channel = RadioChannelDefault({
			'name': 'Basic Repeater',
			'medium_name': 'BasicRpt',
			'short_name': 'BASRPTR',
			'zone_id': '1',
			'rx_freq': '145.310',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_power': 'High',
			'tx_offset': '-0.600',
			'tx_ctcss': '88.5',
			'tx_dcs': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact_id': '',
			'latitude': '',
			'longitude': '',
		}, digital_contacts=None, dmr_ids=None)
		third_channel = RadioChannelDefault({
			'name': 'DMR Repeater',
			'medium_name': 'DMR Rpt',
			'short_name': 'DMR RPT',
			'zone_id': '1',
			'rx_freq': '144.310',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_power': 'High',
			'tx_offset': '-0.600',
			'tx_ctcss': '',
			'tx_dcs': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '1',
			'digital_color': '4',
			'digital_contact_id': '99999',
			'latitude': '',
			'longitude': '',
		}, digital_contacts=None, dmr_ids=None)
		fourth_channel = RadioChannelDefault({
			'name': 'Has lat and long',
			'medium_name': 'lat long',
			'short_name': 'latlong',
			'zone_id': '',
			'rx_freq': '146.520',
			'rx_ctcss': '',
			'rx_dcs': '',
			'rx_dcs_invert': '',
			'tx_power': 'Low',
			'tx_offset': '',
			'tx_ctcss': '',
			'tx_dcs': '',
			'tx_dcs_invert': '',
			'digital_timeslot': '',
			'digital_color': '',
			'digital_contact_id': '',
			'latitude': '38.903450',
			'longitude': '-77.007470',
		}, digital_contacts=None, dmr_ids=None)
		channel_file.writerow(first_channel.headers())
		channel_file.writerow(RadioChannelBuilder.casted(first_channel, radio_types.DEFAULT).output(1))
		channel_file.writerow(RadioChannelBuilder.casted(second_channel, radio_types.DEFAULT).output(2))
		channel_file.writerow(RadioChannelBuilder.casted(third_channel, radio_types.DEFAULT).output(3))
		channel_file.writerow(RadioChannelBuilder.casted(fourth_channel, radio_types.DEFAULT).output(4))
		channel_file.close()

	def _create_dmr_data(self):
		dmr_id_file = RadioWriter.input_writer('dmr_id.csv', '\n')
		dmr_id = DmrIdDefault({
			'radio_id': '00000',
			'name': 'DMR',
		})
		dmr_id_file.writerow(dmr_id.headers())
		dmr_id_file.writerow(dmr_id.output(1))
		dmr_id_file.close()

		digital_contacts_file = RadioWriter.input_writer('digital_contacts.csv', '\n')
		analog_contact = DmrContactDefault({
			'digital_id':  dmr_id.radio_id.fmt_val(),
			'name': 'Analog',
			'call_type': 'all',
		})
		group_contact = DmrContactDefault({
			'digital_id':  99999,
			'name': 'Some Repeater',
			'call_type': 'group',
		})

		digital_contacts_file.writerow(analog_contact.headers())
		digital_contacts_file.writerow(analog_contact.output(1))
		digital_contacts_file.writerow(group_contact.output(2))
		digital_contacts_file.close()

	def _create_zone_data(self):
		zone_id_file = RadioWriter.input_writer('zones.csv', '\n')
		zone = RadioZoneDefault({
			'number': 1,
			'name': 'Zone 1',
		})
		zone_id_file.writerow(zone.headers())
		zone_id_file.writerow(zone.output())
		zone_id_file.close()

	def _create_dmr_user_data(self):
		user_file = RadioWriter.input_writer('user.csv', '\n')
		dmr_user = DmrUserDefault({
			'RADIO_ID': '00000',
			'CALLSIGN': 'N0CALL',
			'FIRST_NAME': 'Sample',
			'LAST_NAME': 'User',
			'CITY': 'Somewhere',
			'STATE': 'Stateville',
			'COUNTRY': 'Theremany',
			'REMARKS': 'Sample Entry',
		})
		user_file.writerow(dmr_user.headers())
		user_file.writerow(dmr_user.output(None))
		user_file.close()
		return

	def _create_output(self):
		FileUtil.safe_create_dir(PathManager.get_output_path())
		return

	def cleanup(self):
		FileUtil.safe_delete_dir(PathManager.get_input_path())
		FileUtil.safe_delete_dir(PathManager.get_output_path())

	def readme(self):
		return

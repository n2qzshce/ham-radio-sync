from src.ham.radio.dmr_contact import DmrContact
from src.ham.radio.dmr_id import DmrId
from src.ham.radio.gpx.radio_additional_gpx import RadioAdditionalGpx
from src.ham.radio.gpx.radio_channel_gpx import RadioChannelGpx
from src.ham.util.file_util import FileUtil
from src.ham.util.path_manager import PathManager
from test.base_test_setup import BaseTestSetup


class GpxTest(BaseTestSetup):
	def setUp(self):
		super().setUp()
		FileUtil.safe_create_dir(PathManager.get_output_path('gpx'))
		self.radio_channel = RadioChannelGpx.create_empty()
		self.digital_contacts = dict()
		cols = dict()
		cols['digital_id'] = '00000'
		cols['name'] = 'Analog'
		cols['call_type'] = 'all'
		digital_contact = DmrContact(cols)
		self.digital_contacts[0] = digital_contact

		cols['digital_id'] = '54321'
		cols['name'] = 'Contact1'
		cols['call_type'] = 'group'
		digital_contact = DmrContact(cols)
		self.digital_contacts[54321] = digital_contact

		cols = dict()
		cols['radio_id'] = '12345'
		cols['name'] = 'N0CALL DMR'
		self.digital_ids = {1: DmrId(cols)}

		self.cols = dict()
		self.cols['name'] = ''
		self.cols['medium_name'] = ''
		self.cols['short_name'] = ''
		self.cols['zone_id'] = ''
		self.cols['rx_freq'] = ''
		self.cols['rx_ctcss'] = ''
		self.cols['rx_dcs'] = ''
		self.cols['rx_dcs_invert'] = ''
		self.cols['tx_power'] = ''
		self.cols['tx_offset'] = ''
		self.cols['tx_ctcss'] = ''
		self.cols['tx_dcs'] = ''
		self.cols['tx_dcs_invert'] = ''
		self.cols['digital_timeslot'] = ''
		self.cols['digital_color'] = ''
		self.cols['digital_contact_id'] = ''
		self.cols['latitude'] = ''
		self.cols['longitude'] = ''

	def test_vhf_repeater(self):
		expected = """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
  <metadata>
    <name>Ham Radio Stations</name>
    <desc>Ham radio station locations generated by Ham Radio Sync</desc>
  </metadata>
  <wpt lat="38.90345" lon="-77.00747">
    <name>Some Repeater</name>
    <desc>Rx: 145.310	Tx offset: -0.600
Rx tone: -	Tx tone: 100.0hz</desc>
  </wpt>
</gpx>"""
		self.cols['name'] = 'Some Repeater'
		self.cols['medium_name'] = 'Some Rpt'
		self.cols['short_name'] = 'SOMERPT'
		self.cols['rx_freq'] = '145.310'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '-0.6'
		self.cols['tx_ctcss'] = '100.0'
		self.cols['latitude'] = '38.903450'
		self.cols['longitude'] = '-77.007470'

		channel = RadioChannelGpx(self.cols, self.digital_contacts, self.digital_ids)
		additional = RadioAdditionalGpx([channel], self.digital_ids, self.digital_contacts, None, None)
		additional.output()
		f = open('out/gpx/ham_radio_sync.gpx')
		result = f.read()
		self.assertEqual(expected, result)

	def test_dmr(self):
		expected = """<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" creator="gpx.py -- https://github.com/tkrajina/gpxpy">
  <metadata>
    <name>Ham Radio Stations</name>
    <desc>Ham radio station locations generated by Ham Radio Sync</desc>
  </metadata>
  <wpt lat="38.90345" lon="-77.00747">
    <name>Dmr Repeater</name>
    <desc>Rx: 447.075	Tx offset: -5.000
Color: 3	Timeslot: 2
Contact: Contact1 54321
Call Type: group</desc>
  </wpt>
</gpx>"""
		self.cols['name'] = 'Dmr Repeater'
		self.cols['medium_name'] = 'Dmr Rpt'
		self.cols['short_name'] = 'DMR RPT'
		self.cols['rx_freq'] = '447.075'
		self.cols['tx_power'] = 'High'
		self.cols['tx_offset'] = '-5'
		self.cols['digital_timeslot'] = '2'
		self.cols['digital_color'] = '3'
		self.cols['digital_contact_id'] = '54321'
		self.cols['latitude'] = '38.903450'
		self.cols['longitude'] = '-77.007470'

		channel = RadioChannelGpx(self.cols, self.digital_contacts, self.digital_ids)
		additional = RadioAdditionalGpx([channel], self.digital_ids, self.digital_contacts, None, None)
		additional.output()
		f = open('out/gpx/ham_radio_sync.gpx')
		result = f.read()
		self.assertEqual(expected, result)

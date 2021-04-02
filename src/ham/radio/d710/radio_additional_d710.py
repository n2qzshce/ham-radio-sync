from src.ham.radio.radio_additional import RadioAdditional
from src.ham.radio.radio_casted_builder import RadioChannelBuilder
from src.ham.util import radio_types
from src.ham.util.file_util import FileUtil


class RadioAdditionalD710(RadioAdditional):
	def __init__(self, channels, dmr_ids, digital_contacts, zones, users):
		super().__init__(channels, dmr_ids, digital_contacts, zones, users)
		for k in range(0, len(self._channels)):
			uncasted_channel = self._channels[k]
			casted_channel = RadioChannelBuilder.casted(uncasted_channel, radio_types.D710)
			self._channels[k] = casted_channel
		return

	def output(self):
		if len(self._channels) < 1:
			return
		self._headers()
		self._output()

	def _headers(self):
		f = FileUtil.open_file(f'out/{radio_types.D710}/{radio_types.D710}.hmk', 'w+')
		headers = self._channels[1].headers()
		f.write(headers+"\n")
		f.close()
		pass

	def _output(self):
		f = FileUtil.open_file(f'out/{radio_types.D710}/{radio_types.D710}.hmk', 'a')
		channel_number = 1
		for channel in self._channels:
			if channel.is_digital():
				continue
			channel_data = channel.output(channel_number)
			f.writelines(channel_data + "\n")
			channel_number += 1
		f.close()

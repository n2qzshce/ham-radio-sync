import os


class PathManager:
	def __init__(self, input_folder_label, output_folder_label):
		self._input_folder_label = input_folder_label
		self._output_folder_label = output_folder_label
		self._input_folder_path = None
		self.set_input_path(os.path.join('./in'))
		self._output_folder_path = None
		self.set_output_path(os.path.join('./out'))

	def get_input_path(self):
		return self._input_folder_path

	def get_output_path(self):
		return self._output_folder_path

	def set_input_path(self, path):
		self._input_folder_path = os.path.abspath(path)
		if self._input_folder_label is not None:
			self._input_folder_label.text = f"Input folder: {self._input_folder_path}"

	def set_output_path(self, path):
		self._output_folder_path = os.path.abspath(path)
		if self._output_folder_label is not None:
			self._output_folder_label.text = f"Output folder: {self._output_folder_path}"

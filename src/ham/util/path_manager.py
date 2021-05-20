import os


class PathManager:
	input_folder_label = None
	output_folder_label = None
	_input_folder_path = None
	_output_folder_path = None

	@classmethod
	def set_input_folder_label(cls, label):
		cls.input_folder_label = label

	@classmethod
	def set_output_folder_label(cls, label):
		cls.output_folder_label = label

	@classmethod
	def get_input_path(cls, file_name=None):
		result = cls._input_folder_path

		if file_name is not None:
			result = os.path.join(cls._input_folder_path, file_name)

		return result

	@classmethod
	def get_output_path(cls, file_name=None):
		result = cls._output_folder_path

		if file_name is not None:
			result = os.path.join(cls._output_folder_path, file_name)

		return result

	@classmethod
	def set_input_path(cls, path):
		cls._input_folder_path = os.path.abspath(path)
		if cls.input_folder_label is not None:
			cls.input_folder_label.text = f"Input folder: {cls._input_folder_path}"

	@classmethod
	def set_output_path(cls, path):
		cls._output_folder_path = os.path.abspath(path)
		if cls.output_folder_label is not None:
			cls.output_folder_label.text = f"Output folder: {cls._output_folder_path}"

	@classmethod
	def input_path_exists(cls, path=None):
		all_path = cls.get_input_path(path)
		return os.path.exists(all_path)

	@classmethod
	def output_path_exists(cls, path):
		all_path = cls.get_output_path(path)
		return os.path.exists(all_path)
	
	@classmethod
	def open_input_file(cls, file_name, mode):
		full_path = os.path.join(cls.get_input_path(), file_name)
		return cls._open_file(full_path, mode)
	
	@classmethod
	def open_output_file(cls, file_name, mode):
		full_path = os.path.join(cls.get_output_path(), file_name)
		return cls._open_file(full_path, mode)

	@classmethod
	def _open_file(cls, file_name, mode):
		return open(f'{file_name}', f'{mode}', encoding='utf-8', newline='\n')

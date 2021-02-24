
class ValidationError(Exception):
	def __init__(self, message, line_num, file_name):
		self.message = message
		self.line_num = line_num
		self.file_name = file_name
		return

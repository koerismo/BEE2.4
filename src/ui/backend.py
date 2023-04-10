''' ui/backend_.py
	Defines a generic backend type for BEE's interface. '''

class BeeGenericBackend():
	''' Defines a generic backend type for BEE's interface. '''

	def __init__(self) -> None:
		pass

	def version() -> str:
		''' Returns the current application's version as a string. '''
		raise NotImplementedError()

	def read_config():
		''' Reads and returns the current application configuration. '''
		raise NotImplementedError()

	def write_config():
		''' Writes the provided object to the application configuration. '''
		raise NotImplementedError()

	def read_packages():
		''' Writes the provided object to the application configuration. '''
		raise NotImplementedError()
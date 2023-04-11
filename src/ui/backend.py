""" ui/backend_.py
	Defines a generic backend type for BEE's interface. """
import abc


class BeeGenericBackend(metaclass=abc.ABCMeta):
	""" Defines a generic backend type for BEE's interface. """

	@abc.abstractmethod
	def version(self) -> str:
		""" Returns the current application's version as a string. """

	@abc.abstractmethod
	def read_config(self) -> dict:
		""" Reads and returns the current application configuration. """

	@abc.abstractmethod
	def write_config(self, cfg: dict) -> None:
		""" Writes the provided object to the application configuration. """

	@abc.abstractmethod
	def read_packages(self):
		""" Writes the provided object to the application configuration. """

''' ui/backend_.py
	Defines a generic backend type for BEE's interface. '''

from abc import ABCMeta, abstractmethod

class BeeGenericBackend(metaclass=ABCMeta):
	''' Defines a generic backend type for BEE's interface. '''

	@abstractmethod
	def version(self) -> str:
		''' Returns the application's version as a string. '''
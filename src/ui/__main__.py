""" ui/__main__.py
	This file serves as a test suite for UI operations with a dummy backend. """

from . import BeeApplication, BeeGenericBackend


# Create dummy API
class BeeDummyBackend(BeeGenericBackend):
	def version(self) -> str:
		return 'dummy'

	def read_config(self) -> dict:
		return { }

	def write_config(self, cfg: dict) -> None:
		...

	def read_packages(self):
		...


# Start app
test_backend = BeeDummyBackend()
test_app = BeeApplication(backend=test_backend)
# test_app.setStyle('fusion')
BeeApplication.exec()

''' ui/__main__.py
	This file serves as a test suite for UI operations with a dummy backend. '''

from . import BeeApplication, BeeGenericBackend

# Create dummy API
class BeeDummyBackend(BeeGenericBackend):
	def version(self) -> str:
		return 'v0.0.1'

# Start app
test_backend = BeeDummyBackend()
test_app = BeeApplication(test_backend)
test_app.exec()
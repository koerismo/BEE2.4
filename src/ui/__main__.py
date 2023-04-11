''' ui/__main__.py
	This file serves as a test suite for UI operations with a dummy backend. '''

from . import BeeApplication, BeeGenericBackend

# Create dummy API
class BeeDummyBackend(BeeGenericBackend): pass

# Start app
test_backend = BeeDummyBackend()
test_app = BeeApplication(backend=test_backend)
# test_app.setStyle('fusion')
test_app.exec()
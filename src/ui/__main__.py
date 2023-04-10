''' ui/__main__.py
	This file serves as a test suite for UI operations with a dummy backend. '''

from . import BeeApplication, BeeGenericBackend

class BeeDummyBackend(BeeGenericBackend): pass

test_backend = BeeDummyBackend()
test_app = BeeApplication(backend=test_backend)
test_app.exec()
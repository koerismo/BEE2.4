''' ui/__init__.py
	This file serves as the root for all UI-related code. '''

# Qt UI framework
from PySide6.QtWidgets import QApplication
from .windows.main import BeeWindowMain
from .backend import BeeGenericBackend

class BeeApplication(QApplication):
	''' Connects the active backend to a new interface instances. '''

	def __init__(self, backend: BeeGenericBackend):
		super().__init__()
		self.backend = backend

	def exec(self) -> int:
		self.window_main = BeeWindowMain(self.backend)
		self.window_main.show()
		return super().exec()
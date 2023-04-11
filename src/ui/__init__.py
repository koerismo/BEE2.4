""" ui/__init__.pyi
	This file serves as the root for all UI-related code. """

# Qt UI framework
from PySide6.QtWidgets import QApplication
from .backend import BeeGenericBackend

from .windows.main import BeeWindowMain
from .windows.export import BeeWindowExport


class BeeApplication(QApplication):
	""" Connects the active backend to a new interface instances. """
	window_main: BeeWindowMain
	window_export: BeeWindowExport

	def __init__(self, backend: BeeGenericBackend):
		super().__init__()
		self.backend = backend
		self.window_main = BeeWindowMain(self.backend)
		self.window_main.show()

		self.window_export = BeeWindowExport(self.backend, self.window_main)
		self.window_export.setGeometry(self.window_main.x() + self.window_main.width() + 10, self.window_main.y() + 31, self.window_export.width(), self.window_export.height())
		self.window_export.show()

''' ui/__init__.py
	This file serves as the root for all UI-related code. '''

# Qt UI framework
from PySide6.QtWidgets import QApplication

# App
from .backend import BeeGenericBackend
from .windows.main import BeeWindowMain
from .windows.export import BeeWindowExport
from .windows.palettes import BeeWindowPalettes

class BeeApplication(QApplication):
	''' Connects the active backend to a new interface instances. '''

	def __init__(self, backend: BeeGenericBackend):
		super().__init__()
		self.backend = backend

	def exec(self) -> int:
		self.window_main = BeeWindowMain(self.backend)
		self.window_main.show()

		self.window_export = BeeWindowExport(self.backend, self.window_main)
		self.window_export.show()
		self.window_export.setGeometry(self.window_main.x() + self.window_main.width() + 10, self.window_main.y() + 31, self.window_export.width(), self.window_export.height())

		self.window_palettes = BeeWindowPalettes(self.backend, self.window_main)
		self.window_palettes.show()
		self.window_palettes.setGeometry(self.window_main.x() - self.window_palettes.width() - 10, self.window_main.y() + 31, self.window_palettes.width(), self.window_palettes.height())

		return super().exec()
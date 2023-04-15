''' ui/windows/palettes.py
	This file defines the palettes window. '''

# Application backend type
from ..backend import BeeGenericBackend

# Qt UI framework
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QWidget,
)

class BeeWindowPalettes(QWidget):
	def __init__(self, backend: BeeGenericBackend, parent: QWidget=None, flags: Qt.WindowType=Qt.Window):
			super().__init__(parent, flags) # type: ignore
			self.backend = backend
			self.resize(230, 280)
			self.setWindowTitle('Palettes')
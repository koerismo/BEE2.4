''' ui/windows/palettes.py
	This file defines the palettes window. '''

# Application backend type
from ..backend import BeeGenericBackend

# Qt UI framework
from PySide6 import QtCore, QtGui, QtWidgets

# Qt UI framework shortcuts
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
	QWidget,
	QHBoxLayout,
	QVBoxLayout,
	QGroupBox,

	QLabel,
	QLineEdit,
	QPushButton,

	QScrollArea,
	QGridLayout,
)

class BeeWindowPalettes(QWidget):
	def __init__(self, backend: BeeGenericBackend, parent: QWidget=None, window_type: Qt.WindowType=Qt.WindowType.Window):
			super().__init__(parent, window_type)
			self.backend = backend
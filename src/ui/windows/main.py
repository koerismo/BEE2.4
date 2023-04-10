''' ui/windows/main.py
	This file defines the main window. '''

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

	QScrollArea,
	QGridLayout,
	QLayout
)

class BeeWindowMain(QWidget):
	''' The primary window, with palette selection. '''

	def __init__(self, backend: BeeGenericBackend, parent: QWidget=None, window_type: Qt.WindowType=Qt.WindowType.Window):
		super().__init__(parent, window_type)
		self.backend = backend

		# Shitty hack to prevent window from growing vertically
		self.setMaximumHeight(0)

		# Begin window initialization
		self.setWindowTitle('BEEMOD [Qt] 2.4.43.0 64-bit - Portal 2')
		layout = QHBoxLayout(self)

		grid_left = QGridLayout()
		layout.addLayout(grid_left)

		scroll_right = QScrollArea()
		scroll_right.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
		scroll_right.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		scroll_right.setVerticalScrollBar(QtWidgets.QScrollBar(Qt.Orientation.Vertical))

		grid_right = QGridLayout()
		grid_right_container = QWidget()
		grid_right_container.setLayout(grid_right)
		scroll_right.setWidget(grid_right_container)
		layout.addWidget(scroll_right)

		grid_left.setSpacing(2)
		grid_left.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
		grid_right.setSpacing(2)
		grid_right.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

		slot_colors = QPalette()
		slot_colors.setColor(QPalette.ColorRole.Window, '#ddd')

		# Add dummy spaces
		for y in range(8):
			for x in range(4):
				widget = QWidget(self)
				widget.setAutoFillBackground(True)
				widget.setPalette(slot_colors)
				widget.setFixedSize(64, 64)
				grid_left.addWidget(widget, y, x)

		for y in range(16):
			for x in range(4):
				widget = QWidget(self)
				widget.setAutoFillBackground(True)
				widget.setPalette(slot_colors)
				widget.setFixedSize(64, 64)
				grid_right.addWidget(widget, y, x)
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
	QLabel,
	QLineEdit,

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
		self.resize(600, 500)

		# Initialize window
		self.setWindowTitle('BEEMOD [Qt] 2.4.43.0 64-bit - Portal 2')
		layout = QHBoxLayout(self)

		# Left/right layouts
		layout_l = QVBoxLayout()
		layout_r = QVBoxLayout()
		layout.addLayout(layout_l)
		layout.addLayout(layout_r)

		# Left-side header
		layout_l.addWidget(QLabel('ITEMS'))

		# Right-side header
		header_r = QHBoxLayout()
		layout_r.addLayout(header_r)
		header_r.addWidget(QLabel('SEARCH'))
		header_r.addWidget(QLineEdit())

		# Left-side grid
		grid_l = QGridLayout()
		layout_l.addLayout(grid_l)
		grid_l.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
		grid_l.setSpacing(2)

		# Right-side scroll area
		scroll = QScrollArea()
		layout_r.addWidget(scroll)
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
		scroll.setVerticalScrollBar(QtWidgets.QScrollBar(Qt.Orientation.Vertical))
		scroll_widget = QWidget(scroll)
		scroll.setWidget(scroll_widget)

		# Right-side grid
		grid_r = QGridLayout(scroll_widget)
		grid_r.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
		grid_r.setSpacing(2)

		# Fill everything with dummy slots
		slot_colors = QPalette()
		slot_colors.setColor(QPalette.ColorRole.Window, '#ddd')

		for y in range(8):
			for x in range(4):
				widget = QWidget(self)
				widget.setAutoFillBackground(True)
				widget.setPalette(slot_colors)
				widget.setFixedSize(64, 64)
				grid_l.addWidget(widget, y, x)

		for y in range(16):
			for x in range(4):
				widget = QWidget(self)
				widget.setAutoFillBackground(True)
				widget.setPalette(slot_colors)
				widget.setFixedSize(64, 64)
				grid_r.addWidget(widget, y, x)
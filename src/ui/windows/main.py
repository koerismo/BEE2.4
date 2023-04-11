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
	QFrame,
	QHBoxLayout,
	QVBoxLayout,
	QLabel,
	QLineEdit,

	QScrollArea,
	QGridLayout,
	QLayout,

	QMenuBar,
	QMenu,
)

class BeeWindowMain(QWidget):
	''' The primary window, with palette selection. '''

	def __init__(self, backend: BeeGenericBackend, parent: QWidget=None, window_type: Qt.WindowType=Qt.WindowType.Window):
		super().__init__(parent, window_type)
		self.backend = backend
		self.layout = QVBoxLayout(self)
		self.layout.setContentsMargins(0,0,0,0)

		# Shitty hack to prevent window from growing vertically
		self.setMaximumHeight(0)
		self.resize(650, 500)

		# Set background color
		win_colors = QPalette()
		win_colors.setColor(QPalette.ColorRole.Window, '#ddd')
		self.setPalette(win_colors)

		# Menu
		bar = QMenuBar()
		self.layout.addWidget(bar)

		m_file = QMenu('File')
		m_edit = QMenu('Edit')
		m_palette = QMenu('Palette')
		m_window = QMenu('Window')
		m_help = QMenu('Help')
		bar.addMenu(m_file)
		bar.addMenu(m_edit)
		bar.addMenu(m_palette)
		bar.addMenu(m_window)
		bar.addMenu(m_help)

		# Initialize window
		self.setWindowTitle('BEEMOD [Qt] 2.4.43.0 64-bit - Portal 2')
		layout = QHBoxLayout()
		layout.setContentsMargins(5,0,5,5)
		self.layout.addLayout(layout)

		# Define widget theme
		widget_colors = QPalette()
		widget_colors.setColor(QPalette.ColorRole.Window, '#fff')		# Background
		widget_colors.setColor(QPalette.ColorRole.WindowText, '#222')	# Border

		# Left/right widgets and layouts
		widget_l = QFrame()
		widget_r = QFrame()
		widget_l.setFrameShape(QFrame.Shape.Box)
		widget_r.setFrameShape(QFrame.Shape.Box)
		layout.addWidget(widget_l)
		layout.addWidget(widget_r)
		layout_l = QVBoxLayout(widget_l)
		layout_r = QVBoxLayout(widget_r)

		# Fill widget backgrounds
		widget_l.setPalette(widget_colors)
		widget_r.setPalette(widget_colors)
		widget_l.setAutoFillBackground(True)
		widget_r.setAutoFillBackground(True)

		# Left-side header
		header_text_l = QLabel('Items')
		header_text_l.setPalette(QPalette())
		layout_l.addWidget(header_text_l)

		# Right-side header
		header_r = QHBoxLayout()
		layout_r.addLayout(header_r)
		header_r.addWidget(QLabel('Search:'))
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
		slot_colors.setColor(QPalette.ColorRole.Window, '#e5e5e5')

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
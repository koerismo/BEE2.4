''' ui/windows/export.py
	This file defines the export options window. '''

# Application backend type
from ..backend import BeeGenericBackend

# Shared
from ..shared.textbutton import QTextButtonInput
from ..shared.hline import QHLine

# Qt UI framework
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
	QWidget,
	QVBoxLayout,

	QLabel,
	QLineEdit,
	QPushButton,

	QScrollArea,
	QScrollBar,
	QGridLayout,
	QSizePolicy,
	QLayout
)

class BeeWindowExport(QWidget):
	''' The export window, containing style, skybox, voice, and various other options. '''

	backend: BeeGenericBackend

	def __init__(self, backend: BeeGenericBackend, parent: QWidget=None, flags: Qt.WindowType=Qt.Window):
			super().__init__(parent, flags) # type: ignore
			self.backend = backend
			self.resize(260, 260)
			self.setWindowTitle('Export Options')

			win_layout = QVBoxLayout(self) # type: ignore
			win_layout.setContentsMargins(0, 0, 0, 0)

			scroll_area = QScrollArea(self)
			win_layout.addWidget(scroll_area)

			scroll_area.setVerticalScrollBar(QScrollBar(Qt.Orientation.Vertical))
			scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

			scroll_widget = QWidget()
			scroll_area.setWidget(scroll_widget)
			scroll_area.setWidgetResizable(True)
			scroll_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

			layout = QVBoxLayout()
			layout.setSpacing(0)

			scroll_widget.setLayout(layout)
			grid = QGridLayout()
			layout.addLayout(grid)

			grid.setColumnStretch(1, 1)
			grid.setSpacing(1)

			grid.addWidget(QLabel('Style: '),    0, 0)
			grid.addWidget(QLabel('Voice: '),    2, 0)
			grid.addWidget(QLabel('Skybox: '),   3, 0)
			grid.addWidget(QLabel('Elev Vid: '), 4, 0)
			grid.addWidget(QLabel('Corridor: '), 5, 0)

			grid.addWidget(QTextButtonInput(), 0, 1)
			grid.addWidget(QPushButton('Use Suggested'), 1, 1)
			grid.addWidget(QTextButtonInput(), 2, 1)
			grid.addWidget(QTextButtonInput(), 3, 1)
			grid.addWidget(QTextButtonInput(), 4, 1)
			grid.addWidget(QTextButtonInput(), 5, 1)

			layout.addWidget(QHLine('Music:'))
from PySide6.QtWidgets import QHBoxLayout, QWidget, QLineEdit, QPushButton, QSizePolicy
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import QObject, Signal
from typing import Optional

class QTextButtonInput(QWidget):
	''' Implements a text line input accompanied by a "..." button. '''

	input: QLineEdit
	button: QPushButton
	pressed: Signal = Signal()

	def __init__(self, text: str='', parent: QWidget=None) -> None:
		super().__init__(parent)
		layout = QHBoxLayout(self)

		self.input = QLineEdit()
		self.input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
		self.input.setDisabled(True)
		self.input.setText(text)

		self.button = QPushButton('...')
		self.button.pressed.connect(self.pressed)
		self.button.setMaximumWidth(24)

		layout.addWidget(self.input, 1)
		layout.addWidget(self.button, 0)
		layout.setSpacing(1)
		layout.setContentsMargins(0, 0, 0, 0)

	def text(self) -> str:
		return self.input.text()

	def setText(self, text: str) -> None:
		return self.input.setText(text)
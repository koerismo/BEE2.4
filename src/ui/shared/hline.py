from PySide6.QtWidgets import QFrame, QWidget, QHBoxLayout, QLabel, QSizePolicy
from PySide6.QtCore import Qt
from typing import Optional

class QHLine(QWidget):
	def __init__(self, title: str='', parent: Optional[QWidget]=None) -> None:
		super().__init__(parent, Qt.Widget) # type: ignore

		self.setContentsMargins(0, 0, 0, 0)

		layout = QHBoxLayout(self)
		layout.setSpacing(10)
		layout.addWidget(QLabel(title))

		line = QFrame()
		line.setContentsMargins(0, 0, 0, 0)
		line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		line.setFrameShape(QFrame.HLine)
		line.setFrameShadow(QFrame.Plain)
		layout.addWidget(line)
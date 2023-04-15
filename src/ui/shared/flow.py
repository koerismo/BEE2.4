from PySide6.QtWidgets import QLayout, QWidget, QLayoutItem
from PySide6.QtCore import QRect, QSize
from typing import Optional, List
from math import ceil

class QFlowGridLayout(QLayout):
	''' Defines a wrapping grid-like container. Adapted to Python from
		https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html '''

	itemList: List[QLayoutItem]
	itemSize: int

	def __init__(self, itemSize: int, parent: QWidget=None, margin: int=0, spacing: int=0) -> None:
		super().__init__(parent)
		self.itemList = []
		self.itemSize = itemSize

		self.setSpacing(spacing)
		self.setContentsMargins(margin, margin, margin, margin)

	def addItem(self, item: QLayoutItem):
		self.itemList.append(item)

	def count(self) -> int:
		return len(self.itemList)

	def itemAt(self, index: int) -> Optional[QLayoutItem]:
		if index < 0 or index >= len(self.itemList): return None
		return self.itemList[index]

	def takeAt(self, index: int) -> QLayoutItem:
		return self.itemList.pop(index)

	def hasHeightForWidth(self) -> bool:
		return True

	def getTableDimensions(self, width: int) -> QSize:
		# print(width)
		''' Calculates the number of columns and rows for the given width. '''

		# Apply margins
		left, _, right, _ = self.getContentsMargins()
		width -= right + left

		# Determine column and row count
		spacing = self.spacing()
		columns = (width + spacing) // (self.itemSize + spacing)
		rows = ceil(len(self.itemList) / columns)

		# Return plain
		return QSize(columns, rows)

	def heightForWidth(self, width: int) -> int:

		# Apply margins
		left, top, right, bottom = self.getContentsMargins()
		width -= right + left

		# Determine column and row count
		spacing = self.spacing()
		columns = (width + spacing) // (self.itemSize + spacing)
		rows = ceil(len(self.itemList) / columns)

		# Determine height from rows + margins
		return (self.itemSize + spacing) * rows - spacing + top + bottom

	def setGeometry(self, rect: QRect) -> None:
		super().setGeometry(rect)
		self.doLayout(rect)

	def minimumSize(self) -> QSize:
		return QSize(self.itemSize, self.itemSize).grownBy(self.contentsMargins())

	def sizeHint(self) -> QSize:
		return self.minimumSize()

	def doLayout(self, rect: QRect) -> None:
		# Compared to the example, this runs a much more naive algorithm that assumes all children are the same dimensions.
		# This is partially for faster speeds, but mostly because I am lazy.

		columns = self.getTableDimensions(rect.width()).width()
		spacing = self.spacing()
		margins = self.contentsMargins()
		left, top, _, _ = rect.adjusted(margins.left(), margins.top(), -margins.right(), -margins.bottom()).getRect()

		for ind, item in enumerate(self.itemList):
			col = ind % columns
			row = (ind - col) // columns
			x = (self.itemSize + spacing) * col
			y = (self.itemSize + spacing) * row
			item.setGeometry(QRect(x + left, y + top, self.itemSize, self.itemSize))
from PyQt5.QtWidgets import (
    QGraphicsEllipseItem, QGraphicsTextItem, QToolTip,
    QDialog, QVBoxLayout, QPushButton, QHBoxLayout
)
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, pos, parent_level):
        super().__init__(-20, -20, 40, 40)
        self.node_id = node_id
        self.parent_level = parent_level
        self.setBrush(QBrush(Qt.gray))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setPos(pos)
        self.locked = False

        self.text = QGraphicsTextItem(str(node_id))
        self.text.setDefaultTextColor(Qt.white)
        self.text.setFont(QFont("Arial", 10, QFont.Bold))
        self.text.setParentItem(self)
        self.text.setPos(-8, -10)

        # Define the allowed color palette
        self.allowed_colors = {
            "Red": "#E74C3C",
            "Green": "#2ECC71",
            " Blue": "#3498DB",
            "Yellow": "#F1C40F"
        }

    def mousePressEvent(self, event):
        if not self.locked and not self.parent_level.committed:
            self.show_color_selection_dialog()
        super().mousePressEvent(event)

    def show_color_selection_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle(f"Select a color for Node {self.node_id}")
        layout = QVBoxLayout()

        button_row = QHBoxLayout()
        for label, hex_code in self.allowed_colors.items():
            btn = QPushButton(label)
            btn.setStyleSheet(f"background-color: {hex_code}; color: black; font-weight: bold;")
            btn.clicked.connect(lambda _, c=hex_code: self.select_color(dialog, c))
            button_row.addWidget(btn)

        layout.addLayout(button_row)
        dialog.setLayout(layout)
        dialog.exec_()

    def select_color(self, dialog, color_hex):
        self.setBrush(QBrush(QColor(color_hex)))
        self.parent_level.node_colors[self.node_id] = color_hex
        self.parent_level.update_narration(f"🎨 Prover colored node {self.node_id} with color.")
        dialog.accept()

    def hoverEnterEvent(self, event):
        if self.locked:
            QToolTip.showText(event.screenPos(), "🔒 This node is committed", self.parent_level)
        else:
            QToolTip.showText(event.screenPos(), f" Node {self.node_id}: Click to choose a color", self.parent_level)

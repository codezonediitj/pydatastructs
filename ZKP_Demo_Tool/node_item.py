from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QColorDialog, QToolTip
from PyQt5.QtGui import QBrush, QColor, QFont
from PyQt5.QtCore import Qt

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, pos, parent_level):
        super().__init__(-20, -20, 40, 40)  # 40x40 circle
        self.node_id = node_id
        self.parent_level = parent_level
        self.setBrush(QBrush(Qt.gray))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setPos(pos)
        self.locked = False

        # Node label
        self.text = QGraphicsTextItem(str(node_id))
        self.text.setDefaultTextColor(Qt.white)
        self.text.setFont(QFont("Arial", 10, QFont.Bold))
        self.text.setParentItem(self)
        self.text.setPos(-8, -10)

    def mousePressEvent(self, event):
        if not self.locked and not self.parent_level.committed:
            color = QColorDialog.getColor()
            if color.isValid():
                self.setBrush(QBrush(color))
                self.parent_level.node_colors[self.node_id] = color.name()
                self.parent_level.update_narration(f"🎨 Prover colored node {self.node_id} as a secret.")
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        if self.locked:
            QToolTip.showText(event.screenPos(), "🔒 This node is committed", self.parent_level)
        else:
            QToolTip.showText(event.screenPos(), f" Node {self.node_id}: Click to color", self.parent_level)
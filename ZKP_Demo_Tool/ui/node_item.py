# node_item.py
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QColor, QFont, QPen
from PyQt5.QtCore import Qt, QPointF, QPropertyAnimation

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, pos, parent, label=None):
        super().__init__(-20, -20, 40, 40)
        self.node_id = node_id
        self.parent = parent
        self.setBrush(QBrush(Qt.gray))
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(1)

        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setPos(pos)

        self.locked = False
        self.role = None
        self.label = label if label else f"Node {node_id}"
        self.hash_display = None

        # Label below node
        self.text_item = QGraphicsTextItem(self.label, self)
        self.text_item.setFont(QFont("Arial", 9))
        self.text_item.setDefaultTextColor(Qt.white)
        self.text_item.setPos(-self.text_item.boundingRect().width() / 2, 22)

        # Lock visual indicator
        self.lock_icon = QGraphicsTextItem("🔒", self)
        self.lock_icon.setFont(QFont("Arial", 12))
        self.lock_icon.setDefaultTextColor(Qt.darkGray)
        self.lock_icon.setPos(-10, -35)
        self.lock_icon.setVisible(False)
    def set_label(self, label_text):
        if hasattr(self, 'label'):
            self.scene().removeItem(self.label)

        from PyQt5.QtWidgets import QGraphicsTextItem
        from PyQt5.QtCore import Qt

        self.label = QGraphicsTextItem(label_text)
        self.label.setDefaultTextColor(Qt.white)
        self.label.setParentItem(self)
        self.label.setPos(-20, -35)

    def set_color(self, color):
        if not self.locked:
            self.setBrush(QBrush(QColor(color)))
    def change_color(self):
        current_color = self.brush().color()
        next_color = self.get_next_color(current_color)
        self.setBrush(QBrush(next_color))
        self.parent.node_colors[self.node_id] = next_color
    def mousePressEvent(self, event):
        self.change_color()
    def get_next_color(self, current_color):
        color_cycle = [Qt.red, Qt.green, Qt.blue]  # Or your fixed palette
        try:
            i = color_cycle.index(current_color)
            return color_cycle[(i + 1) % len(color_cycle)]
        except ValueError:
            return color_cycle[0]
    def lock(self):
        self.locked = True
        self.setBrush(QBrush(Qt.gray))
        self.setPen(QPen(Qt.darkGray, 2))
        self.lock_icon.setVisible(True)
        self.update()

    def unlock(self):
        self.locked = False
        self.setPen(QPen(Qt.black, 2))
        self.setBrush(QBrush(Qt.gray))
        self.lock_icon.setVisible(False)
        self.update()

    def show_hash(self, short_hash):
        if not self.hash_display:
            self.hash_display = QGraphicsTextItem(short_hash, self)
            self.hash_display.setFont(QFont("Courier", 7))
            self.hash_display.setDefaultTextColor(Qt.lightGray)
            self.hash_display.setPos(-self.hash_display.boundingRect().width() / 2, 35)
        else:
            self.hash_display.setPlainText(short_hash)

    def hide_hash(self):
        if self.hash_display:
            self.scene().removeItem(self.hash_display)
            self.hash_display = None

    def set_label(self, label):
        self.label = label
        self.text_item.setPlainText(label)

    def pulse_red(self):
        # Animate node glow red for non-repudiation breach
        animation = QPropertyAnimation(self, b"opacity")
        animation.setDuration(800)
        animation.setKeyValueAt(0, 1.0)
        animation.setKeyValueAt(0.5, 0.3)
        animation.setKeyValueAt(1, 1.0)
        animation.start()
        self.setBrush(QBrush(QColor("red")))
    def set_label(self, text):
        label = QGraphicsTextItem(text, self)
        label.setDefaultTextColor(Qt.black)
        label.setFont(QFont("Arial", 10))
        label.setPos(-10, -10)  # Adjust position if needed

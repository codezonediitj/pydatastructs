import sys
import hashlib
import secrets
import random
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QMessageBox, QHBoxLayout, QTextEdit, QGraphicsEllipseItem,
    QGraphicsTextItem, QColorDialog, QComboBox, QGraphicsScene, QGraphicsView,QDialog, QDialogButtonBox, QGraphicsLineItem
)
from PyQt5.QtGui import QFont, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF, QPointF

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, pos, parent):
        super().__init__(-20, -20, 40, 40)
        self.node_id = node_id
        self.parent = parent
        self.setBrush(QBrush(Qt.gray))
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setPos(pos)

    def mousePressEvent(self, event):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setBrush(QBrush(color))
            self.parent.node_colors[self.node_id] = color.name()
            self.parent.instructions.setText(f"🎨 Node {self.node_id} set to {color.name()}")
        super().mousePressEvent(event)

# ------------------ Main Game Class ------------------
class ZKPCommitmentGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKP Commitment Game - Interactive Edition")
        self.setGeometry(100, 100, 800, 600)

        self.colors = ["Red", "Green", "Blue"]
        self.node_colors = {}
        self.commitments = {}
        self.nonces = {}

        self.layout = QVBoxLayout()
        self.instructions = QLabel("Step 1: Click a node to choose its color.")
        self.layout.addWidget(self.instructions)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.buttons_layout = QHBoxLayout()
        self.commit_button = QPushButton("🔒 Commit")
        self.challenge_button = QPushButton("🎲 Challenge Edge")
        self.commit_button.clicked.connect(self.commit_colors)
        self.challenge_button.clicked.connect(self.challenge_random_edge)
        self.buttons_layout.addWidget(self.commit_button)
        self.buttons_layout.addWidget(self.challenge_button)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)
        self.create_graph()

    def create_graph(self):
        self.nodes = {}
        self.edges = []

        positions = [
            QPointF(300, 100), QPointF(500, 200),
            QPointF(450, 400), QPointF(150, 400), QPointF(100, 200)
        ]
        for i, pos in enumerate(positions):
            node = NodeItem(i, pos, self)
            self.scene.addItem(node)
            self.nodes[i] = node

        edge_indices = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]
        for i, j in edge_indices:
            line = QGraphicsLineItem(
                self.nodes[i].pos().x(), self.nodes[i].pos().y(),
                self.nodes[j].pos().x(), self.nodes[j].pos().y())
            line.setPen(QPen(Qt.white))
            self.scene.addItem(line)
            self.edges.append((i, j))

        self.view.setScene(self.scene)

    def commit_colors(self):
        self.commitments.clear()
        self.nonces.clear()
        for node_id, color in self.node_colors.items():
            nonce = str(random.randint(1000, 9999))
            commitment = hashlib.sha256((color + nonce).encode()).hexdigest()
            self.commitments[node_id] = commitment
            self.nonces[node_id] = nonce
        self.instructions.setText("🔒 Commitments locked. Now run a challenge.")

    def challenge_random_edge(self):
        if not self.commitments:
            QMessageBox.warning(self, "Warning", "Please commit first!")
            return

        edge = random.choice(self.edges)
        node1, node2 = edge
        color1 = self.node_colors.get(node1)
        color2 = self.node_colors.get(node2)

        if color1 is None or color2 is None:
            QMessageBox.warning(self, "Incomplete", "Some nodes are uncolored.")
            return

        if color1 != color2:
            self.instructions.setText(f"✅ Verifier challenged edge {edge}: Colors are different. Proof OK.")
        else:
            self.instructions.setText(f"❌ Verifier challenged edge {edge}: Same color! Proof fails.")

# ------------------ Run Application ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZKPCommitmentGame()
    window.show()
    sys.exit(app.exec_())
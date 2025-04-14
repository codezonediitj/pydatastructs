import sys
import hashlib
import secrets
import random
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QMessageBox, QHBoxLayout, QTextEdit, QGraphicsEllipseItem,
    QGraphicsTextItem, QColorDialog, QComboBox, QGraphicsScene, QGraphicsView,QDialog, QDialogButtonBox, QGraphicsLineItem, QToolTip
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
        self.locked = False

        self.text = QGraphicsTextItem(str(node_id))
        self.text.setDefaultTextColor(Qt.white)
        self.text.setFont(QFont("Arial", 10, QFont.Bold))
        self.text.setParentItem(self)
        self.text.setPos(-10, -10)

    def mousePressEvent(self, event):
        if not self.locked:
            color = QColorDialog.getColor()
            if color.isValid():
                self.setBrush(QBrush(color))
                self.parent.node_colors[self.node_id] = color.name()
                self.parent.narration.setText(f"🎨 Prover: I colored node {self.node_id} as a secret.")
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        if self.locked:
            QToolTip.showText(event.screenPos(), "🔒 Color is committed and hidden", self.parent)
        else:
            QToolTip.showText(event.screenPos(), "Click to secretly color this node", self.parent)

class ZKPCommitmentGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKP Commitment Game - Interactive Edition")
        self.setGeometry(100, 100, 900, 650)

        self.rounds = 0
        self.max_rounds = 3
        self.colors = ["Red", "Green", "Blue"]
        self.node_colors = {}
        self.commitments = {}
        self.nonces = {}

        self.layout = QVBoxLayout()

        self.narration = QLabel("👩‍💼 Prover: Let's secretly color the graph to prove I know a valid coloring!")
        self.narration.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.narration)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.buttons_layout = QHBoxLayout()
        self.commit_button = QPushButton("🔒 Commit")
        self.challenge_button = QPushButton("🎲 Challenge Edge")
        self.reset_button = QPushButton("🔁 Reset Game")
        self.commit_button.clicked.connect(self.commit_colors)
        self.challenge_button.clicked.connect(self.challenge_random_edge)
        self.reset_button.clicked.connect(self.reset_game)
        self.buttons_layout.addWidget(self.commit_button)
        self.buttons_layout.addWidget(self.challenge_button)
        self.buttons_layout.addWidget(self.reset_button)
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
            line.setPen(QPen(Qt.white, 2))
            self.scene.addItem(line)
            self.edges.append((i, j))

        self.view.setScene(self.scene)

    def commit_colors(self):
        self.commitments.clear()
        self.nonces.clear()
        missing = [nid for nid in self.nodes if nid not in self.node_colors]
        if missing:
            QMessageBox.warning(self, "Incomplete", f"Please color all nodes: Missing {missing}")
            return

        for node_id, color in self.node_colors.items():
            nonce = str(random.randint(1000, 9999))
            commitment = hashlib.sha256((color + nonce).encode()).hexdigest()
            self.commitments[node_id] = commitment
            self.nonces[node_id] = nonce
            self.nodes[node_id].locked = True
            self.nodes[node_id].setBrush(QBrush(Qt.gray))

        self.narration.setText("🔒 Prover: I’ve committed my secrets! Verifier, try to challenge me.")

    def challenge_random_edge(self):
        if not self.commitments:
            QMessageBox.warning(self, "Warning", "Please commit first!")
            return

        edge = random.choice(self.edges)
        node1, node2 = edge
        color1 = self.node_colors.get(node1)
        color2 = self.node_colors.get(node2)

        self.nodes[node1].setBrush(QBrush(QColor(color1)))
        self.nodes[node2].setBrush(QBrush(QColor(color2)))

        if color1 == color2:
            result = f"❌ Verifier: Edge {edge} has same colors. Proof fails."
        else:
            result = f"✅ Verifier: Edge {edge} colors differ. Proof OK."
            self.rounds += 1

        self.narration.setText(result + f" Round {self.rounds}/{self.max_rounds}")

        if self.rounds == self.max_rounds:
            QMessageBox.information(self, "🎉 Success", "Verifier: I’m convinced! Prover has a valid coloring.")

    def reset_game(self):
        self.node_colors.clear()
        self.commitments.clear()
        self.nonces.clear()
        self.rounds = 0
        for node in self.nodes.values():
            node.locked = False
            node.setBrush(QBrush(Qt.gray))

        self.narration.setText("🔁 Game reset. 👩‍💼 Prover: Let's try again!")

# ------------------ Run Application ------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZKPCommitmentGame()
    window.show()
    sys.exit(app.exec_())

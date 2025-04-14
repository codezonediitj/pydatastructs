
import random
import hashlib
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsScene, QGraphicsView,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtGui import QFont, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QPointF, QTimer

from ui.node_item import NodeItem


class BaseLevel(QWidget):
    def __init__(self, level_name, parent_selector, max_rounds=3):
        super().__init__()
        self.level_name = level_name
        self.parent_selector = parent_selector
        self.max_rounds = max_rounds
        self.rounds = 0
        self.committed = False

        self.node_colors = {}
        self.commitments = {}
        self.nonces = {}
        self.nodes = {}
        self.edges = []

        self.setWindowTitle(f"{level_name} - ZKP Game")
        self.setGeometry(100, 100, 900, 650)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.narration = QLabel(f"👩\u200d💼 Prover: Color nodes secretly to convince the Verifier!")
        self.narration.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.narration)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.buttons_layout = QHBoxLayout()
        self.commit_btn = QPushButton("🔒 Commit")
        self.challenge_btn = QPushButton("🎲 Challenge")
        self.reset_btn = QPushButton("🔁 Reset")
        self.commit_btn.clicked.connect(self.commit_colors)
        self.challenge_btn.clicked.connect(self.challenge_edge_once)
        self.reset_btn.clicked.connect(self.reset_game)

        self.buttons_layout.addWidget(self.commit_btn)
        self.buttons_layout.addWidget(self.challenge_btn)
        self.buttons_layout.addWidget(self.reset_btn)
        self.layout.addLayout(self.buttons_layout)

        self.show_education_modal()

    def show_education_modal(self):
        QMessageBox.information(
            self,
            "🔐 About Zero-Knowledge Rounds",
            "Each round simulates one ZKP exchange.\n\n"
            "You can only commit once per round, and reveal one edge.\n"
            "The verifier learns nothing beyond this — try not to leak!\n\n"
            "You’ll repeat this 3 times to earn trust."
        )

    def update_narration(self, text):
        self.narration.setText(text)

    def create_graph(self, node_positions, edge_list):
        for i, pos in enumerate(node_positions):
            node = NodeItem(i, pos, self)
            self.scene.addItem(node)
            self.nodes[i] = node

        for i, j in edge_list:
            x1, y1 = node_positions[i].x(), node_positions[i].y()
            x2, y2 = node_positions[j].x(), node_positions[j].y()
            line = self.scene.addLine(x1, y1, x2, y2, QPen(Qt.white, 2))
            self.edges.append((i, j))

        self.view.setScene(self.scene)

    def commit_colors(self):
        missing = [nid for nid in self.nodes if nid not in self.node_colors]
        if missing:
            self.update_narration(f"⚠️ Please color all nodes: Missing {missing}")
            return

        self.commitments.clear()
        self.nonces.clear()

        for node_id, color in self.node_colors.items():
            nonce = str(random.randint(1000, 9999))
            commitment = hashlib.sha256((color + nonce).encode()).hexdigest()
            self.commitments[node_id] = commitment
            self.nonces[node_id] = nonce
            self.nodes[node_id].locked = True
            self.nodes[node_id].setBrush(QBrush(Qt.gray))

        self.committed = True
        self.update_narration("🔒 Commitments made. Verifier, choose an edge to challenge!")

    def challenge_edge_once(self):
        if not self.committed:
            QMessageBox.warning(self, "⚠️ Commit First", "You must commit before challenging.")
            return

        edge = random.choice(self.edges)
        node1, node2 = edge
        color1 = self.node_colors.get(node1)
        color2 = self.node_colors.get(node2)

        self.nodes[node1].setBrush(QBrush(QColor(color1)))
        self.nodes[node2].setBrush(QBrush(QColor(color2)))

        if color1 == color2:
            result = f"❌ Verifier: Edge {edge} has same colors. Proof fails!"
        else:
            result = f"✅ Verifier: Edge {edge} looks good."
            self.rounds += 1

        self.update_narration(result + f" Round {self.rounds}/{self.max_rounds}")

        if self.rounds < self.max_rounds:
            QTimer.singleShot(1500, self.prompt_next_round)
        else:
            QTimer.singleShot(1500, self.finish_level)

    def prompt_next_round(self):
        QMessageBox.information(
            self,
            "🎯 Round Complete",
            "Round complete! Please recolor the graph to start the next round."
        )
        self.reset_game(preserve_round=True)

    def finish_level(self):
        QMessageBox.information(self, "🎉 Success", "Verifier: I’m convinced! You passed all rounds.")
        self.parent_selector.update_trust_points(points_earned=3)
        self.close()
        self.parent_selector.show()

    def reset_game(self, preserve_round=False):
        self.committed = False
        self.node_colors.clear()
        self.commitments.clear()
        self.nonces.clear()

        for node in self.nodes.values():
            node.locked = False
            node.setBrush(QBrush(Qt.gray))

        if not preserve_round:
            self.rounds = 0
            self.update_narration("🔁 Game reset. Recolor and start again!")
        else:
            self.update_narration("🎨 Prover: Please recolor the graph for the next round.")

import sys
import subprocess
import hashlib
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGraphicsScene,
    QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem,
    QHBoxLayout, QScrollArea
)
from PyQt5.QtGui import QFont, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF, QLineF


class ZKPNode:
    def __init__(self, name, role_label, position, color):
        self.name = name
        self.role_label = role_label
        self.position = position
        self.color = color
        self.nonce = str(random.randint(10000, 99999))
        self.commitment = hashlib.sha256((role_label + self.nonce).encode()).hexdigest()
        self.revealed_role = role_label
        self.revealed_nonce = self.nonce


class NarrationEngine:
    @staticmethod
    def format_log(node1, node2, binding_ok, hiding_ok, binding_broken=False):
        log = f"""
🎥 Security Camera Activated: Monitoring link → {node1.name} ↔ {node2.name}

🔐 Commitments Submitted:
   • {node1.name} → SHA256(????) = {node1.commitment[:12]}...
   • {node2.name} → SHA256(????) = {node2.commitment[:12]}...

Challenge Issued → Reveal phase begins...

🔓 Revealed:
   • {node1.name} → \"{node1.revealed_role}\" with nonce = {node1.revealed_nonce}
   • {node2.name} → \"{node2.revealed_role}\" with nonce = {node2.revealed_nonce}

Recomputed Hashes:
"""
        if binding_broken:
            log += "   ❌ Mismatch detected — Binding broken!\n    Prover tried to change their role after committing.\n\n"
        else:
            log += "   ✅ Matches original commitments — Binding held.\n\n"

        if not binding_broken and hiding_ok:
            log += "✅ Hiding held — Verifier only learns that roles are different.\nZKP passed successfully.\n"
        elif not binding_broken and not hiding_ok:
            log += f"⚠️ Hiding broken — {node1.name} and {node2.name} revealed same role!\nZKP failed. Verifier now knows part of the secret mapping.\n"

        log += """
📘 Explanation:
- Binding ensures that once a role is committed with a hash, it can't be changed.
- Hiding ensures that the hash doesn't reveal the actual role until the reveal phase.
- If two adjacent nodes share the same role, it can indicate a conflict of interest or security flaw.
  For example, if an ATM and a Validator are the same role, one could validate its own transaction.
  This breaks the fundamental principle of role separation in secure systems.
"""
        return log


class SceneZKPGraph(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 ZKP Graph Simulation - Security Log Mode")
        self.setGeometry(150, 100, 1100, 750)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("background-color: #1e1e1e; border: none;")

        # Scrollable narration box
        self.text_output = QLabel()
        self.text_output.setWordWrap(True)
        self.text_output.setFont(QFont("Courier New", 12))
        self.text_output.setStyleSheet("background-color: #1c1c1c; padding: 10px; border: 1px solid #444; color: white;")
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.text_output)
        scroll.setMinimumHeight(250)

        self.verify_button = QPushButton("🎯 Simulate ZKP Verification")
        self.verify_button.setFont(QFont("Arial", 14))
        self.verify_button.setStyleSheet("padding: 10px; background-color: #2d3436; color: white; border-radius: 8px;")
        self.verify_button.clicked.connect(self.reveal_connection)

        self.next_button = QPushButton("➡ Next: Scene 3 - Bipartate Graph")
        self.next_button.setFont(QFont("Arial", 13, QFont.Bold))
        self.next_button.setStyleSheet(
            "background-color: #0055ff; color: white; padding: 10px; border-radius: 10px;"
        )
        self.next_button.clicked.connect(self.go_to_next_scene)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.verify_button)
        layout.addWidget(scroll)

        # Center the button using a horizontal layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.nodes = []
        self.node_graphics = {}
        self.edges = []

        self.build_graph()

    def build_graph(self):
        layout = [
            ("ATM",         "Initiator", QPointF(150, 150), QColor("#e74c3c")),
            ("Validator",   "Validator", QPointF(500, 150), QColor("#f1c40f")),
            ("Merchant",    "Receiver",  QPointF(300, 350), QColor("#2ecc71")),
            ("Customer",    "Initiator", QPointF(850, 150), QColor("#e74c3c")),
            ("Treasury",    "Receiver",  QPointF(650, 400), QColor("#2ecc71")),
            ("Insider",     "Validator", QPointF(150, 450), QColor("#f1c40f"))
        ]

        connections = [(0, 1), (1, 2), (2, 4), (3, 1), (5, 2), (0, 5)]

        for name, role, pos, color in layout:
            node = ZKPNode(name, role, pos, color)
            self.nodes.append(node)

        for idx, node in enumerate(self.nodes):
            ellipse = QGraphicsEllipseItem(-30, -30, 60, 60)
            ellipse.setBrush(QBrush(Qt.gray))
            ellipse.setPen(QPen(Qt.white, 2))
            ellipse.setPos(node.position)
            self.scene.addItem(ellipse)

            lock = QGraphicsTextItem("🔐")
            lock.setFont(QFont("Arial", 16))
            lock.setDefaultTextColor(Qt.white)
            lock.setPos(node.position.x() - 10, node.position.y() - 55)
            self.scene.addItem(lock)

            label = QGraphicsTextItem(node.name)
            label.setFont(QFont("Arial", 12))
            label.setDefaultTextColor(Qt.white)
            label.setPos(node.position.x() - 30, node.position.y() + 35)
            self.scene.addItem(label)

            self.node_graphics[idx] = (ellipse, lock, label)

        for a, b in connections:
            p1 = self.nodes[a].position
            p2 = self.nodes[b].position
            line = QGraphicsLineItem(QLineF(p1, p2))
            line.setPen(QPen(Qt.white, 2))
            self.scene.addItem(line)
            self.edges.append((a, b))

    def reveal_connection(self):
        a, b = random.choice(self.edges)
        node1, node2 = self.nodes[a], self.nodes[b]

        self.node_graphics[a][0].setBrush(QBrush(node1.color))
        self.node_graphics[b][0].setBrush(QBrush(node2.color))

        recomputed_hash_1 = hashlib.sha256((node1.revealed_role + node1.revealed_nonce).encode()).hexdigest()
        recomputed_hash_2 = hashlib.sha256((node2.revealed_role + node2.revealed_nonce).encode()).hexdigest()

        binding_ok = (recomputed_hash_1 == node1.commitment and recomputed_hash_2 == node2.commitment)
        hiding_ok = node1.revealed_role != node2.revealed_role

        log = NarrationEngine.format_log(
            node1, node2,
            binding_ok=binding_ok,
            hiding_ok=hiding_ok,
            binding_broken=not binding_ok
        )
        self.text_output.setText(log)

    def go_to_next_scene(self):
        subprocess.Popen(["python", "scene3_bipartate.py"])
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SceneZKPGraph()
    window.show()
    sys.exit(app.exec_())

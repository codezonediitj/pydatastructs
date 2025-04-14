import sys
import hashlib
import secrets
import random
import networkx as nx
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QMessageBox, QHBoxLayout, QTextEdit, QGraphicsEllipseItem,
    QGraphicsTextItem, QColorDialog, QComboBox, QGraphicsScene, QGraphicsView,QDialog, QDialogButtonBox
)
from PyQt5.QtGui import QFont, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRectF

class CommitmentGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKP Commitment Game - Master Edition")
        self.setGeometry(100, 100, 1200, 700)

        self.graph = nx.cycle_graph(5)
        self.colors = {}
        self.commitments = {}
        self.nonces = {}
        self.revealed = set()

        self.init_ui()
        self.draw_graph()

    def init_ui(self):
        layout = QHBoxLayout()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view, 70)

        control_panel = QVBoxLayout()

        self.commit_button = QPushButton("🔒 Commit to Colors")
        self.commit_button.clicked.connect(self.commit_colors)
        control_panel.addWidget(self.commit_button)

        self.challenge_button = QPushButton("🎯 Verifier: Challenge Random Edge")
        self.challenge_button.clicked.connect(self.challenge_edge)
        control_panel.addWidget(self.challenge_button)

        self.cheat_button = QPushButton("😈 Try to Cheat (Change Color)")
        self.cheat_button.clicked.connect(self.try_to_cheat)
        control_panel.addWidget(self.cheat_button)

        self.education_button = QPushButton("🧠 What’s Happening?")
        self.education_button.clicked.connect(self.show_education_modal)
        control_panel.addWidget(self.education_button)

        self.color_select = QComboBox()
        self.color_select.addItems(["Red", "Green", "Blue"])
        control_panel.addWidget(QLabel("Choose color for next node click:"))
        control_panel.addWidget(self.color_select)

        self.status = QLabel("🔐 Set colors by clicking nodes. Then commit.")
        self.status.setWordWrap(True)
        control_panel.addWidget(self.status)

        self.transcript = QTextEdit()
        self.transcript.setReadOnly(True)
        self.transcript.setFont(QFont("Courier", 10))
        control_panel.addWidget(QLabel("📝 ZKP Transcript:"))
        control_panel.addWidget(self.transcript)

        layout.addLayout(control_panel, 30)
        self.setLayout(layout)

    def draw_graph(self):
        self.scene.clear()
        self.pos = nx.spring_layout(self.graph, seed=42)
        self.node_items = {}

        for node in self.graph.nodes:
            x, y = self.pos[node]
            x, y = x * 300 + 300, y * 300 + 200
            ellipse = QGraphicsEllipseItem(QRectF(x, y, 40, 40))
            ellipse.setBrush(QBrush(Qt.lightGray))
            ellipse.setPen(QPen(Qt.black))
            ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
            ellipse.mousePressEvent = lambda event, n=node: self.set_node_color(n)
            self.scene.addItem(ellipse)

            label = QGraphicsTextItem(str(node))
            label.setPos(x + 12, y + 10)
            self.scene.addItem(label)

            self.node_items[node] = (ellipse, label)

        for u, v in self.graph.edges:
            x1, y1 = self.pos[u]
            x2, y2 = self.pos[v]
            x1, y1 = x1 * 300 + 320, y1 * 300 + 220
            x2, y2 = x2 * 300 + 320, y2 * 300 + 220
            self.scene.addLine(x1, y1, x2, y2, QPen(Qt.black))

    def set_node_color(self, node):
        color = self.color_select.currentText()
        self.colors[node] = color
        ellipse, _ = self.node_items[node]
        ellipse.setBrush(QBrush(QColor(color)))
        self.status.setText(f"🎨 Node {node} set to {color} (only you know this)")
        self.transcript.append(f"[Prover] Sets node {node} to {color}")

    def commit_colors(self):
        self.commitments.clear()
        self.nonces.clear()
        self.revealed.clear()

        missing = [n for n in self.graph.nodes if n not in self.colors]
        if missing:
            self.status.setText(f"⚠️ Color all nodes first! Missing: {missing}")
            return

        for node, color in self.colors.items():
            nonce = secrets.token_hex(8)
            self.nonces[node] = nonce
            self.commitments[node] = hashlib.sha256((color + nonce).encode()).hexdigest()
            ellipse, _ = self.node_items[node]
            ellipse.setBrush(QBrush(Qt.darkGray))
            self.transcript.append(f"[Prover] Commits to node {node} with hash = {self.commitments[node]}")

        self.status.setText("🔒 All node colors committed! Verifier may now challenge an edge.")

    def challenge_edge(self):
        edge = random.choice(list(self.graph.edges))
        u, v = edge

        if u in self.revealed or v in self.revealed:
            self.status.setText("⏭️ This edge was already revealed. Try again.")
            return

        self.revealed.update([u, v])
        result = self.reveal_and_verify(u, v)
        self.status.setText(result)

    def reveal_and_verify(self, u, v):
        color_u, color_v = self.colors[u], self.colors[v]
        nonce_u, nonce_v = self.nonces[u], self.nonces[v]

        commit_u = hashlib.sha256((color_u + nonce_u).encode()).hexdigest()
        commit_v = hashlib.sha256((color_v + nonce_v).encode()).hexdigest()

        self.transcript.append(f"\n[Verifier] Challenges edge ({u}, {v})")
        self.transcript.append(f"→ Prover reveals: node {u} = {color_u}, nonce = {nonce_u}")
        self.transcript.append(f"→ Prover reveals: node {v} = {color_v}, nonce = {nonce_v}")
        self.transcript.append(f"→ Verifier recomputes H({color_u}||{nonce_u}) = {commit_u}")
        self.transcript.append(f"→ Verifier recomputes H({color_v}||{nonce_v}) = {commit_v}")

        if commit_u != self.commitments[u] or commit_v != self.commitments[v]:
            self.transcript.append("❌ Commitment mismatch! Binding property violated!")
            return "🚨 Verification Failed! Commitment mismatch (binding broken)"

        if color_u == color_v:
            self.transcript.append("❌ Same color for both nodes! Invalid coloring.")
            return "❌ Verification Failed! Adjacent nodes have same color."

        ellipse_u, _ = self.node_items[u]
        ellipse_v, _ = self.node_items[v]
        ellipse_u.setBrush(QBrush(QColor(color_u)))
        ellipse_v.setBrush(QBrush(QColor(color_v)))

        self.transcript.append("✅ Commitment verified. Coloring valid for edge.")
        return f"✅ Edge ({u}, {v}) verified! {color_u} ≠ {color_v}"

    def try_to_cheat(self):
        if not self.commitments:
            self.status.setText("⚠️ Commit first before cheating.")
            return

        node = random.choice(list(self.graph.nodes))
        new_color = random.choice([c for c in ["Red", "Green", "Blue"] if c != self.colors[node]])
        self.colors[node] = new_color

        self.status.setText(f"😈 Prover changed color of node {node} to {new_color} post-commit. Now try verifying it!")
        self.transcript.append(f"🚨 [Prover] Illegally changed color of node {node} to {new_color} after committing!")

    def show_education_modal(self):
        modal = QDialog(self)
        modal.setWindowTitle("🔍 Understanding Commitment Schemes")
        layout = QVBoxLayout()

        explanation = QLabel("""
        🔐 Commitment Schemes
        --------------------------
        ✔️ Hiding: The verifier cannot know the secret until you reveal it.
        ✔️ Binding: You cannot change your mind after committing.

        Example:
        - You commit to a color by hashing it with a random nonce.
        - You lock that value and show the lock to the verifier.
        - Later, you reveal the color + nonce.
        - Verifier checks if the lock matches the key.

        🚫 Hash Collisions: Very unlikely two different messages give same hash.
        
        That's why commitment = secrecy + honesty.
        """)
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(modal.accept)
        layout.addWidget(button_box)

        modal.setLayout(layout)
        modal.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CommitmentGame()
    window.show()
    sys.exit(app.exec_())
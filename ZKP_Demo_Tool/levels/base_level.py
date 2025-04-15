import random
import hashlib
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsScene, QGraphicsView,
    QHBoxLayout, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit
)
from PyQt5.QtGui import QFont, QBrush, QColor, QPen, QTextCursor
from PyQt5.QtCore import Qt, QPointF, QTimer

from ui.node_item import NodeItem

class BaseLevel(QWidget):
    def __init__(self, level_name, parent_selector, max_rounds=3, auto_mode=False, auto_rounds=5):
        super().__init__()
        self.level_name = level_name
        self.parent_selector = parent_selector
        self.max_rounds = max_rounds
        self.auto_mode = auto_mode
        self.auto_rounds = auto_rounds
        self.rounds = 0
        self.committed = False

        self.valid_proofs = 0
        self.invalid_proofs = 0
        self.demo_phase = True
        self.auto_total_rounds = auto_rounds * 2

        self.node_colors = {}
        self.commitments = {}
        self.nonces = {}
        self.nodes = {}
        self.edges = []

        self.setWindowTitle(f"{level_name} - ZKP Game")
        self.setGeometry(100, 100, 900, 700)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.narration = QLabel(f"👩‍💼 Prover: Color nodes secretly to convince the Verifier!")
        self.narration.setFont(QFont("Arial", 14, QFont.Bold))
        self.narration.setStyleSheet("color: white;")
        self.layout.addWidget(self.narration)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: #1c1c1c; color: white; font-weight: bold; font-size: 13px;")
        self.log_box.setFont(QFont("Consolas", 12))
        self.log_box.setFixedHeight(150)
        self.layout.addWidget(self.log_box)

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
        if self.auto_mode:
            QTimer.singleShot(1000, self.auto_run_verification)
    def update_narration(self, text):
        self.narration.setText(text)
    def log(self, message):
        self.log_box.append(f"➡️ {message}")
        self.log_box.moveCursor(QTextCursor.End)


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

    def randomly_color_nodes(self, allow_collision=False):
        palette = ["#e74c3c", "#2ecc71", "#f1c40f", "#3498db"]
        self.node_colors.clear()
        used = {}
        for node_id, node in self.nodes.items():
            if not allow_collision:
                color = palette[node_id % len(palette)]
            else:
                color = random.choice(palette)
            self.node_colors[node_id] = color
            node.setBrush(QBrush(QColor(color)))
            self.log(f"Node {node_id} colored {color}")

    def commit_colors(self, auto_trigger=False):
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
            self.log(f"Node {node_id} locked with hidden commitment")

        self.committed = True
        if not auto_trigger:
            self.update_narration("🔒 Commitments made. Verifier, choose an edge to challenge!")

    def challenge_edge_once(self, auto=False):
        if not self.committed:
            if not auto:
                QMessageBox.warning(self, "⚠️ Commit First", "You must commit before challenging.")
            return

        edge = random.choice(self.edges)
        node1, node2 = edge
        color1 = self.node_colors.get(node1)
        color2 = self.node_colors.get(node2)

        self.nodes[node1].setBrush(QBrush(QColor(color1)))
        self.nodes[node2].setBrush(QBrush(QColor(color2)))
        self.log(f"Verifier opens edge {edge}: Node {node1} = {color1}, Node {node2} = {color2}")

        if color1 == color2:
            self.invalid_proofs += 1
            result = f"❌ Verifier: Edge {edge} has same colors. Proof fails!"
            self.update_narration(result)
        else:
            self.valid_proofs += 1
            result = f"✅ Verifier: Edge {edge} looks good."
        self.rounds += 1

        self.update_narration(result + f" Round {self.rounds}/{self.auto_total_rounds}")

        if not self.auto_mode:
            if self.rounds < self.max_rounds:
                QTimer.singleShot(1500, self.prompt_next_round)
            else:
                QTimer.singleShot(1500, self.finish_level)

    def auto_run_verification(self):
        if self.rounds >= self.auto_total_rounds:
            QTimer.singleShot(1000, self.show_final_report)
            return

        allow_collision = False if self.rounds < self.auto_rounds else True
        self.randomly_color_nodes(allow_collision=allow_collision)
        self.update_narration(f"🎨 Round {self.rounds + 1}: Auto-coloring graph...")
        QTimer.singleShot(1000, self.auto_commit_step)

    def auto_commit_step(self):
        self.commit_colors(auto_trigger=True)
        QTimer.singleShot(1000, self.auto_challenge_step)

    def auto_challenge_step(self):
        self.challenge_edge_once(auto=True)
        QTimer.singleShot(1500, self.auto_run_verification)

    def show_final_report(self):
        total = self.valid_proofs + self.invalid_proofs
        success_rate = (self.valid_proofs / total) * 100 if total > 0 else 0

        msg = QMessageBox()
        msg.setWindowTitle("📊 Simulation Summary")
        msg.setText(f"✅ Valid Proofs: {self.valid_proofs}\n❌ Invalid Proofs: {self.invalid_proofs}\n\n"
                      f"🎯 Success Probability: {success_rate:.2f}%")
        msg.exec_()
        self.finish_level()

    def prompt_next_round(self):
        QMessageBox.information(
            self,
            "🎯 Round Complete",
            "Round complete! Please recolor the graph to start the next round."
        )
        self.reset_game(preserve_round=True)

    def finish_level(self):
        self.parent_selector.update_trust_points(points_earned=3)
        self.close()
        self.parent_selector.show()

    def reject_proof(self):
        QMessageBox.critical(self, "❌ Proof Rejected", "Verifier: The proof failed. I cannot be convinced.")
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
            self.valid_proofs = 0
            self.invalid_proofs = 0
            self.update_narration("🔁 Game reset. Recolor and start again!")
            self.log_box.clear()
        else:
            self.update_narration("🎨 Prover: Please recolor the graph for the next round.")
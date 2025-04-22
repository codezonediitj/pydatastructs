import random
import hashlib
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsScene, QGraphicsView,
    QHBoxLayout, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem, QTextEdit,
    QDialog, QRadioButton, QButtonGroup, QSpinBox, QGraphicsTextItem, QGraphicsLineItem
)
from PyQt5.QtGui import QFont, QBrush, QColor, QPen, QTextCursor
from PyQt5.QtCore import Qt, QPointF, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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
        self.graph = {}
        self.scene = QGraphicsScene()
        self.nodes = {}
        self.edges = []
        self.graph_nodes = {}
        self.valid_proofs = 0
        self.invalid_proofs = 0
        self.auto_total_rounds = 0
        self.node_colors = {}
        self.commitments = {}
        self.nonces = {}

        self.setWindowTitle(f"{level_name} - ZKP Game")
        self.setGeometry(100, 100, 900, 700)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.narration = QLabel("Prover: Color nodes secretly to convince the Verifier!")
        self.narration.setFont(QFont("Arial", 14, QFont.Bold))
        self.narration.setStyleSheet("color: white;")
        self.layout.addWidget(self.narration)

        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: #1c1c1c; color: white; font-weight: bold; font-size: 13px;")
        font = QFont("Consolas", 12)
        if not font.exactMatch():
            font = QFont("Courier New", 12)
        self.log_box.setFont(font)
        self.log_box.setFixedHeight(150)
        self.layout.addWidget(self.log_box)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.figure = Figure(figsize=(5, 2.5))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.success_rates = []
        self.round_numbers = []
        self.ax.set_title("ZKP Success Rate Over Rounds")
        self.ax.set_xlabel("Rounds")
        self.ax.set_ylabel("Success %")
        self.ax.set_ylim(0, 100)
        self.layout.addWidget(self.canvas)

        self.buttons_layout = QHBoxLayout()
        self.commit_btn = QPushButton("Commit")
        self.challenge_btn = QPushButton("Challenge")
        self.reset_btn = QPushButton("Reset")
        self.commit_btn.clicked.connect(self.commit_colors)
        self.challenge_btn.clicked.connect(self.challenge_edge_once)
        self.reset_btn.clicked.connect(self.reset_game)
        self.buttons_layout.addWidget(self.commit_btn)
        self.buttons_layout.addWidget(self.challenge_btn)
        self.buttons_layout.addWidget(self.reset_btn)
        self.layout.addLayout(self.buttons_layout)

        if hasattr(self, 'show_education_modal'):
            self.show_education_modal()
        if hasattr(self, 'ask_mode_selection'):
            self.ask_mode_selection()
        if self.auto_mode:
            self.auto_total_rounds = self.auto_rounds
            QTimer.singleShot(1000, self.auto_run_verification)
        self.base_coloring = {
            0: 0, 1: 1, 2: 2,
            3: 0, 4: 1, 5: 2,
            6: 0, 7: 1
        }

    def add_node(self, node_id, pos, label=None):
        from ui.node_item import NodeItem  # Make sure this is imported

        node = NodeItem(node_id, pos, parent=self)

        # Attach label to node (if provided)
        if label:
            node.setToolTip(label)
            node.set_label(label)  # We'll add this method next

        self.nodes[node_id] = node
        self.graph_nodes[node_id] = node
        self.scene.addItem(node)

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.edges.append((u, v))
        node_u = self.graph_nodes[u]
        node_v = self.graph_nodes[v]
        line = QGraphicsLineItem(
            node_u.pos().x(), node_u.pos().y(),
            node_v.pos().x(), node_v.pos().y()
        )
        pen = QPen(Qt.black)
        pen.setWidth(2)
        line.setPen(pen)
        self.scene.addItem(line)

    def challenge_edge_once(self, auto=False):
        if not self.committed:
            if not auto:
                QMessageBox.warning(self, "Commit First", "You must commit before challenging.")
            return
        edge = random.choice(self.edges)
        node1, node2 = edge
        color1 = self.node_colors.get(node1)
        color2 = self.node_colors.get(node2)
        self.nodes[node1].setBrush(QBrush(QColor(color1)))
        self.nodes[node2].setBrush(QBrush(QColor(color2)))
        self.log(f"Verifier checks edge {edge}")
        recomputed1 = hashlib.sha256((color1 + self.nonces[node1]).encode()).hexdigest()
        recomputed2 = hashlib.sha256((color2 + self.nonces[node2]).encode()).hexdigest()
        valid1 = recomputed1 == self.commitments[node1]
        valid2 = recomputed2 == self.commitments[node2]
        if not valid1:
            self.log(f"\u274c Non-repudiation failed for node {node1}")
            self.nodes[node1].pulse_red()
        if not valid2:
            self.log(f"\u274c Non-repudiation failed for node {node2}")
            self.nodes[node2].pulse_red()
        if not valid1 or not valid2:
            self.update_narration("Non-repudiation breach detected. Proof invalid.")
            self.invalid_proofs += 1
        elif color1 == color2:
            self.invalid_proofs += 1
            self.update_narration(f"Proof failed: same color on edge {edge}.")
        else:
            self.valid_proofs += 1
            self.update_narration(f"Proof accepted: edge {edge} is valid. Round {self.rounds}/{self.auto_total_rounds}")
        self.update_success_chart()

    def reset_game(self, preserve_round=False):
        self.committed = False
        self.node_colors.clear()
        self.commitments.clear()
        self.nonces.clear()
        for node in self.nodes.values():
            node.unlock()
            node.hide_hash()
        if not preserve_round:
            self.rounds = 0
            self.valid_proofs = 0
            self.invalid_proofs = 0
            self.log_box.clear()
            self.update_narration("Game reset. Recolor to start.")
        else:
            self.update_narration("Recolor to begin next round.")

    def update_narration(self, text):
        self.narration.setText(text)

    def log(self, message):
        self.log_box.append(f"\u27a1\ufe0f {message}")
        self.log_box.moveCursor(QTextCursor.End)

    def update_success_chart(self):
        total_rounds = self.valid_proofs + self.invalid_proofs
        if total_rounds == 0:
            return
        success_rate = (self.valid_proofs / total_rounds) * 100
        self.success_rates.append(success_rate)
        self.round_numbers.append(total_rounds)
        self.ax.clear()
        self.ax.plot(self.round_numbers, self.success_rates, marker='o')
        self.ax.set_title("ZKP Success Rate Over Rounds")
        self.ax.set_xlabel("Rounds")
        self.ax.set_ylabel("Success %")
        self.ax.set_ylim(0, 100)
        self.canvas.draw()

    def apply_random_permuted_coloring(self):
        palette = ["#e74c3c", "#2ecc71", "#f1c40f"]
        perm = palette.copy()
        random.shuffle(perm)
        self.node_colors.clear()
        for node_id, color_index in self.base_coloring.items():
            hex_color = perm[color_index]
            self.node_colors[node_id] = hex_color
            self.nodes[node_id].setBrush(QBrush(QColor(hex_color)))
            self.log(f"Node {node_id} colored {hex_color}")

    def commit_colors(self, auto_trigger=False):
        if any(nid not in self.node_colors for nid in self.nodes):
            self.update_narration("Please color all nodes first.")
            return
        self.commitments.clear()
        self.nonces.clear()
        for node_id, color in self.node_colors.items():
            nonce = str(random.randint(1000, 9999))
            color_str = color.name() if isinstance(color, QColor) else str(color)
            commitment = hashlib.sha256((color_str + nonce).encode()).hexdigest()
            self.commitments[node_id] = commitment
            self.nonces[node_id] = nonce
            node = self.nodes[node_id]
            node.lock()
            short_hash = commitment[:6] + "..."
            node.show_hash(short_hash)
        self.committed = True
        if not auto_trigger:
            self.update_narration("Commitments made. Verifier, choose an edge to challenge!")
import sys
import hashlib
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGraphicsScene,
    QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem,
    QHBoxLayout, QTextEdit
)
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt, QPointF

class Node(QGraphicsEllipseItem):
    def __init__(self, name, pos, color, node_type, description=""):
        super().__init__(-30, -30, 60, 60)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.white, 2))
        self.setPos(pos)
        self.name = name
        self.node_type = node_type
        self.description = description

        self.label = QGraphicsTextItem(name)
        self.label.setDefaultTextColor(Qt.white)
        self.label.setFont(QFont("Arial", 8))
        self.label.setParentItem(self)
        self.label.setPos(-30, 40)

class Edge:
    def __init__(self, scene, node1, node2):
        self.line = QGraphicsLineItem(node1.x(), node1.y(), node2.x(), node2.y())
        self.line.setPen(QPen(Qt.gray, 2, Qt.SolidLine))
        scene.addItem(self.line)
        self.nodes = (node1, node2)

class ZKPVerifierExplained(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 ZKP Simulation with Verifier Explanation")
        self.setGeometry(100, 100, 1300, 850)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        self.statement_label = QLabel("🎓 Knowledge Statement: 'I know (u, v) ∈ G such that employee u has access to account v.'")
        self.statement_label.setStyleSheet("padding: 8px; font-size: 16px;")
        self.layout.addWidget(self.statement_label)

        self.protocol_log = QTextEdit()
        self.protocol_log.setReadOnly(True)
        self.protocol_log.setStyleSheet("background-color: #111; color: #ddd; font-family: monospace;")
        self.layout.addWidget(self.protocol_log)

        self.button_layout = QHBoxLayout()
        self.commit_button = QPushButton("🔐 Step 1: Commit to Secret Edge")
        self.challenge_account_btn = QPushButton("Step 2: Reveal Account")
        self.challenge_employee_btn = QPushButton("Step 2: Reveal Employee")
        self.challenge_account_btn.setEnabled(False)
        self.challenge_employee_btn.setEnabled(False)
        self.button_layout.addWidget(self.commit_button)
        self.button_layout.addWidget(self.challenge_account_btn)
        self.button_layout.addWidget(self.challenge_employee_btn)
        self.layout.addLayout(self.button_layout)

        self.commit_button.clicked.connect(self.commit_phase)
        self.challenge_account_btn.clicked.connect(lambda: self.reveal("account"))
        self.challenge_employee_btn.clicked.connect(lambda: self.reveal("employee"))

        self.accounts = []
        self.employees = []
        self.edges = []
        self.secret_edge = None
        self.nonce = None
        self.commitment = None

        self.build_graph()

    def build_graph(self):
        account_data = [
            ("Vault#011", "$800K"),
            ("Account#992", "Suspicious Flow"),
            ("Loan#743", "Offshore Link")
        ]

        emp_data = [
            ("Alice", "Teller - Branch A"),
            ("Bob", "Manager - HQ"),
            ("Claire", "Auditor - Internal Affairs")
        ]

        for i, (name, desc) in enumerate(account_data):
            node = Node(name, QPointF(200, 100 + i * 200), QColor("gold"), "account", desc)
            self.accounts.append(node)
            self.scene.addItem(node)

        for i, (name, desc) in enumerate(emp_data):
            node = Node(name, QPointF(1000, 100 + i * 200), QColor("skyblue"), "employee", desc)
            self.employees.append(node)
            self.scene.addItem(node)

        access_list = [
            (0, 0),
            (1, 1),
            (2, 2),
            (0, 1)
        ]

        for a_idx, e_idx in access_list:
            self.edges.append(Edge(self.scene, self.accounts[a_idx], self.employees[e_idx]))

    def commit_phase(self):
        self.secret_edge = random.choice(self.edges)
        u, v = self.secret_edge.nodes
        self.nonce = str(random.randint(100000, 999999))
        combined = u.name + v.name + self.nonce
        self.commitment = hashlib.sha256(combined.encode()).hexdigest()

        self.protocol_log.clear()
        self.protocol_log.append("🔐 [Commit Phase]")
        self.protocol_log.append(f"Secret Edge: {u.name} ↔ {v.name} (kept hidden)")
        self.protocol_log.append(f"Nonce (random salt): {self.nonce}")
        self.protocol_log.append(f"Commitment = SHA256({u.name} + {v.name} + nonce)")
        self.protocol_log.append(f"→ {self.commitment}\n")

        self.challenge_account_btn.setEnabled(True)
        self.challenge_employee_btn.setEnabled(True)

    def reveal(self, challenge_type):
        u, v = self.secret_edge.nodes
        self.protocol_log.append(f" [Challenge Phase] Verifier asks to reveal: {challenge_type.upper()}")

        if challenge_type == "account":
            revealed = u.name
            self.protocol_log.append(f"Prover reveals: {revealed} + nonce")
            self.protocol_log.append("\nVerifier tries every employee to match the hash:")
            for emp in self.employees:
                trial = hashlib.sha256((u.name + emp.name + self.nonce).encode()).hexdigest()
                match = "✅ MATCH" if trial == self.commitment else "❌"
                self.protocol_log.append(f"  • H({u.name} + {emp.name} + {self.nonce}) → {trial[:20]}... {match}")
        else:
            revealed = v.name
            self.protocol_log.append(f"Prover reveals: {revealed} + nonce")
            self.protocol_log.append("\nVerifier tries every account to match the hash:")
            for acc in self.accounts:
                trial = hashlib.sha256((acc.name + v.name + self.nonce).encode()).hexdigest()
                match = "✅ MATCH" if trial == self.commitment else "❌"
                self.protocol_log.append(f"  • H({acc.name} + {v.name} + {self.nonce}) → {trial[:20]}... {match}")

        self.protocol_log.append("\n🛡️ If any match → verifier is convinced.")
        self.challenge_account_btn.setEnabled(False)
        self.challenge_employee_btn.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZKPVerifierExplained()
    window.show()
    sys.exit(app.exec_())

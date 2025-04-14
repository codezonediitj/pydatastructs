import sys
import hashlib
import secrets
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QMessageBox, QHBoxLayout, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class CommitmentGameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🔒 Commitment Game")
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: #2C3E50;")

        layout = QVBoxLayout()

        title = QLabel("🔐 Commitment Scheme Simulation")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: white; padding: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        role_label = QLabel("🧑‍💻 You are the Prover. The system plays the Verifier.")
        role_label.setStyleSheet("color: #ECF0F1; padding: 5px;")
        role_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(role_label)

        self.secret_input = QLineEdit()
        self.secret_input.setPlaceholderText("Enter your secret value")
        self.secret_input.setFont(QFont("Arial", 12))
        self.secret_input.setStyleSheet("padding: 8px;")
        layout.addWidget(self.secret_input)

        commit_btn = QPushButton("🔒 Commit to Secret")
        commit_btn.setFont(QFont("Arial", 12))
        commit_btn.setStyleSheet("margin: 10px; padding: 10px;")
        commit_btn.clicked.connect(self.generate_commitment)
        layout.addWidget(commit_btn)

        reveal_btn = QPushButton("🔓 Reveal to Verifier")
        reveal_btn.setFont(QFont("Arial", 12))
        reveal_btn.setStyleSheet("margin: 10px; padding: 10px;")
        reveal_btn.clicked.connect(self.reveal_secret)
        layout.addWidget(reveal_btn)

        self.commitment_label = QLabel("Commitment: ...")
        self.commitment_label.setStyleSheet("color: #ECF0F1; margin: 10px;")
        layout.addWidget(self.commitment_label)

        self.transcript_box = QTextEdit()
        self.transcript_box.setReadOnly(True)
        self.transcript_box.setStyleSheet("background-color: #34495E; color: #F1C40F; padding: 10px;")
        layout.addWidget(self.transcript_box)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: #1ABC9C; font-weight: bold; padding: 10px;")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

        self.nonce = None
        self.commitment = None

    def generate_commitment(self):
        secret = self.secret_input.text().strip()
        if not secret:
            QMessageBox.warning(self, "Input Error", "Please enter a secret value.")
            return

        self.nonce = secrets.token_hex(8)
        combined = secret + self.nonce
        self.commitment = hashlib.sha256(combined.encode()).hexdigest()

        self.commitment_label.setText(f"Commitment: {self.commitment}")
        self.transcript_box.clear()
        self.transcript_box.append("Prover commits to a secret using SHA-256(secret || nonce)")
        self.transcript_box.append(f"nonce: {self.nonce}")
        self.transcript_box.append("Commitment sent to Verifier")
        self.result_label.setText("✅ Secret committed. You may now reveal.")
        self.result_label.setStyleSheet("color: #1ABC9C; font-weight: bold; padding: 10px;")

    def reveal_secret(self):
        if not self.commitment:
            QMessageBox.warning(self, "No Commitment", "Please commit to a value first.")
            return

        secret = self.secret_input.text().strip()
        combined = secret + self.nonce
        check = hashlib.sha256(combined.encode()).hexdigest()

        self.transcript_box.append("\nProver reveals the secret and nonce...")
        self.transcript_box.append(f"secret: {secret}")
        self.transcript_box.append(f"recomputed hash: {check}")

        if check == self.commitment:
            self.result_label.setStyleSheet("color: #1ABC9C; font-weight: bold; padding: 10px;")
            self.result_label.setText("✅ Reveal successful. Verifier is convinced.")
            self.transcript_box.append("Verifier confirms: ✅ commitment is valid!")
        else:
            self.result_label.setStyleSheet("color: red; font-weight: bold; padding: 10px;")
            self.result_label.setText("❌ Reveal failed. Commitment mismatch.")
            self.transcript_box.append("Verifier says: ❌ mismatch in commitment!")

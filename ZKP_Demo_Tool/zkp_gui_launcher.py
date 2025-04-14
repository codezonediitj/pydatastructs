# launcher.py (updated to use new level selector)

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from ui.level_selector import LevelSelector


class ZKPGUILauncher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ZKP Learning Playground")
        self.setFixedSize(400, 320)
        self.setStyleSheet("background-color: #2C3E50;")

        layout = QVBoxLayout()

        # Title label
        title = QLabel("🎓 Zero-Knowledge Proof Playground")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: white; padding: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Button style
        button_style = """
            QPushButton {
                background-color: #34495E;
                color: #ECF0F1;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3D566E;
            }
        """

        buttons = [
            ("🔐 Commitment Puzzle Book", self.commitment_game),
            ("👥 Prover-Verifier ZKP", self.zkp_game),
            ("🎭 Indistinguishability Game", self.ind_game)
        ]

        for label, handler in buttons:
            btn = QPushButton(label)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet(button_style)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        self.setLayout(layout)

    def commitment_game(self):
        self.level_selector = LevelSelector()
        self.level_selector.show()

    def zkp_game(self):
        QMessageBox.information(self, "Coming Soon", "👥 Prover-Verifier ZKP Game will launch here!")

    def ind_game(self):
        QMessageBox.information(self, "Coming Soon", "🎭 Indistinguishability Game will launch here!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZKPGUILauncher()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt
from commitment_game import CommitmentGame
class ZKPGUILauncher(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ZKP Learning Playground")
        self.setFixedSize(400, 320)
        self.setStyleSheet("background-color: #2C3E50;")

        layout = QVBoxLayout()

        # Title label
        title = QLabel("\ud83c\udf93 Zero-Knowledge Proof Playground")
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
            ("\ud83d\udd10 Commitment Game", self.commitment_game),
            ("\ud83d\udc65 Prover-Verifier ZKP", self.zkp_game),
            ("\ud83c\udfad Indistinguishability Game", self.ind_game)
        ]

        for label, handler in buttons:
            btn = QPushButton(label)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet(button_style)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

        self.setLayout(layout)

    def commitment_game(self):
        self.commit_window = CommitmentGame()
        self.commit_window.show()
    def zkp_game(self):
        QMessageBox.information(self, "Coming Soon", "\ud83d\udc65 Prover-Verifier ZKP Game will launch here!")

    def ind_game(self):
        QMessageBox.information(self, "Coming Soon", "\ud83c\udfad Indistinguishability Game will launch here!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZKPGUILauncher()
    window.show()
    sys.exit(app.exec_())

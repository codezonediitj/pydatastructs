import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ZKPSceneLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔐 Zero-Knowledge Proof Demo Launcher")
        self.setGeometry(300, 200, 500, 320)
        self.setStyleSheet("background-color: #1e1e1e; color: white;")

        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel("🎓 Launch a Scene")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Scene 1
        scene1_btn = QPushButton(" Scene 1: Introduction to Commitment")
        scene1_btn.clicked.connect(lambda: self.launch("tutorial_scene.py"))
        layout.addWidget(scene1_btn)

        # Scene 2
        scene2_btn = QPushButton("🎮 Scene 2: Commitment Game")
        scene2_btn.clicked.connect(lambda: self.launch("scene2_commitment.py"))
        layout.addWidget(scene2_btn)

        # Scene 3
        scene3_btn = QPushButton("🔀 Scene 3: Bipartite Graph ZKP")
        scene3_btn.clicked.connect(lambda: self.launch("scene3_bipartate.py"))
        layout.addWidget(scene3_btn)

        # Style all buttons
        for btn in [scene1_btn, scene2_btn, scene3_btn]:
            btn.setStyleSheet("padding: 12px; font-size: 14px; background-color: #2a2a2a; border-radius: 8px;")

        self.setLayout(layout)

    def launch(self, script_path):
        subprocess.Popen(["python", script_path])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = ZKPSceneLauncher()
    launcher.show()
    sys.exit(app.exec_())
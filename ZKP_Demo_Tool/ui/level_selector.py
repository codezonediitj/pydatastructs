# ui/level_selector.py
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGridLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from levels.level1_triangle import Level1Triangle
# We'll import level2_ring etc. later as they're written

class LevelSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKP Puzzle Game - Level Selector")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title = QLabel("🔐 Zero-Knowledge Proof Puzzle Book")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        self.layout.addWidget(title)

        self.instructions = QLabel("Earn Trust Points by completing levels to unlock the next!")
        self.instructions.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instructions)

        self.trust_points = 0
        self.level_buttons = []
        self.build_level_grid()

    def build_level_grid(self):
        grid = QGridLayout()
        levels = [
            {"name": "Level 1: Triangle", "required_points": 0, "function": self.load_level1},
            {"name": "Level 2: 5-Node Ring", "required_points": 3, "function": self.coming_soon},
            {"name": "Level 3: Bipartite Graph", "required_points": 6, "function": self.coming_soon},
            {"name": "Level 4: Social Network", "required_points": 9, "function": self.coming_soon}
        ]

        for i, level in enumerate(levels):
            btn = QPushButton(level["name"])
            if self.trust_points < level["required_points"]:
                btn.setEnabled(False)
                btn.setText(f"🔒 {level['name']} (Locked)")
            else:
                btn.clicked.connect(level["function"])
            self.level_buttons.append(btn)
            grid.addWidget(btn, i // 2, i % 2)

        self.layout.addLayout(grid)

    def load_level1(self):
        self.hide()
        self.level_window = Level1Triangle(parent_selector=self)
        self.level_window.show()

    def coming_soon(self):
        QMessageBox.information(self, "Locked Level", "Complete earlier levels to unlock this level!")

    def update_trust_points(self, points_earned):
        self.trust_points += points_earned
        QMessageBox.information(self, "Trust Points", f"You earned {points_earned} Trust Points!")
        self.rebuild()

    def rebuild(self):
        for btn in self.level_buttons:
            btn.setParent(None)
        self.level_buttons = []
        self.build_level_grid()

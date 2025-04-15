from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QGridLayout, QComboBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from levels.level2_bank_graph import Level2BankGraph
from ui.level_card import create_level_card

class LevelSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKP Puzzle Game - Level Selector")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        title_label = QLabel("🔒 The ZKP Puzzle Book")
        title_label.setFont(QFont("Cochin", 24, QFont.Bold))
        title_label.setStyleSheet("color: gold;")
        title_label.setAlignment(Qt.AlignCenter)

        self.instructions = QLabel("Earn Trust Points by completing levels to unlock the next!")
        self.instructions.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.instructions)

        self.round_mode_dropdown = QComboBox()
        self.round_mode_dropdown.addItems([
            "Manual Mode",
            "Auto Mode - 5 Rounds",
            "Auto Mode - 10 Rounds",
            "Auto Mode - 20 Rounds"
        ])
        self.layout.addWidget(self.round_mode_dropdown)

        self.trust_points = 0
        self.level_buttons = []
        self.build_level_grid()

    def build_level_grid(self):
        # Horizontal layout or grid for cards
        card_layout = QHBoxLayout()

        

        # Level 2: Unlocks after 3 trust points
        level2_card = create_level_card(
            parent=self,
            title="Level 2: 5-Node Ring",
            description="Demonstrate your skill on a cyclic 5-node graph with non-repeating color constraints.",
            button_label="Play Now",
            unlock_condition_met=(self.trust_points >= 3),
            launch_function=self.load_level2
        )

        # Add cards to layout
        
        card_layout.addWidget(level2_card)

        # Then add to main layout in your init or builder method:
        self.layout.addLayout(card_layout)
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(20)
        bottom_layout.setContentsMargins(20, 20, 20, 20)
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["⌨️ Manual Mode", "🤖 Auto Mode"])
        self.mode_selector.setFixedHeight(40)
        self.mode_selector.setStyleSheet("""
            QComboBox {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 5px 10px;
                border-radius: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
        """)
        bottom_layout.addWidget(self.mode_selector)

        grid = QGridLayout()
        levels = [
            {"name": "💠 Level 2.5: Multi-Path Challenge", "required_points": 0, "function": self.load_level2, "color": "#27ae60"}
        ]

        for i, level in enumerate(levels):
            button = QPushButton(level["name"])

            if self.trust_points >= level["required_points"]:
                button.setEnabled(True)
                button.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {level['color']};
                        color: white;
                        font-weight: bold;
                        font-size: 16px;
                        padding: 15px;
                        border-radius: 10px;
                        border: 2px solid white;
                    }}
                    QPushButton:hover {{
                        background-color: #2c3e50;
                        border: 2px solid gold;
                    }}
                """)
                button.clicked.connect(level["function"])
            else:
                button.setEnabled(False)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #444;
                        color: #aaa;
                        font-weight: bold;
                        font-size: 16px;
                        padding: 15px;
                        border-radius: 10px;
                        border: 2px dashed gray;
                    }
                """)
                button.setToolTip(f"🔒 Requires {level['required_points']} Trust Points to unlock.")

            grid.addWidget(button, 0, i)

        
        self.layout.addLayout(grid)

    def update_trust_points(self, points_earned):
        self.trust_points += points_earned
        QMessageBox.information(self, "Trust Points", f"You earned {points_earned} Trust Points!")
        self.rebuild()

    def rebuild(self):
        for btn in self.level_buttons:
            btn.setParent(None)
        self.level_buttons = []
        self.build_level_grid()

    def get_round_mode(self):
        mode_text = self.round_mode_dropdown.currentText()
        if "Manual" in mode_text:
            return False, 3
        elif "5" in mode_text:
            return True, 5
        elif "10" in mode_text:
            return True, 10
        else:
            return True, 20

    def load_level2(self):
        self.hide()
        auto_mode, auto_rounds = self.get_round_mode()
        self.level_window = Level2BankGraph(parent_selector=self, auto_mode=auto_mode, auto_rounds=auto_rounds)

        self.level_window.show()
    

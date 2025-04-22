from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QPixmap, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QResource


class ZKPTutorial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKP Animated Tutorial - Scene 1")
        self.setGeometry(300, 200, 900, 650)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.init_ui()
        self.animate_scene()

    def init_ui(self):
        # Main layout
        self.layout = QVBoxLayout()

        # Title
        self.title_label = QLabel("\u2728 Scene 1: Roles in the Network")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.layout.addWidget(self.title_label)

        # Image area (placeholder)
        self.image_label = QLabel()
        pixmap = QPixmap("../assets/scene1.png")
        if pixmap.isNull():
            self.image_label.setText("[Visual Story: ATM, Bank, Merchant cartoon goes here]")
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setFont(QFont("Arial", 16, QFont.Bold))
        else:
            self.image_label.setPixmap(pixmap.scaled(720, 360, Qt.KeepAspectRatio))
            self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Narration text
        self.narration_label = QLabel()
        self.narration_label.setWordWrap(True)
        self.narration_label.setFont(QFont("Georgia", 16))
        self.narration_label.setAlignment(Qt.AlignLeft)
        self.narration_label.setText(
            "<p>✨ <b>Every adventure needs a team —</b><br>"
            "and in the world of secure transactions, three heroes take the stage!</p>"

            "<p>🟦 <b>Initiator</b> starts the quest:<br>"
            "They say, “I want to make a move!” 💸</p>"

            "<p>🔺 <b>Validator</b> checks the map:<br>"
            "“Is this legit? Let me verify...” 🔍</p>"

            "<p>🟩 <b>Receiver</b> opens the treasure chest:<br>"
            "“It’s real. I’m in. Transaction complete!” </p>"

            "<p>But here's the twist…<br>"
            "<b>What if we could prove we did everything right —</b><br>"
            "💡 <i>without showing the treasure itself?</i></p>"

            "<p>That’s where <b>Zero-Knowledge Proofs</b> enter the story.<br>"
            " Ready to see some cryptographic magic?</p>"
        )
        self.layout.addWidget(self.narration_label)

        # Navigation button
        self.next_button = QPushButton("▶ Next")
        self.next_button.setFont(QFont("Arial", 13, QFont.Bold))
        self.next_button.setStyleSheet(
            "background-color: #1f1f1f; color: white; padding: 10px; border-radius: 10px;"
        )
        self.next_button.clicked.connect(self.go_to_next_scene)

        # Center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)
        button_layout.addStretch()
        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)

    def animate_scene(self):
        # Fade-in effect for narration
        effect = QGraphicsOpacityEffect()
        self.narration_label.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(1500)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.start() 
        self.fade_animation = animation  # Keep reference to avoid garbage collection

    def go_to_next_scene(self):
        print("Next scene triggered (hook this up later)")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    tutorial = ZKPTutorial()
    tutorial.show()
    sys.exit(app.exec_())

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton

def create_level_card(parent, title, description, button_label, unlock_condition_met, launch_function):
    card = QFrame(parent)
    card.setFrameShape(QFrame.StyledPanel)
    card.setStyleSheet("""
        QFrame {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #ccc;
        }
    """)

    layout = QVBoxLayout(card)

    title_label = QLabel(title)
    title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
    layout.addWidget(title_label)

    desc_label = QLabel(description)
    desc_label.setWordWrap(True)
    desc_label.setStyleSheet("color: #555; font-size: 13px;")
    layout.addWidget(desc_label)

    play_button = QPushButton(button_label)
    play_button.setFixedHeight(40)

    if unlock_condition_met:
        play_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        play_button.clicked.connect(launch_function)
    else:
        play_button.setEnabled(False)
        play_button.setStyleSheet("""
            QPushButton {
                background-color: #bbb;
                color: #666;
                border-radius: 8px;
            }
        """)
        play_button.setToolTip("Earn more trust points to unlock this level.")

    layout.addWidget(play_button)
    return card

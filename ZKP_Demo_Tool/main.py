import sys
from PyQt5.QtWidgets import QApplication
from level_selector import LevelSelector

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LevelSelector()
    window.show()
    sys.exit(app.exec_())
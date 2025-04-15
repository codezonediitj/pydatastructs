from PyQt5.QtCore import QPointF
from levels.base_level import BaseLevel

class Level2Ring(BaseLevel):
    def __init__(self, parent_selector, auto_mode=False, auto_rounds=5):
        super().__init__(
            "Level 2: Encrypted Fraud Network",
            parent_selector,
            auto_mode=auto_mode,
            auto_rounds=auto_rounds
        )

        # Node layout (visually inspired by screenshot)
        positions = [
            QPointF(300, 400),  # 0 - bottom center-left
            QPointF(150, 300),  # 1
            QPointF(150, 200),  # 2
            QPointF(300, 100),  # 3 - top center-left
            QPointF(450, 100),  # 4 - top center-right
            QPointF(600, 200),  # 5
            QPointF(600, 300),  # 6
            QPointF(450, 400)   # 7 - bottom center-right
        ]

        # Edge list (dense fraud ring)
        edges = [
            (0, 1), (0, 7), (1, 2), (1, 7), (2, 3),
            (3, 4), (4, 5), (5, 6), (6, 7),
            (2, 5), (1, 4), (3, 6), (0, 5), (7, 2)
        ]

        self.create_graph(positions, edges)


from PyQt5.QtCore import QPointF
from levels.base_level import BaseLevel


class Level1Triangle(BaseLevel):
    def __init__(self, parent_selector, auto_mode=False, auto_rounds=3):
        super().__init__("Level 1: Triangle", parent_selector, auto_mode=auto_mode, auto_rounds=auto_rounds)


        # Define triangle layout
        positions = [
            QPointF(300, 100),
            QPointF(500, 300),
            QPointF(100, 300)
        ]

        edges = [(0, 1), (1, 2), (2, 0)]

        self.create_graph(positions, edges)

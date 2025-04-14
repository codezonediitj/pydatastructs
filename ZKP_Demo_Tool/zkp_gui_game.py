import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout,
    QHBoxLayout, QLabel, QComboBox, QGraphicsView, QGraphicsScene, QTextEdit
)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF
class DummyGraph:
    def __init__(self):
        self.vertices = ['A', 'B', 'C', 'D']
        self.edge_weights = {('A', 'B'): 2, ('B', 'C'): 3, ('C', 'D'): 4, ('A', 'D'): 10}
graph = DummyGraph()

class GraphCanvas(QGraphicsView):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.draw_graph()

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
    def draw_graph(self):
        node_positions = {
            'A': QPointF(50, 50),
            'B': QPointF(250, 50),
            'C': QPointF(250, 200),
            'D': QPointF(50, 200)
        }
        radius = 30

        pen = QPen(Qt.black)
        brush = QBrush(QColor("skyblue"))

        self.scene.clear()

        for node, pos in node_positions.items():
            self.scene.addEllipse(pos.x(), pos.y(), radius, radius, pen, brush)
            self.scene.addText(node).setPos(pos.x()+8, pos.y()+5)

        for (src, dst), weight in self.graph.edge_weights.items():
            src_pos = node_positions[src] + QPointF(radius / 2, radius / 2)
            dst_pos = node_positions[dst] + QPointF(radius / 2, radius / 2)
            self.scene.addLine(src_pos.x(), src_pos.y(), dst_pos.x(), dst_pos.y(), QPen(Qt.darkGray))
            mid_x = (src_pos.x() + dst_pos.x()) / 2
            mid_y = (src_pos.y() + dst_pos.y()) / 2
            self.scene.addText(str(weight)).setPos(mid_x, mid_y)

class ZKPDemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zero-Knowledge Proof Demo - Graph Mode")
        self.setGeometry(200, 100, 1000, 700)
        self.canvas = GraphCanvas(graph)
        self.start_selector = QComboBox()
        self.end_selector = QComboBox()
        for v in graph.vertices:
            self.start_selector.addItem(v)
            self.end_selector.addItem(v)
        self.prove_button = QPushButton("🔒 Commit to Path")
        self.prove_button.clicked.connect(self.run_zkp_simulation)
        self.output_panel = QTextEdit()
        self.output_panel.setReadOnly(True)
        self.output_panel.setStyleSheet("background-color: #f8f8f8; padding: 8px; font-family: Courier;")
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Start Node:"))
        control_layout.addWidget(self.start_selector)
        control_layout.addWidget(QLabel("End Node:"))
        control_layout.addWidget(self.end_selector)
        control_layout.addWidget(self.prove_button)
        main_layout = QVBoxLayout()
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.canvas, stretch=3)
        main_layout.addWidget(QLabel("Walkthrough Panel:"))
        main_layout.addWidget(self.output_panel, stretch=1)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

import random
import hashlib
from PyQt5.QtCore import QPointF, QTimer
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QMessageBox
from levels.base_level import BaseLevel


class Level2BankGraph(BaseLevel):
    def __init__(self, parent_selector, auto_mode=False, auto_rounds=5):
        super().__init__("Level 2: Banking Fraud Simulation", parent_selector, auto_mode=auto_mode, auto_rounds=auto_rounds)
        self.create_fraud_graph()

    def create_fraud_graph(self):
        positions = [
            QPointF(300, 50),    # 0: Customer A
            QPointF(200, 130),   # 1: ATM 1
            QPointF(400, 130),   # 2: ATM 2 / Suspicious Customer
            QPointF(300, 210),   # 3: Bank Branch
            QPointF(200, 290),   # 4: Auditor
            QPointF(400, 290),   # 5: Merchant
        ]

        self.node_roles = {
            0: "Customer A",
            1: "ATM 1",
            2: "ATM 2 / Suspicious Customer",
            3: "Bank Branch",
            4: "Auditor",
            5: "Merchant"
        }

        edges = [
            (0, 1), (0, 2),
            (1, 3), (2, 3),
            (1, 2),
            (3, 4), (3, 5),
            (2, 5), (1, 5),
            (4, 5)
        ]

        self.create_graph(positions, edges)

    def create_graph(self, positions, edges):
        self.graph.clear()
        self.scene.clear()
        self.nodes = {}
        self.graph_nodes = {} 
        self.edges = []

        for i, pos in enumerate(positions):
            label = self.node_roles.get(i, f"Node {i}")
            self.add_node(i, pos, label=label)

        added_edges = set()
        for u, v in edges:
            if u != v and (u, v) not in added_edges and (v, u) not in added_edges:
                self.add_edge(u, v)
                added_edges.add((u, v))

    def show_education_modal(self):
        pass

    def ask_mode_selection(self):
        pass

    def auto_run_verification(self):
        def run_next():
            if self.rounds >= self.auto_total_rounds:
                self.finish_level()
                return

            self.reset_game(preserve_round=True)
            self.apply_random_permuted_coloring()
            self.commit_colors(auto_trigger=True)
            QTimer.singleShot(1000, lambda: self.challenge_edge_once(auto=True))
            self.rounds += 1
            QTimer.singleShot(2000, run_next)

        run_next()

    def prompt_next_round(self):
        self.reset_game(preserve_round=True)
        self.update_narration("Next round: recolor and commit.")

    def finish_level(self):
        self.update_narration("✅ Verification complete!")
        if self.valid_proofs + self.invalid_proofs == 0:
            return
        total = self.valid_proofs + self.invalid_proofs
        success = (self.valid_proofs / total) * 100
        self.log(f"\n🎯 Final Success Rate: {success:.2f}%")

    def update_success_chart(self):
        total_rounds = self.valid_proofs + self.invalid_proofs
        if total_rounds == 0:
            return
        success_rate = (self.valid_proofs / total_rounds) * 100
        self.success_rates.append(success_rate)
        self.round_numbers.append(total_rounds)
        self.ax.clear()
        self.ax.plot(self.round_numbers, self.success_rates, marker='o')
        self.ax.set_title("ZKP Success Rate Over Rounds")
        self.ax.set_xlabel("Rounds")
        self.ax.set_ylabel("Success %")
        self.ax.set_ylim(0, 100)
        self.canvas.draw()

    def reset_game(self, preserve_round=False):
        self.committed = False
        self.node_colors.clear()
        self.commitments.clear()
        self.nonces.clear()
        for node in self.nodes.values():
            node.unlock()
            node.hide_hash()

        if not preserve_round:
            self.rounds = 0
            self.valid_proofs = 0
            self.invalid_proofs = 0
            self.log_box.clear()
            self.update_narration("Game reset. Recolor to start.")
        else:
            self.update_narration("Recolor to begin next round.")

    def challenge_edge_once(self, auto=False):
        if not self.committed:
            if not auto:
                QMessageBox.warning(self, "Commit First", "You must commit before challenging.")
            return

        edge = random.choice(self.edges)
        node1, node2 = edge
        color1 = self.node_colors.get(node1)
        color2 = self.node_colors.get(node2)

        color1_str = color1.name() if isinstance(color1, QColor) else str(color1)
        color2_str = color2.name() if isinstance(color2, QColor) else str(color2)

        self.nodes[node1].setBrush(QBrush(QColor(color1)))
        self.nodes[node2].setBrush(QBrush(QColor(color2)))
        self.log(f"Verifier checks edge {edge}")

        recomputed1 = hashlib.sha256((color1_str + self.nonces[node1]).encode()).hexdigest()
        recomputed2 = hashlib.sha256((color2_str + self.nonces[node2]).encode()).hexdigest()
        valid1 = recomputed1 == self.commitments[node1]
        valid2 = recomputed2 == self.commitments[node2]

        if not valid1:
            self.log(f"❌ Non-repudiation failed for node {node1}")
            self.nodes[node1].pulse_red()
        if not valid2:
            self.log(f"❌ Non-repudiation failed for node {node2}")
            self.nodes[node2].pulse_red()

        if not valid1 or not valid2:
            self.update_narration("Non-repudiation breach detected. Proof invalid.")
            self.invalid_proofs += 1
        elif color1 == color2:
            self.invalid_proofs += 1
            result = f"Proof failed: same color on edge {edge}."
            self.update_narration(result)
        else:
            self.valid_proofs += 1
            result = f"Proof accepted: edge {edge} is valid."
            self.update_narration(f"{result} Round {self.rounds}/{self.auto_total_rounds}")

        self.update_success_chart()

        if not self.auto_mode:
            QTimer.singleShot(1500, self.prompt_next_round if self.rounds < self.max_rounds else self.finish_level)

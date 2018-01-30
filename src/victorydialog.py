#!/usr/bin/env python3
"""VictoryDialog UI class file"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox, QGridLayout
from PyQt5.QtCore import Qt

class VictoryDialog(QDialog):
    """Dialog that shows the final statistics after finishing a maze"""
    def __init__(self, solver, moves, time):
        super().__init__()

        self.setWindowTitle('Victory')
        main_layout = QVBoxLayout(self)

        self.victory_text = QLabel()
        self.victory_text.setAlignment(Qt.AlignCenter)
        if solver:
            self.victory_text.setText('Solver found a solution for the maze.')
        else:
            self.victory_text.setText('Congratulations! You found the exit!')

        self.stats_text = QLabel('Final statistics')
        self.stats_text.setAlignment(Qt.AlignCenter)

        stats_layout = QGridLayout()

        self.time_text = QLabel('Time:')
        self.time_value_text = QLabel('%02d:%02.d' % (int(time / 60), int(time % 60)))
        self.time_value_text.setAlignment(Qt.AlignRight)

        self.moves_text = QLabel('Moves:')
        self.moves_value_text = QLabel(str(moves))
        self.moves_value_text.setAlignment(Qt.AlignRight)

        main_layout.addWidget(self.victory_text)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.stats_text)
        main_layout.addLayout(stats_layout)
        stats_layout.addWidget(self.time_text, 0, 0, 1, 1)
        stats_layout.addWidget(self.time_value_text, 0, 1, 1, 1)
        stats_layout.addWidget(self.moves_text, 1, 0, 1, 1)
        stats_layout.addWidget(self.moves_value_text, 1, 1, 1, 1)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        main_layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)

        self.show()

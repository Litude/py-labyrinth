#!/usr/bin/env python3
"""HelpDialog UI class file"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox, QGridLayout
from PyQt5.QtCore import Qt

class HelpDialog(QDialog):
    """Dialog that explains the goal, buttons and hotkeys for the game"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Help Screen')

        self.main_layout = QVBoxLayout(self)
        self.controls_layout = QGridLayout()
        self.hotkeys_layout = QGridLayout()

        self.initailize_goal_text()
        self.initialize_controls()
        self.initialize_hotkeys()
        self.initialize_buttons()

        self.show()

    def initailize_goal_text(self):
        """Initializes the goal text and adds it to the layout"""
        goal_text = QLabel("The goal of the game is to reach the exit, which is located in the "
                           "bottom-right corner of the top floor. Moves and time are kept track "
                           "of, so try solving the maze in as short a time and with as few moves "
                           "as possible.\n"
                           "\n"
                           "If you can't find the exit, the game can also show "
                           "the path to the goal by choosing Solve from the File menu.")
        goal_text.setWordWrap(True)
        goal_text.setMaximumWidth(280)

        self.main_layout.addWidget(goal_text)
        self.main_layout.addSpacing(10)

    def initialize_controls(self):
        """Initializes the controls and adds them to the layout"""
        controls_text = QLabel('Game controls')
        controls_text.setAlignment(Qt.AlignCenter)

        move_key = QLabel('Arrow keys')
        move_text = QLabel('Move player')
        move_text.setAlignment(Qt.AlignRight)

        ladder_key = QLabel('Q/A')
        ladder_text = QLabel('Ascend/descend ladder')
        ladder_text.setAlignment(Qt.AlignRight)

        self.main_layout.addWidget(controls_text)
        self.main_layout.addLayout(self.controls_layout)
        self.controls_layout.addWidget(move_key, 0, 0, 1, 1)
        self.controls_layout.addWidget(move_text, 0, 1, 1, 1)
        self.controls_layout.addWidget(ladder_key, 1, 0, 1, 1)
        self.controls_layout.addWidget(ladder_text, 1, 1, 1, 1)
        self.main_layout.addSpacing(10)

    def initialize_hotkeys(self):
        """Initializes the hotkeys and adds them to the layout"""
        hotkeys_text = QLabel('Hotkeys')
        hotkeys_text.setAlignment(Qt.AlignCenter)

        help_key = QLabel('F1')
        help_text = QLabel('Help screen')
        help_text.setAlignment(Qt.AlignRight)

        newg_key = QLabel('F2')
        newg_text = QLabel('New game')
        newg_text.setAlignment(Qt.AlignRight)

        solve_key = QLabel('F3')
        solve_text = QLabel('Solve')
        solve_text.setAlignment(Qt.AlignRight)

        loadg_key = QLabel('F11')
        loadg_text = QLabel('Load game')
        loadg_text.setAlignment(Qt.AlignRight)

        saveg_key = QLabel('F12')
        saveg_text = QLabel('Save game')
        saveg_text.setAlignment(Qt.AlignRight)

        exit_key = QLabel('Alt+F4')
        exit_text = QLabel('Exit')
        exit_text.setAlignment(Qt.AlignRight)

        self.main_layout.addWidget(hotkeys_text)
        self.main_layout.addLayout(self.hotkeys_layout)
        self.hotkeys_layout.addWidget(help_key, 0, 0, 1, 1)
        self.hotkeys_layout.addWidget(help_text, 0, 1, 1, 1)
        self.hotkeys_layout.addWidget(newg_key, 1, 0, 1, 1)
        self.hotkeys_layout.addWidget(newg_text, 1, 1, 1, 1)
        self.hotkeys_layout.addWidget(solve_key, 2, 0, 1, 1)
        self.hotkeys_layout.addWidget(solve_text, 2, 1, 1, 1)
        self.hotkeys_layout.addWidget(loadg_key, 3, 0, 1, 1)
        self.hotkeys_layout.addWidget(loadg_text, 3, 1, 1, 1)
        self.hotkeys_layout.addWidget(saveg_key, 4, 0, 1, 1)
        self.hotkeys_layout.addWidget(saveg_text, 4, 1, 1, 1)
        self.hotkeys_layout.addWidget(exit_key, 5, 0, 1, 1)
        self.hotkeys_layout.addWidget(exit_text, 5, 1, 1, 1)

    def initialize_buttons(self):
        """Initializes the buttons and adds them to the layout"""
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok,
            Qt.Horizontal, self)
        self.main_layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)

#!/usr/bin/env python3
"""NewGameDialog UI class file"""

from PyQt5.QtWidgets import QLabel, QVBoxLayout, QDialog, QDialogButtonBox, QSpinBox
from PyQt5.QtCore import Qt
from coordinate import Coordinate

class NewGameDialog(QDialog):
    """The NewGameDialog which allows selecting dimensions of a new maze"""
    def __init__(self, old_dimensions):
        super().__init__()

        self.setWindowTitle('New Game')
        layout = QVBoxLayout(self)

        self.width_text = QLabel('Width (5-100):')
        self.width = QSpinBox()
        self.width.setRange(5, 100)
        self.width.setValue(old_dimensions.x)

        self.height_text = QLabel('Height (5-100):')
        self.height = QSpinBox()
        self.height.setRange(5, 100)
        self.height.setValue(old_dimensions.y)

        self.floors_text = QLabel('Floors (1-5):')
        self.floors = QSpinBox()
        self.floors.setRange(1, 5)
        self.floors.setValue(old_dimensions.z)

        layout.addWidget(self.width_text)
        layout.addWidget(self.width)
        layout.addWidget(self.height_text)
        layout.addWidget(self.height)
        layout.addWidget(self.floors_text)
        layout.addWidget(self.floors)

        # OK and Cancel buttons
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        self.show()

    def get_values(self):
        """Method returning the values chosen in the dialog"""
        return Coordinate(self.width.value(), self.height.value(), self.floors.value())

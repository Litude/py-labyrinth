#!/usr/bin/env python3
"""Labyrinth main file used for running the application"""

import sys
from PyQt5.QtWidgets import QApplication
from gamemainui import GameMainUI

def main():
    """Function that initializes the UI thereby starting the game"""

    app = QApplication(sys.argv)
    gui = GameMainUI()
    gui.show()
    sys.exit(app.exec_())

main()

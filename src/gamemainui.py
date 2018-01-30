#!/usr/bin/env python3
"""GameMainUI UI class file"""

from os import path, makedirs
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QMessageBox, QLabel
from PyQt5.QtCore import QTimer
from gameview import GameView
from newgamedialog import NewGameDialog
from victorydialog import VictoryDialog
from helpdialog import HelpDialog

SAVEFOLDER = '../save'

class GameMainUI(QMainWindow):
    """The main UI window class that calls all other UI classes"""

    def __init__(self):
        super().__init__()

        self.setCentralWidget(GameView())

        self.time_text = QLabel()
        self.move_text = QLabel()

        self.update_timer = QTimer()
        self.update_timer.setInterval(100)
        self.update_timer.timeout.connect(self.refresh)
        self.update_timer.start()

        self.initialize_ui()

    def initialize_ui(self):
        """Initializes the UI components of the main window"""
        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        new_game_action = QAction('New Game', self)
        new_game_action.setShortcut('F2')
        new_game_action.triggered.connect(self.menu_new_game)
        file_menu.addAction(new_game_action)

        solve_action = QAction('Solve', self)
        solve_action.setShortcut('F3')
        solve_action.triggered.connect(self.menu_solve)
        file_menu.addAction(solve_action)

        file_menu.addSeparator()

        load_game_action = QAction('Load Game', self)
        load_game_action.setShortcut('F11')
        load_game_action.triggered.connect(self.menu_load_game)
        file_menu.addAction(load_game_action)

        save_game_action = QAction('Save Game', self)
        save_game_action.setShortcut('F12')
        save_game_action.triggered.connect(self.menu_save_game)
        file_menu.addAction(save_game_action)

        file_menu.addSeparator()

        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu('Help')

        help_action = QAction('Help Screen', self)
        help_action.setShortcut('F1')
        help_action.triggered.connect(self.menu_help)
        help_menu.addAction(help_action)

        help_menu.addSeparator()

        about_action = QAction('About', self)
        about_action.triggered.connect(self.menu_about)
        help_menu.addAction(about_action)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Labyrinth')
        self.statusBar().addWidget(self.move_text)
        self.statusBar().addPermanentWidget(self.time_text)
        self.show()

    def keyPressEvent(self, event): # pylint: disable=invalid-name
        """Redefined function that gets called periodically by the base class.
        Passes key press events to the central widget."""
        self.centralWidget().keyPressEvent(event)
        self.victory_check()

    def refresh(self):
        """Periodically called according to the interval in update_timer to update UI
        information"""

        #Pass refresh to central widget
        self.centralWidget().refresh()

        #Update statusbar
        moves = self.centralWidget().get_game_instance().get_player().get_moves()
        self.move_text.setText('Moves: ' + str(moves))
        if not self.centralWidget().get_game_instance().is_won():
            minutes = int(self.centralWidget().get_time() / 1000 / 60)
            seconds = int(self.centralWidget().get_time() / 1000) % 60
            self.time_text.setText('Time: %02d:%02.d' % (minutes, seconds))

        self.update()
        self.victory_check()

    def menu_new_game(self):
        """Called when New Game is chosen from the File menu"""
        old_dimensions = self.centralWidget().get_game_instance().get_field().get_dimensions(True)
        dlg = NewGameDialog(old_dimensions)
        if dlg.exec_():
            self.centralWidget().get_game_instance().new_game(dlg.get_values())
            self.centralWidget().reset_timer()
            self.change_menu_action_states(True)

    def menu_solve(self):
        """Called when Solve is chosen from the File menu"""
        if self.centralWidget().solve_game():
            self.change_menu_action_states(False)
        else:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle('Warning')
            error_dialog.setIcon(QMessageBox.Warning)
            error_dialog.setText('Solver could not find a solution. Either the maze is missing a '
                                 'goal or it is unreachable.')
            error_dialog.exec_()

    def menu_save_game(self):
        """Called when Save Game is chosen from the File menu"""
        if not path.exists(SAVEFOLDER):
            makedirs(SAVEFOLDER)
        file_name = QFileDialog.getSaveFileName(
            self, 'Save file', SAVEFOLDER, "Saved games (*.sav)")[0]
        if file_name:
            self.centralWidget().store_time()
            self.centralWidget().get_game_instance().save_game(file_name)
            self.centralWidget().reset_timer()

    def menu_load_game(self):
        """Called when Load Game is chosen from the File menu"""
        file_name = QFileDialog.getOpenFileName(
            self, 'Open file', SAVEFOLDER, "Saved games (*.sav)")[0]
        if file_name:
            try:
                self.centralWidget().get_game_instance().load_game(file_name)
                self.centralWidget().reset_timer()
                self.change_menu_action_states(True)
                self.refresh()
            except ValueError as error:
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle('Error')
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setText(*error.args)
                error_dialog.exec_()

    @staticmethod
    def menu_help():
        """Called when Help Screen is chosen from the Help menu"""
        dlg = HelpDialog()
        dlg.exec_()

    @staticmethod
    def menu_about():
        """Called when About is chosen from the Help menu"""
        about_dialog = QMessageBox()
        about_dialog.setWindowTitle('About')
        about_dialog.setIcon(QMessageBox.Information)
        about_dialog.setText('Labyrinth v2.0\n\nCopyright 2018')
        about_dialog.exec_()

    def victory_check(self):
        """Calls periodically by the refresh function to check if the goal has been reached.
        If the goal has been reached, the victory dialog is shown and the game is finished."""
        if self.centralWidget().get_game_instance().check_victory():
            self.centralWidget().store_time()
            self.change_menu_action_states(False)
            dlg = VictoryDialog(self.centralWidget().get_game_instance().get_field().is_solved(),
                                self.centralWidget().get_game_instance().get_player().get_moves(),
                                self.centralWidget().get_game_instance().get_elapsed_time())
            dlg.exec_()
            self.statusBar().showMessage('Game over. Start or load a new game from the File menu.')

    def change_menu_action_states(self, state):
        """Used to enable or disable menu items."""
        for menu_action in self.menuBar().actions()[0].menu().actions():
            if menu_action.text() == 'Solve' or menu_action.text() == 'Save Game':
                menu_action.setEnabled(state)

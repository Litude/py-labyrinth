#!/usr/bin/env python3
"""GameView UI class file"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QElapsedTimer
from game import Game
from cell import Cell
from coordinate import Coordinate

TILESIZE = 20

class GameView(QWidget):
    """GameView UI class handles drawing the game and also keeps the Game instance"""
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game.new_game(Coordinate(20, 20, 2))
        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.start()

    def keyPressEvent(self, event): # pylint: disable=invalid-name
        """Redefined function that gets called periodically by the base class.
        Disable movement when maze is solved or game is won."""
        if not self.game.get_field().is_solved() and not self.game.is_won():
            if event.key() == Qt.Key_Right:
                self.game.get_player().move_player(self.game.get_field(), Cell.RIGHT)
            if event.key() == Qt.Key_Left:
                self.game.get_player().move_player(self.game.get_field(), Cell.LEFT)
            if event.key() == Qt.Key_Up:
                self.game.get_player().move_player(self.game.get_field(), Cell.BACK)
            if event.key() == Qt.Key_Down:
                self.game.get_player().move_player(self.game.get_field(), Cell.FRONT)
            if event.key() == Qt.Key_Q:
                self.game.get_player().move_player(self.game.get_field(), Cell.TOP)
            if event.key() == Qt.Key_A:
                self.game.get_player().move_player(self.game.get_field(), Cell.BOTTOM)
        self.update()

    def paintEvent(self, event): # pylint: disable=invalid-name,unused-argument
        """Redefined function that gets called periodically by the base class.
        Used to call drawing functions."""
        painter = QPainter()
        painter.begin(self)
        self.draw_game(painter)
        painter.end()

    def refresh(self):
        """Periodically called from GameMainUI and used to update player position if the
        auto-solve option has been enabled"""
        if self.game.get_field().is_solved() and not self.game.is_won():
            player_position = self.game.get_player().get_position()
            solution_direction = self.game.get_field().get_cell(player_position).get_solution()
            self.game.get_player().move_player(self.game.get_field(), solution_direction)

    def solve_game(self):
        """Called by GameMainUI to solve the maze"""
        goal_position = self.game.get_field().get_goal()
        player_position = self.game.get_player().get_position()
        return self.game.get_field().solve_maze(player_position, goal_position)

    def draw_game(self, painter):
        """Called by paintEvent to initialize the actual drawing of the game"""
        line_pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(line_pen)

        #Calculate offsets to move view acc. to position or center the maze if whole maze fits
        if self.width() < self.game.get_field().get_width() * TILESIZE:
            x_offset = self.width()/2 - self.game.get_player().get_position().x * TILESIZE
        else:
            x_offset = (self.width() - self.game.get_field().get_width() * TILESIZE) / 2

        if self.height() < self.game.get_field().get_width() * TILESIZE:
            y_offset = self.height()/2 - self.game.get_player().get_position().y * TILESIZE
        else:
            y_offset = (self.height() - self.game.get_field().get_height() * TILESIZE) / 2

        #Draw the current floor and solution if the maze is solved
        z = self.game.get_player().get_floor()
        for y in range(self.game.get_field().get_height()):
            for x in range(self.game.get_field().get_width()):
                coordinates = Coordinate(x, y, z)
                self.draw_maze(painter, x_offset, y_offset, coordinates)
                if self.game.get_field().get_cell(coordinates).get_solution():
                    self.draw_solution(painter, x_offset, y_offset, coordinates)

        #Draw the player
        self.draw_player(painter, x_offset, y_offset)

    def draw_maze(self, painter, x_offset, y_offset, coordinates):
        """Draws the maze"""
        maze_pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(maze_pen)
        cell = self.game.get_field().get_cell(coordinates)
        x = coordinates.x
        y = coordinates.y

        if cell.is_wall(Cell.BACK) and not cell.is_entrance():
            painter.drawLine(x*TILESIZE+x_offset, y*TILESIZE+y_offset,
                             (x+1)*TILESIZE+x_offset, y*TILESIZE+y_offset)
        if cell.is_wall(Cell.FRONT) and not cell.is_goal():
            painter.drawLine(x*TILESIZE+x_offset, (y+1)*TILESIZE+y_offset,
                             (x+1)*TILESIZE+x_offset, (y+1)*TILESIZE+y_offset)
        if cell.is_wall(Cell.LEFT):
            painter.drawLine(x*TILESIZE+x_offset, y*TILESIZE+y_offset,
                             x*TILESIZE+x_offset, (y+1)*TILESIZE+y_offset)
        if cell.is_wall(Cell.RIGHT):
            painter.drawLine((x+1)*TILESIZE+x_offset, y*TILESIZE+y_offset,
                             (x+1)*TILESIZE+x_offset, (y+1)*TILESIZE+y_offset)

        if not cell.is_wall(Cell.TOP):
            #Draw ladders
            painter.drawLine(x*TILESIZE+6+x_offset, y*TILESIZE+2+y_offset,
                             x*TILESIZE+6+x_offset, (y+1)*TILESIZE-6+y_offset)
            painter.drawLine((x+1)*TILESIZE-6+x_offset, y*TILESIZE+2+y_offset,
                             (x+1)*TILESIZE-6+x_offset, (y+1)*TILESIZE-6+y_offset)
            painter.drawLine(x*TILESIZE+6+x_offset, y*TILESIZE+4+y_offset,
                             (x+1)*TILESIZE-6+x_offset, y*TILESIZE+4+y_offset)
            painter.drawLine(x*TILESIZE+6+x_offset, y*TILESIZE+8+y_offset,
                             (x+1)*TILESIZE-6+x_offset, y*TILESIZE+8+y_offset)
            painter.drawLine(x*TILESIZE+6+x_offset, y*TILESIZE+12+y_offset,
                             (x+1)*TILESIZE-6+x_offset, y*TILESIZE+12+y_offset)

        if not cell.is_wall(Cell.BOTTOM):
            painter.drawEllipse(x*TILESIZE+2+x_offset, y*TILESIZE+TILESIZE/2+y_offset,
                                TILESIZE-4, TILESIZE/2-4)

    def draw_solution(self, painter, x_offset, y_offset, coordinates):
        """Draws the solution"""
        solution_pen = QPen(Qt.green, 1, Qt.SolidLine)
        painter.setPen(solution_pen)
        cell = self.game.get_field().get_cell(coordinates)
        x = coordinates.x
        y = coordinates.y

        if cell.get_solution() == Cell.RIGHT:
            painter.drawLine(x*TILESIZE+x_offset+TILESIZE/2, y*TILESIZE+y_offset+TILESIZE/2,
                             (x+1)*TILESIZE+x_offset+TILESIZE/2, y*TILESIZE+y_offset+TILESIZE/2)
        if cell.get_solution() == Cell.LEFT:
            painter.drawLine((x-1)*TILESIZE+x_offset+TILESIZE/2, y*TILESIZE+y_offset+TILESIZE/2,
                             x*TILESIZE+x_offset+TILESIZE/2, y*TILESIZE+y_offset+TILESIZE/2)
        if cell.get_solution() == Cell.BACK:
            painter.drawLine(x*TILESIZE+x_offset+TILESIZE/2, y*TILESIZE+y_offset+TILESIZE/2,
                             x*TILESIZE+x_offset+TILESIZE/2, (y-1)*TILESIZE+y_offset+TILESIZE/2)
        if cell.get_solution() == Cell.FRONT:
            painter.drawLine(x*TILESIZE+x_offset+TILESIZE/2, (y+1)*TILESIZE+y_offset+TILESIZE/2,
                             x*TILESIZE+x_offset+TILESIZE/2, y*TILESIZE+y_offset+TILESIZE/2)

    def draw_player(self, painter, x_offset, y_offset):
        """Draws the player"""
        player_pen = QPen(Qt.red, 1, Qt.SolidLine)
        painter.setPen(player_pen)
        player_position = self.game.get_player().get_position()
        painter.drawEllipse(player_position.x*TILESIZE+2+x_offset,
                            player_position.y*TILESIZE+2+y_offset,
                            TILESIZE-4,
                            TILESIZE-4)

    def reset_timer(self):
        """Resets the internal timer, should be called always when the current time is updated
        to the game instance. This means when saving or loading games."""
        self.elapsed_timer.restart()

    def get_game_instance(self):
        """Returns the game instance"""
        return self.game

    def store_time(self):
        """Stores the current time in the Game instance"""
        self.game.set_elapsed_time(self.get_time() / 1000)

    def get_time(self):
        """Need to add time stored in the game instance to properly restore time from saved games"""
        return self.elapsed_timer.elapsed() + self.game.get_elapsed_time() * 1000

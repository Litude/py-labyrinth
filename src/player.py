#!/usr/bin/env python3
"""The Player class and associated functions"""

from cell import Cell
from coordinate import Coordinate

class Player:
    """Player class which keeps track of moves and its current position. Starting position and
    number of moves can be specified; both default to 0"""

    def __init__(self, position=Coordinate(0, 0, 0), moves=0):
        self.__position = position
        self.__moves = moves

    def get_position(self):
        """Returns the player position as a coordinate"""
        return self.__position

    def get_floor(self):
        """Returns the current player floor"""
        return self.__position.z

    def get_moves(self):
        """Returns the number of moves"""
        return self.__moves

    def is_player(self, position):
        """Returns a boolean whether the player is at position"""
        if self.__position == position:
            return True
        return False

    def move_player(self, maze, direction):
        """Assumes all maze edges have walls, doesn't check if trying to go out of the maze
        boundaries. Returns True if moving succeeded, False otherwise"""
        if not maze.get_cell(self.__position).is_wall(direction):
            if direction == Cell.TOP:
                self.__position.z += 1
            elif direction == Cell.BOTTOM:
                self.__position.z -= 1
            elif direction == Cell.LEFT:
                self.__position.x -= 1
            elif direction == Cell.RIGHT:
                self.__position.x += 1
            elif direction == Cell.BACK:
                self.__position.y -= 1
            elif direction == Cell.FRONT:
                self.__position.y += 1

            self.__moves += 1
            return True

        return False

#!/usr/bin/env python3
"""The main Game class acting as kind of a container for a Player and the Maze"""

from struct import pack, unpack
from os import path
from cell import Cell
from maze import Maze
from player import Player
from coordinate import Coordinate

#Saved file constants
HEADER_SIZE = 18
HEADER_SIGNATURE = b'LABv20'

class Game:
    """The Game class contains a Maze and a Player and also keeps track of time"""

    def __init__(self):

        self.__field = None
        self.__player = None
        self.__time = 0
        self.__won = False

    def new_game(self, mazesize):
        """New game, takes maze dimensions as input"""
        self.__field = Maze(mazesize)
        self.__field.carve_maze(Coordinate(0, 0, 0))
        self.__player = Player(Coordinate(0, 0, 0))
        self.__won = False
        self.__time = 0

    def set_elapsed_time(self, time):
        """Called by the GUI before saving to update the time, time should be in seconds"""
        self.__time = int(time)

    def get_elapsed_time(self):
        """Returns elapsed time in seconds"""
        return self.__time

    def get_field(self):
        """Returns the Maze object of Game"""
        return self.__field

    def set_player(self, player):
        """Used to set or replace the current Player instance"""
        self.__player = player

    def get_player(self):
        """Returns the Player instance"""
        return self.__player

    def check_victory(self):
        """This is called to change the state of the game into a won game if conditions are met.
        Returns True if the state is changed, false otherwise."""
        if self.__field.get_goal() == self.__player.get_position() and not self.__won:
            self.__won = True
            return True
        return False

    def is_won(self):
        """Returns whether the game is over but doesn't check if victory requirements are met.
        For checking requirements, check_victory should be used to actually update the state"""
        return self.__won

    def save_game(self, filename):
        """Saves the current Game instance as filename"""
        with open(filename, 'wb') as save_file:
            save_file.write(HEADER_SIGNATURE)
            save_file.write(pack('BBB', *self.__field.get_dimensions(True)))
            save_file.write(pack('BBB', *self.__player.get_position()))
            save_file.write(pack('H', self.__player.get_moves()))
            save_file.write(pack('I', self.get_elapsed_time()))

            for z in range(self.__field.get_floors()):
                for y in range(self.__field.get_height()):
                    for x in range(self.__field.get_width()):
                        cell_value = self.encode_cell(self.__field, Coordinate(x, y, z))
                        save_file.write(pack('B', cell_value))

    @staticmethod
    def encode_cell(field, coordinate):
        """Returns the binary value of the cell at coordinate in field"""
        cell_value = 0
        cell = field.get_cell(coordinate)

        if cell.is_wall(Cell.TOP):
            cell_value |= 1 << Cell.TOP
        if cell.is_wall(Cell.BOTTOM):
            cell_value |= 1 << Cell.BOTTOM
        if cell.is_wall(Cell.LEFT):
            cell_value |= 1 << Cell.LEFT
        if cell.is_wall(Cell.RIGHT):
            cell_value |= 1 << Cell.RIGHT
        if cell.is_wall(Cell.BACK):
            cell_value |= 1 << Cell.BACK
        if cell.is_wall(Cell.FRONT):
            cell_value |= 1 << Cell.FRONT

        if cell.is_entrance():
            cell_value |= 1 << Cell.ENTRANCE
        if cell.is_goal():
            cell_value |= 1 << Cell.GOAL

        return cell_value

    def load_game(self, filename):
        """Replaces the current Game instance with that in filename"""
        with open(filename, 'rb') as load_file:
            filesize = path.getsize(filename)

            if filesize < HEADER_SIZE:
                raise ValueError('File is not a valid save file!')

            #Check that the header signature matches
            if not load_file.read(6) == HEADER_SIGNATURE:
                raise ValueError('File is not a valid save file!')

            maze_dimensions = Coordinate(*unpack('BBB', load_file.read(3)))

            #Check that the file size matches with what it should be according to the header
            if filesize != HEADER_SIZE + maze_dimensions.x * maze_dimensions.y * maze_dimensions.z:
                raise ValueError('File is not a valid save file!')

            loaded_field = Maze(maze_dimensions)

            player_coord = Coordinate(*unpack('BBB', load_file.read(3)))
            player_moves = unpack('H', load_file.read(2))[0]

            #Check that the player is inside the maze
            if (player_coord.x >= maze_dimensions.x or
                    player_coord.y >= maze_dimensions.y or
                    player_coord.z >= maze_dimensions.z):
                raise ValueError('File is not a valid save file!')

            loaded_player = Player(player_coord, player_moves)

            loaded_time = unpack('I', load_file.read(4))[0]

            for z in range(loaded_field.get_floors()):
                for y in range(loaded_field.get_height()):
                    for x in range(loaded_field.get_width()):
                        cell_value = unpack('B', load_file.read(1))[0]
                        self.decode_cell(loaded_field, Coordinate(x, y, z), cell_value)

            loaded_field.set_carved()
            self.__field = loaded_field
            self.__player = loaded_player
            self.__time = loaded_time
            self.__won = False

    @staticmethod
    def decode_cell(field, coordinate, cell_value):
        """Updates the cell at coordinate in field according to cell_value"""
        if not cell_value & (1 << Cell.TOP):
            field.get_cell(coordinate).remove_wall(Cell.TOP)
        if not cell_value & (1 << Cell.BOTTOM):
            field.get_cell(coordinate).remove_wall(Cell.BOTTOM)
        if not cell_value & (1 << Cell.LEFT):
            field.get_cell(coordinate).remove_wall(Cell.LEFT)
        if not cell_value & (1 << Cell.RIGHT):
            field.get_cell(coordinate).remove_wall(Cell.RIGHT)
        if not cell_value & (1 << Cell.BACK):
            field.get_cell(coordinate).remove_wall(Cell.BACK)
        if not cell_value & (1 << Cell.FRONT):
            field.get_cell(coordinate).remove_wall(Cell.FRONT)

        if cell_value & (1 << Cell.ENTRANCE):
            field.get_cell(coordinate).set_as_entrance()
        if cell_value & (1 << Cell.GOAL):
            field.get_cell(coordinate).set_as_goal()

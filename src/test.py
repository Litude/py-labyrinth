#!/usr/bin/env python3
"""Labyrinth unit tests for testing non-UI related classes and functions"""

import unittest
from maze import Maze
from cell import Cell
from player import Player
from coordinate import Coordinate

class Test(unittest.TestCase):
    """Unit testing class used for testing the non-UI related classes and functions"""

    def test_unvisited_neighbours(self):
        """Tests that the unvisited neighbors function returns the correct neighbors for edges and
        the middle of an uncarved maze"""

        field = Maze(Coordinate(5, 5, 5))

        #Test lower-left corner case
        self.assertEqual(Maze.carver_unvisited_neighbors(field, Coordinate(0, 0, 0), bias=1),
                         [Cell.RIGHT, Cell.FRONT, Cell.TOP])

        #Test middle case
        self.assertEqual(Maze.carver_unvisited_neighbors(field, Coordinate(2, 2, 2), bias=1),
                         [Cell.LEFT, Cell.RIGHT, Cell.BACK, Cell.FRONT, Cell.TOP, Cell.BOTTOM])

        #Test upper-right corner case
        self.assertEqual(Maze.carver_unvisited_neighbors(field, Coordinate(4, 4, 4), bias=1),
                         [Cell.LEFT, Cell.BACK, Cell.BOTTOM])

    def test_unvisited_flag(self):
        """Tests that the unvisited flag is properly reset after carving a maze"""

        field = Maze(Coordinate(5, 5, 5))

        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(1, 1, 1)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(2, 2, 2)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(3, 3, 3)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(4, 4, 4)).is_visited(), False)

        field.carve_maze()

        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(1, 1, 1)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(2, 2, 2)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(3, 3, 3)).is_visited(), False)
        self.assertEqual(field.get_cell(Coordinate(4, 4, 4)).is_visited(), False)

    def test_walls(self):
        """Tests that walls are equal on both sides and that the map matches the one generated by
        seed 900"""

        field = Maze(Coordinate(5, 5, 5), seed=900)
        field.carve_maze()

        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_wall(Cell.RIGHT), False)
        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_wall(Cell.RIGHT),
                         field.get_cell(Coordinate(1, 0, 0)).is_wall(Cell.LEFT))

        self.assertEqual(field.get_cell(Coordinate(2, 0, 0)).is_wall(Cell.RIGHT), True)
        self.assertEqual(field.get_cell(Coordinate(2, 0, 0)).is_wall(Cell.RIGHT),
                         field.get_cell(Coordinate(3, 0, 0)).is_wall(Cell.LEFT))

        self.assertEqual(field.get_cell(Coordinate(0, 1, 0)).is_wall(Cell.FRONT), False)
        self.assertEqual(field.get_cell(Coordinate(0, 1, 0)).is_wall(Cell.FRONT),
                         field.get_cell(Coordinate(0, 2, 0)).is_wall(Cell.BACK))

        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_wall(Cell.FRONT), True)
        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_wall(Cell.FRONT),
                         field.get_cell(Coordinate(0, 1, 0)).is_wall(Cell.BACK))

        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_wall(Cell.TOP), True)
        self.assertEqual(field.get_cell(Coordinate(0, 0, 0)).is_wall(Cell.TOP),
                         field.get_cell(Coordinate(0, 0, 1)).is_wall(Cell.BOTTOM))

        self.assertEqual(field.get_cell(Coordinate(2, 0, 0)).is_wall(Cell.TOP), False)
        self.assertEqual(field.get_cell(Coordinate(2, 0, 0)).is_wall(Cell.TOP),
                         field.get_cell(Coordinate(2, 0, 1)).is_wall(Cell.BOTTOM))

    def test_solver(self):
        """Tests that the solver can find the goal in a maze"""

        field = Maze(Coordinate(5, 5, 5), seed=900)
        field.carve_maze()
        self.assertEqual(field.solve_maze(Coordinate(0, 0, 0), field.get_goal()), True)

    def test_player_movement(self):
        """Tests that the player can't move through walls but can move normally"""

        field = Maze(Coordinate(5, 5, 5), seed=900)
        field.carve_maze()
        player = Player()

        self.assertEqual(player.move_player(field, Cell.FRONT), False)
        self.assertEqual(player.move_player(field, Cell.RIGHT), True)

if __name__ == '__main__':
    unittest.main()

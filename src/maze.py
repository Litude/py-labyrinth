#!/usr/bin/env python3
"""The Maze class which is basically a container for Cells"""

import random
from copy import copy
from coordinate import Coordinate
from cell import Cell

BIAS = 5

class Maze:
    """The Maze class which is a container class for Cells"""

    def __init__(self, size, seed=None):
        """
        Initialize maze with cells that have walls on all sides
        Seed can be passed for unit testing
        """

        self.__maze = [None] * size.z
        self.__size = size
        self.__carved = False
        self.__solved = False

        for i in range(size.z):
            self.__maze[i] = [None] * size.y
            for j in range(size.y):
                self.__maze[i][j] = [None] * size.x
                for k in range(size.x):
                    self.__maze[i][j][k] = Cell()

        random.seed(seed)

    def __str__(self):
        """
        Draws the complete maze
        """

        row1 = ""
        row2 = ""
        result = ""

        for z in range(self.__size.z):
            result += "Floor " + str(z + 1) + '\n'
            for y in range(self.__size.y):
                for x in range(self.__size.x):
                    if self.get_cell(Coordinate(x, y, z)).is_wall(Cell.BACK):
                        row1 += "##"
                    else:
                        row1 += "# "
                    if self.get_cell(Coordinate(x, y, z)).is_wall(Cell.LEFT):
                        row2 += "#"
                    else:
                        row2 += " "
                    if (not self.get_cell(Coordinate(x, y, z)).is_wall(Cell.TOP) and not
                            self.get_cell(Coordinate(x, y, z)).is_wall(Cell.BOTTOM)):
                        row2 += "X"
                    elif not self.get_cell(Coordinate(x, y, z)).is_wall(Cell.TOP):
                        row2 += "/"
                    elif not self.get_cell(Coordinate(x, y, z)).is_wall(Cell.BOTTOM):
                        row2 += "\\"
                    else:
                        row2 += " "

                row1 += "#\n"
                row2 += "#\n"

                result = result + row1 + row2

                row1 = ""
                row2 = ""

            result += "##" * self.__size.x + "#\n"

        return result

    def get_cell(self, point):
        """Returns the cell at the given coordinates"""
        return self.__maze[point.z][point.y][point.x]

    def get_goal(self):
        """Returns the coordiantes for the goal in the maze. Always checks the 'last' cell first
        since except for hacked saves it is always the goal"""
        if self.get_cell(self.__size - 1).is_goal():
            return self.__size - 1
        else:
            for z in range(self.__size.z):
                for y in range(self.__size.y):
                    for x in range(self.__size.x):
                        if self.get_cell(Coordinate(x, y, z)).is_goal():
                            return Coordinate(x, y, z)
        return None

    def get_width(self):
        """Returns the width (x-dimension) of the maze"""
        return self.__size.x

    def get_height(self):
        """Returns the height (y-dimension) of the maze"""
        return self.__size.y

    def get_floors(self):
        """Returns the number of floors (z-dimension) of the maze"""
        return self.__size.z

    def get_dimensions(self, full_dimensions=False):
        """Returns a tuple of the maze dimensions"""
        if not full_dimensions:
            return self.__size - 1
        return self.__size

    def set_carved(self):
        """Sets the maze as carved. Carving sets this flag automatically, should only be used when
        loading a saved game"""
        self.__carved = True

    def is_carved(self):
        """Returns whether the maze is carved"""
        return self.__carved

    def is_solved(self):
        """Returns whether the maze is solved"""
        return self.__solved

    def carve_maze(self, start=Coordinate(0, 0, 0)):
        """Recursive carver implemented in an iterative manner. Takes coordinates for carving
        start or defaults to x=0, y=0 and z=0."""

        stack = [copy(start)]

        #Carver start is set as entrance, goal is always the 'max' coordinates of the maze
        self.get_cell(start).set_as_entrance()
        self.get_cell(self.__size - 1).set_as_goal()

        while stack:

            #Pop cell from stack when no neighbors found
            cell = stack.pop()

            neighbors = self.carver_unvisited_neighbors(cell)
            self.get_cell(cell).set_visited(True)

            while neighbors:
                #Found neighbors, choose one at random and add old cell to stack
                stack.append(copy(cell))
                direction = random.randrange(0, len(neighbors))

                if neighbors[direction] == Cell.TOP:
                    self.get_cell(cell).remove_wall(Cell.TOP)
                    self.get_cell(Coordinate(cell.x, cell.y, cell.z+1)).remove_wall(Cell.BOTTOM)
                    cell.z += 1

                elif neighbors[direction] == Cell.BOTTOM:
                    self.get_cell(cell).remove_wall(Cell.BOTTOM)
                    self.get_cell(Coordinate(cell.x, cell.y, cell.z-1)).remove_wall(Cell.TOP)
                    cell.z -= 1

                elif neighbors[direction] == Cell.LEFT:
                    self.get_cell(cell).remove_wall(Cell.LEFT)
                    self.get_cell(Coordinate(cell.x-1, cell.y, cell.z)).remove_wall(Cell.RIGHT)
                    cell.x -= 1

                elif neighbors[direction] == Cell.RIGHT:
                    self.get_cell(cell).remove_wall(Cell.RIGHT)
                    self.get_cell(Coordinate(cell.x+1, cell.y, cell.z)).remove_wall(Cell.LEFT)
                    cell.x += 1

                elif neighbors[direction] == Cell.BACK:
                    self.get_cell(cell).remove_wall(Cell.BACK)
                    self.get_cell(Coordinate(cell.x, cell.y-1, cell.z)).remove_wall(Cell.FRONT)
                    cell.y -= 1

                elif neighbors[direction] == Cell.FRONT:
                    self.get_cell(cell).remove_wall(Cell.FRONT)
                    self.get_cell(Coordinate(cell.x, cell.y+1, cell.z)).remove_wall(Cell.BACK)
                    cell.y += 1

                neighbors = self.carver_unvisited_neighbors(cell)
                self.get_cell(cell).set_visited(True)

        #When the stack is empty, carving is finished
        #Make all cells unvisited for future use

        self.make_cells_unvisited()
        self.__carved = True

    def solve_maze(self, start, goal):
        """Recursive solver implemented in an iterative manner, needs coordinates for solving
        start."""
        stack = [copy(start)]

        while stack:

            #Pop cell from stack when no neighbors found
            cell = stack.pop()

            neighbors = self.solver_unvisited_neighbors(cell)
            self.get_cell(cell).set_visited(True)

            while neighbors:
                #Found neighbors, choose one at random and add old cell to stack
                stack.append(copy(cell))
                direction = random.randrange(0, len(neighbors))

                self.get_cell(cell).set_solution(neighbors[direction])

                if neighbors[direction] == Cell.TOP:
                    cell.z += 1

                elif neighbors[direction] == Cell.BOTTOM:
                    cell.z -= 1

                elif neighbors[direction] == Cell.LEFT:
                    cell.x -= 1

                elif neighbors[direction] == Cell.RIGHT:
                    cell.x += 1

                elif neighbors[direction] == Cell.BACK:
                    cell.y -= 1

                elif neighbors[direction] == Cell.FRONT:
                    cell.y += 1

                neighbors = self.solver_unvisited_neighbors(cell)
                self.get_cell(cell).set_visited(True)

                #Only need to check for goal after moving since stack cells are already visited and
                #start != goal

                if cell == goal:
                    self.make_cells_unvisited()
                    self.__solved = True
                    return True

            self.get_cell(cell).set_solution(None)

        #Solver could not find a goal, reset visited flag for stability
        self.make_cells_unvisited()
        return False

    def make_cells_unvisited(self):
        """Makes all cells unvisited, used after carving and solving to reset flags"""

        for z in range(self.__size.z):
            for y in range(self.__size.y):
                for x in range(self.__size.x):
                    self.get_cell(Coordinate(x, y, z)).set_visited(False)

    def carver_unvisited_neighbors(self, cell, bias=BIAS):
        """Used by the carver to find unvisited neighbors, disregards walls. Bias determines how
        many more times likely the maze carver is going to stay on the current floor vs. going up
        or down a floor"""

        unvisited = []

        if (cell.x > 0 and not
                self.get_cell(Coordinate(cell.x-1, cell.y, cell.z)).is_visited()):
            unvisited.append(Cell.LEFT)
        if (cell.x < self.__size.x - 1 and not
                self.get_cell(Coordinate(cell.x+1, cell.y, cell.z)).is_visited()):
            unvisited.append(Cell.RIGHT)
        if (cell.y > 0 and not
                self.get_cell(Coordinate(cell.x, cell.y-1, cell.z)).is_visited()):
            unvisited.append(Cell.BACK)
        if (cell.y < self.__size.y - 1 and not
                self.get_cell(Coordinate(cell.x, cell.y+1, cell.z)).is_visited()):
            unvisited.append(Cell.FRONT)
        #Only add TOP and BOTTOM directions if no other neighbors have been found or acc. to bias
        if not unvisited or random.randrange(0, bias) == 0:
            if (cell.z < self.__size.z - 1 and not
                    self.get_cell(Coordinate(cell.x, cell.y, cell.z+1)).is_visited()):
                unvisited.append(Cell.TOP)
            if (cell.z > 0 and not
                    self.get_cell(Coordinate(cell.x, cell.y, cell.z-1)).is_visited()):
                unvisited.append(Cell.BOTTOM)

        if unvisited:
            return unvisited
        return None

    def solver_unvisited_neighbors(self, cell):
        """Used by the solver to list unvisited neighbors, checks both walls and visited flags"""

        unvisited = []

        if (cell.z < self.__size.z - 1 and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z)).is_wall(Cell.TOP) and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z+1)).is_visited()):
            unvisited.append(Cell.TOP)
        if (cell.z > 0 and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z)).is_wall(Cell.BOTTOM) and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z-1)).is_visited()):
            unvisited.append(Cell.BOTTOM)
        if (cell.x > 0 and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z)).is_wall(Cell.LEFT) and not
                self.get_cell(Coordinate(cell.x-1, cell.y, cell.z)).is_visited()):
            unvisited.append(Cell.LEFT)
        if (cell.x < self.__size.x - 1 and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z)).is_wall(Cell.RIGHT) and not
                self.get_cell(Coordinate(cell.x+1, cell.y, cell.z)).is_visited()):
            unvisited.append(Cell.RIGHT)
        if (cell.y > 0 and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z)).is_wall(Cell.BACK) and not
                self.get_cell(Coordinate(cell.x, cell.y-1, cell.z)).is_visited()):
            unvisited.append(Cell.BACK)
        if (cell.y < self.__size.y - 1 and not
                self.get_cell(Coordinate(cell.x, cell.y, cell.z)).is_wall(Cell.FRONT) and not
                self.get_cell(Coordinate(cell.x, cell.y+1, cell.z)).is_visited()):
            unvisited.append(Cell.FRONT)

        if unvisited:
            return unvisited
        return None

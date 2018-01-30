#!/usr/bin/env python3
"""Includes the Cell class which mazes consist of."""

class Cell:
    """The Cell class which mazes consist of."""

    TOP = 0         #Increases z
    BOTTOM = 1      #Decreases z
    LEFT = 2        #Decreases x
    RIGHT = 3       #Increases x
    BACK = 4        #Decreases y
    FRONT = 5       #Increases y
    ENTRANCE = 6    #Used in maze saving/loading only
    GOAL = 7        #Used in maze saving/loading only

    """
        _______________
       /|    0        /|    As viewed side-on, numbers in
      / |            / |    parentheses are on the back plane
     /  |   (4)     /  |
    /______________/   |
    |   |          |   |
    |(2)|    5     | 3 |
    |   |----------|---|
    |  /           |  /
    | /     (1)    | /
    |/_____________|/

    """

    def __init__(self):
        self.__top_wall = True
        self.__bottom_wall = True
        self.__left_wall = True
        self.__right_wall = True
        self.__back_wall = True
        self.__front_wall = True
        self.__entrance = False
        self.__goal = False

        self.__visited = False
        self.__solution_direction = None

    def set_as_entrance(self):
        """Sets the current cell as the maze entrance"""
        self.__entrance = True

    def set_as_goal(self):
        """Sets the current cell as the maze goal"""
        self.__goal = True

    def is_entrance(self):
        """Returns whether the current cell is the entrance"""
        return self.__entrance

    def is_goal(self):
        """Returns whether the current cell is the goal"""
        return self.__goal

    def set_visited(self, flag):
        """Allows changing of the current cells visited flag"""
        self.__visited = flag

    def is_visited(self):
        """Returns whether the current cell has the visited flag checked"""
        return self.__visited

    def is_wall(self, wall):
        """Returns whether the current cell has a wall in the specified direction"""
        if wall == Cell.TOP:
            return self.__top_wall
        elif wall == Cell.BOTTOM:
            return self.__bottom_wall
        elif wall == Cell.LEFT:
            return self.__left_wall
        elif wall == Cell.RIGHT:
            return self.__right_wall
        elif wall == Cell.BACK:
            return self.__back_wall
        elif wall == Cell.FRONT:
            return self.__front_wall
        return None

    def remove_wall(self, wall):
        """Removes wall from the specified direction"""
        if wall == Cell.TOP:
            self.__top_wall = False
        elif wall == Cell.BOTTOM:
            self.__bottom_wall = False
        elif wall == Cell.LEFT:
            self.__left_wall = False
        elif wall == Cell.RIGHT:
            self.__right_wall = False
        elif wall == Cell.BACK:
            self.__back_wall = False
        elif wall == Cell.FRONT:
            self.__front_wall = False

    def set_solution(self, direction):
        """Used for storing the direction to the goal"""
        self.__solution_direction = direction

    def get_solution(self):
        """Retrieve the direction to the goal"""
        return self.__solution_direction

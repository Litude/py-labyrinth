#!/usr/bin/env python3
"""Coordinate class, more like a struct, which groups x, y and z"""

#This should have been a namedtuple but since they are immutable, a class
#was required...

class Coordinate:
    """A coordinate container with x, y and z values. Direct access to fields is allowed and
    preferred"""

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.n = 0 #Used for iterator access

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)
        return Coordinate(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)
        return Coordinate(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return Coordinate(self.x * other.x, self.y * other.y, self.z * other.z)
        return Coordinate(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return Coordinate(self.x / other.x, self.y / other.y, self.z / other.z)
        return Coordinate(self.x / other, self.y / other, self.z / other)

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        raise IndexError("Coordinate index out of range")

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n == 0:
            result = self.x
        elif self.n == 1:
            result = self.y
        elif self.n == 2:
            result = self.z
        else:
            raise StopIteration

        self.n += 1
        return result

    def __str__(self):
        return "Coordinate: x=%d, y=%d, z=%d" % (self.x, self.y, self.z)

    def get_x(self):
        """Returns the x coordinate"""
        return self.x

    def get_y(self):
        """Returns the y coordinate"""
        return self.y

    def get_z(self):
        """Returns the z coordinate"""
        return self.z

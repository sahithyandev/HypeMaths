import typing as t
from math import sqrt


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    # TODO find the correct term
    @property
    def value(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2)

    def rotate(self, angle: float):
        """TODO Rotate an angle to a specific radians"""

    def scale(self, scaler: float) -> "Vector":
        return Vector(self.x * scaler, self.y * scaler)

    def add(self, v: "Vector") -> "Vector":
        return Vector(self.x + v.x, self.y + v.y)

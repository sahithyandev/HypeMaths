import typing as t

import hypemaths as hm
from hypemaths.exceptions import MatrixDimensionError


class Vector:
    def __init__(self, *points) -> None:
        self.points = self._cleaned_vector(points)

    @staticmethod
    def _cleaned_vector(points: tuple) -> list:
        def value_check(vector_points: list) -> bool:
            for index, point in enumerate(vector_points):
                if not isinstance(point, (int, float)):
                    raise TypeError(f"All points must be integers or floats, but point[{index}] is {type(point)}")
            return True

        if len(points) == 1 and isinstance(points[0], list):
            points = points[0]
        else:
            points = list(points)

        if not value_check(points):
            pass

        return points

    @property
    def dimensions(self) -> int:
        return len(self)

    def __len__(self) -> int:
        return len(self.points)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.points})"

    def __eq__(self, other: "Vector") -> bool:
        if not isinstance(other, Vector):
            raise TypeError(
                f"Equality comparison with vector can only be performed with another vector, got {type(other)}"
            )

        return self.points == other.points

    def __getitem__(self, index: int) -> t.Union[int, float]:
        return self.points[index]

    def __setitem__(self, index: t.Union[int, tuple], value: t.Union[int, float]) -> None:
        if isinstance(value, (int, float)):
            self.points[index] = value
        else:
            raise TypeError(
                f"All values must be integers or floats, but value[{value}] is {type(value)}."
            )

    def __delitem__(self, index: int) -> None:
        del self.points[index]

    @classmethod
    def from_matrix(cls, matrix: "hm.Matrix") -> "Vector":
        if matrix.cols != 1:
            raise MatrixDimensionError("Matrix must only have 1 column.")

        points = [column[0] for column in matrix]
        return cls(*points)

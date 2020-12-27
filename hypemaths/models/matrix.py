import typing as t

from hypemaths.exceptions import InvalidMatrixError, MatrixDimensionError


class Matrix:
    def __init__(
            self, matrix: t.Union[int, float, list] = None, dims: tuple = None, fill: t.Union[int, float] = None
    ) -> None:
        if not matrix:
            if not dims or fill is not None:
                self.matrix = self._create_filled_matrix(dims, fill)
            else:
                raise ValueError("You need to pass the dimensions of the matrix or the fill value!")
        else:
            self.matrix = self._cleaned_matrix(matrix)

    @property
    def rows(self) -> int:
        return len(self.matrix)

    @property
    def cols(self) -> int:
        return len(self.matrix[0])

    @property
    def dims(self) -> tuple:
        return tuple(self._get_mat_dimension(self.matrix))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.matrix})"

    def __eq__(self, other: "Matrix") -> bool:
        if not isinstance(other, Matrix):
            raise TypeError(f"Equality comparison with Matrix can only be performed with another Matrix, got {type(other)}")

        return self.matrix == other.matrix

    def __getitem__(self, index: int) -> t.Union[int, float, list]:
        return self.matrix[index]

    def __setitem__(self, index: int, value: list) -> None:
        self.matrix[index] = value

    def __add__(self, other: "Matrix") -> "Matrix":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(f"Matrix can only be added with other matrix. Not {type(other)}")

        if not (self.rows, self.cols) == (other.rows, other.cols):
            raise MatrixDimensionError("These matrices cannot be added due to wrong dimensions.")

        matrix = [[self[row][cols] + other[row][cols] for cols in range(self.cols)] for row in range(self.rows)]

        return cls(matrix)

    def __sub__(self, other: "Matrix") -> "Matrix":
        cls = self.__class__

        if not isinstance(other, cls):
            raise TypeError(f"Matrix can only be added with other matrix. Not {type(other)}")

        return (self + other * -1)

    def __mul__(self, other: t.Union["Matrix", int, float]) -> "Matrix":
        cls = self.__class__

        if isinstance(other, int) or isinstance(other, float):
            matrix = [[other * element for element in self_row] for self_row in self]
            return cls(matrix)

        if not isinstance(other, cls):
            raise TypeError(f"Matrix can only be multiplied with other matrix. Not {type(other)}")

        if self.cols != other.rows:
            raise MatrixDimensionError("These matrices cannot be multiplied due to wrong dimensions.")

        matrix = [[
            sum(a * b for a, b in zip(self_row, other_col)) for other_col in zip(*other)] for self_row in self
        ]

        return cls(matrix)

    def transpose(self) -> "Matrix":
        """Transposes the matrix."""
        cls = self.__class__

        matrix = [[self[cols][row] for cols in range(self.rows)] for row in range(self.cols)]

        return cls(matrix)

    @staticmethod
    def _cleaned_matrix(matrix: list) -> list:
        """Checks if a matrix passed is valid or not and returns the clean matrix."""
        def contains_sublist(mat: list) -> bool:
            return all(isinstance(element, list) for element in mat)

        def value_check(mat: list) -> bool:
            for row, row_values in enumerate(mat):
                for col, value in enumerate(row_values):
                    if not isinstance(value, (int, float)):
                        raise TypeError(
                            f"All values must be integers or floats, but value[{row}][{col}] is {type(value)}"
                        )
            return True

        if isinstance(matrix, (int, float)):
            return [[matrix]]

        matrix = [matrix] if not contains_sublist(matrix) else matrix
        if value_check(matrix):
            len_set = set([len(x) for x in matrix])
            if len(len_set) > 1 and value_check(matrix):
                raise InvalidMatrixError(
                    "Matrix sizes are invalid! Must have same number of element in each sub list."
                )
            return matrix

    @staticmethod
    def _create_filled_matrix(dims: tuple, fill: t.Union[int, float]) -> list:
        if len(dims) != 2:
            raise ValueError("You must pass the 2 DIMENSIONS for the Matrix fill.")

        if not isinstance(fill, (int, float)):
            raise TypeError(
                f"The fill value must be integer or float, but the given fill value is {type(fill)}."
            )

        matrix_structure = []
        first_row = [fill] * dims[1]
        for _ in range(dims[0]):
            matrix_structure.append(first_row.copy())

        return matrix_structure

    def _get_mat_dimension(self, matrix: list) -> list:
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

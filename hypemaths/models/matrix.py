import copy
import typing as t

import hypemaths as hm
from hypemaths.exceptions import (
    InvalidMatrixError,
    MatrixDimensionError,
    MatrixNotSquare,
)


class Matrix:
    def __init__(
            self,
            matrix: t.Union[int, float, list] = None,
            dims: tuple = None,
            fill: t.Union[int, float] = None,
    ) -> None:
        """
        Parameters
        ----------
        matrix : t.Union[int, float, list]
            This is the nested 2D lists which will be converted into an efficient `Matrix` object capable of several
            calculations and features. Defaults to `None`.
        dims : tuple
            This is the dimensions of the fill matrix, created when the `matrix` parameter is not specified and only
            this value and the fill value is provided. Defaults to `None`.
        fill : t.Union[int, float]
            This is the fill value, which works with the `dims` parameter to create a filled matrix with the given
            value. Defaults to `None`.
        """
        if not matrix:
            if dims is not None:
                self.matrix = self._create_filled_matrix(dims, fill)
            else:
                raise ValueError("You need to pass the dimensions of the matrix or the fill value!")
        else:
            self.matrix = self._cleaned_matrix(matrix)

    @property
    def rows(self) -> int:
        """
        Returns
        -------
        int
            The number of rows in the 2D matrix created.
        """
        return len(self.matrix)

    @property
    def cols(self) -> int:
        """
        Returns
        -------
        int
            The number of the columns in the 2D matrix created.
        """
        return len(self.matrix[0])

    @property
    def dims(self) -> tuple:
        """
        Returns
        -------
        tuple
            The tuple containing the shape or the rows and columns in the matrix created.
        """
        return tuple(self._get_mat_dimension(self.matrix))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.matrix})"

    def __eq__(self, other: "Matrix") -> bool:
        if not isinstance(other, Matrix):
            raise TypeError(
                f"Equality comparison with Matrix can only be performed with another Matrix, got {type(other)}"
            )

        return self.matrix == other.matrix

    def __getitem__(self, index: t.Union[int, tuple]) -> t.Union[int, float, list]:
        if isinstance(index, int):
            return self.matrix[index]
        else:
            return self.matrix[index[0]][index[1]]

    def __setitem__(self, index: t.Union[int, tuple], value: t.Union[int, float]) -> None:
        if isinstance(value, (int, float)):
            if isinstance(index, int):
                self.matrix[index] = value
            else:
                self.matrix[index[0]][index[1]] = value
        else:
            raise TypeError(
                f"All values must be integers or floats, but value[{value}] is {type(value)}."
            )

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
            raise TypeError(f"Matrix can only be subtracted with other matrix. Not {type(other)}")

        if not (self.rows, self.cols) == (other.rows, other.cols):
            raise MatrixDimensionError("These matrices cannot be subtracted due to wrong dimensions.")

        matrix = [[self[row][cols] - other[row][cols] for cols in range(self.cols)] for row in range(self.rows)]

        return cls(matrix)

    def __mul__(self, other: t.Union["Matrix"]) -> "Matrix":
        cls = self.__class__

        if isinstance(other, (int, float)):
            matrix = [[element * other for element in row] for row in self]
            return cls(matrix)

        if not isinstance(other, cls):
            raise TypeError(f"Matrix can only be multiplied with other matrix. Not {type(other)}")

        if self.cols != other.rows:
            raise MatrixDimensionError("These matrices cannot be multiplied due to wrong dimensions.")

        matrix = [[
            sum(a * b for a, b in zip(self_row, other_col)) for other_col in zip(*other)] for self_row in self
        ]

        return cls(matrix)

    def __truediv__(self, other: "Matrix") -> "Matrix":
        cls = self.__class__

        if isinstance(other, (int, float)):
            matrix = [[element / other for element in row] for row in self]
            return cls(matrix)

        if not isinstance(other, cls):
            raise TypeError(f"Matrix can only be divided with other matrix. Not {type(other)}")

        if self.cols != other.rows:
            raise MatrixDimensionError("These matrices cannot be divided due to wrong dimensions.")

        matrix = [[
            sum(a / b for a, b in zip(self_row, other_col)) for other_col in zip(*other)] for self_row in self
        ]

        return cls(matrix)

    def __radd__(self, other: "Matrix") -> "Matrix":
        return self.__add__(other)

    def __rmul__(self, other: "Matrix") -> "Matrix":
        return self.__mul__(other)

    def __matmul__(self, other: "Matrix") -> "Matrix":
        return self.__mul__(other)

    @staticmethod
    def _cleaned_matrix(matrix: list) -> list:
        """
        Checks if a matrix passed is valid or not and returns the processed and cleaned matrix.

        Parameters
        ----------
        matrix : list
            The matrix passed to this function for processing, validation and cleaning.

        Returns
        -------
        list
            The list consisting the validated and cleaned matrix after passing the checks.

        Raises
        ------
        TypeError
            If the matrix contains any datatype other than `int` or `float`.
        InvalidMatrixError
            If the matrix has invalid size or cannot be validated.
        """
        def contains_sublist(mat: list) -> bool:
            """
            Parameters
            ----------
            mat: list
                The matrix passed for checking if it contains sublist.

            Returns
            -------
            bool
                If the matrix passed contains sublist.
            """
            return all(isinstance(element, list) for element in mat)

        def value_check(mat: list) -> bool:
            """
            Parameters
            ----------
            mat: list
                The matrix passed for validating the datatypes in it.

            Returns
            -------
            bool
                If the matrix contains any datatypes other than `int` or `float`.

            Raises
            ------
            TypeError
                Raised if the matrix consists of value which is not a `int` or `float`.
            """
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
    def _create_filled_matrix(dims: tuple, fill: t.Union[int, float] = None) -> list:
        """
        Parameters
        ----------
        dims: tuple
            The dimensions for the matrix to be initialized. Only 2 dimensions (X, Y) are allowed.
        fill: t.Union[int, float]
            The value to be filled across the matrix of the specified dimension.

        Returns
        -------
        list
            The 2D python list, to be converted into `Matrix` object.

        Raises
        ------
        ValueError
            If the number of dimensions don't equal to 2.
        TypeError
            If the fill value isn't either `int` or `float`.
        """
        if len(dims) != 2:
            raise ValueError("You must pass the 2 DIMENSIONS for the Matrix fill.")

        if not fill:
            fill = 0

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
        """
        Parameters
        ----------
        matrix : list
            The matrix whose dimensions are to be figured out.

        Returns
        -------
        list
            A tuple containing the dimensions of the matrix passed.
        """
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

    def clone(self) -> "Matrix":
        """
        Returns the copy of the matrix.

        Returns
        -------
        Matrix
            The copy of the present matrix.

        Examples
        --------
        Getting the copy instead of directly assigning, when you want to modify the matrix without disturbing the first one.

        >>> from hypemaths import Matrix
        >>> matrix = Matrix([[1, 2], [3, 4]])
        >>> matrix.clone()
        Matrix([[1, 2], [3, 4]])
        """
        return copy.deepcopy(self)

    def trace(self) -> t.Union[int, float]:
        """
        Returns the sum of the diagonals of the matrix

        Returns
        -------
        t.Union[int, float]
            The sum of the diagonals of the current `Matrix`

        Raises
        ------
        MatrixNotSquare
            If the number of columns and rows are not equal in the `Matrix`.

        Examples
        --------
        Getting the sum of the rows of the specified matrix.

        >>> from hypemaths import Matrix
        >>> matrix = Matrix([[5, 5], [3, 4]])
        >>> matrix.trace()
        9
        """
        if self.rows != self.cols:
            raise MatrixNotSquare("Cannot retrieve the sum of diagonals as the row and column count are not same.")

        total = 0
        for i in range(self.rows):
            total += self[i, i]
        return total

    def transpose(self) -> "Matrix":
        """
        Transposes the matrix.

        This converts the matrix elements order, by converting the rows into columns and vice versa.

        Returns
        -------
        Matrix
            The transposed matrix.

        Examples
        --------
        >>> from hypemaths import Matrix
        >>> mat = Matrix([[1, 2], [3, 4]])
        >>> mat.transpose()
        Matrix([[1, 3], [2, 4]])
        """
        cls = self.__class__

        matrix = [[self[cols][row] for cols in range(self.rows)] for row in range(self.cols)]

        return cls(matrix)

    @classmethod
    def from_vector(cls, vector: "hm.Vector") -> "Matrix":
        """
        Convert a `Vector` into a `Matrix` object.

        Parameters
        ----------
        vector: Vector
            The vector which is going to be converted into Matrix.

        Returns
        -------
        Matrix
            The matrix formed after conversion of vector.

        Examples
        --------
        >>> from hypemaths import Vector
        >>> vec = Vector(1, 2, 3, 4)
        >>> vec
        Vector([1, 2, 3, 4])
        >>> Matrix.from_vector(vec)
        Matrix([[1], [2], [3], [4]])
        """
        matrix_list = []
        for value in vector:
            matrix_list.append([value])

        return cls(matrix_list)

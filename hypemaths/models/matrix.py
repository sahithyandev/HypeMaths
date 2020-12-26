import typing as t

from hypemaths.exceptions import InvalidMatrixError


class Matrix:
    def __init__(
            self, matrix: t.Union[int, float, list] = None, dims: tuple = None, fill: t.Union[int, float] = None
    ) -> None:
        if not matrix:
            if not dims or fill:
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
        try:
            return len(self.matrix[0])
        except TypeError:  #
            return 1

    @property
    def dims(self) -> tuple:
        return tuple(self._get_mat_dimension(self.matrix))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.matrix})"

    @staticmethod
    def _cleaned_matrix(matrix: list) -> list:
        """Checks if a matrix passed is valid or not and returns the clean matrix."""
        def contains_sublist(mat: list) -> bool:
            return all(isinstance(element, list) for element in mat)

        def value_check(mat: list) -> bool:
            for row, row_values in enumerate(mat):
                if not contains_sublist(mat):
                    if not isinstance(row_values, (int, float)):
                        raise TypeError(
                            f"All values must be integers or floats, but value[{row}] is {type(row_values)}"
                        )
                else:
                    for col, value in enumerate(row_values):
                        if not isinstance(value, (int, float)):
                            raise TypeError(
                                f"All values must be integers or floats, but value[{row}][{col}] is {type(value)}"
                            )
            return True

        if isinstance(matrix, (int, float)):
            return [[matrix]]

        if isinstance(matrix, (int, float)):
            return [[matrix]]

        if value_check(matrix):
            if not contains_sublist(matrix):
                return matrix
            else:
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

        return [[fill] * dims[1]] * dims[0]

    def _get_mat_dimension(self, matrix: list) -> list:
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

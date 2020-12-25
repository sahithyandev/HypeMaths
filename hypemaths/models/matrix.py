import typing as t

from hypemaths.exceptions import InvalidMatrixError


class Matrix:
    def __init__(self, matrix: t.Union[int, float, list] = None, dims: tuple = None, fill: t.Union[int, float] = None) -> None:
        if not matrix:
            if not dims or fill:
                raise ValueError("You need to pass the dimensions of the matrix or the fill value!")

        else:
            self.matrix = self._cleaned_matrix(matrix)

    def _cleaned_matrix(self, matrix: list) -> list:
        """Checks if a matrix passed is valid or not and returns the clean matrix."""
        if isinstance(matrix, (int, float)):
            return [[matrix]]

        if len(matrix) == 1:
            if isinstance(matrix[0], list):
                return matrix
            return [matrix]

        if len(matrix) >= 2:
            if not isinstance(matrix[0], list):
                return matrix
            else:
                len_set = set([len(x) for x in matrix])
                if len(len_set) > 1:
                    raise InvalidMatrixError(
                        "Matrix sizes are invalid! Must have same number of element in each sub list."
                    )
                return matrix

        raise InvalidMatrixError("Matrix sizes are invalid!")

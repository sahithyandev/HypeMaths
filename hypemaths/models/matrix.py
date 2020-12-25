import typing as t

from hypemaths.exceptions import InvalidMatrixError


class Matrix:
    def __init__(
            self, matrix: t.Union[int, float, list] = None, dims: tuple = None, fill: t.Union[int, float] = None
    ) -> None:
        if not matrix:
            if not dims or fill:
                raise ValueError("You need to pass the dimensions of the matrix or the fill value!")

        else:
            self.matrix = self._cleaned_matrix(matrix)
            self.dims = tuple(self._get_mat_dimension(matrix))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.matrix})"

    @staticmethod
    def _cleaned_matrix(matrix: list) -> list:
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
                is_valid_matrix = all(isinstance(element, list) for element in matrix)
                if not is_valid_matrix:
                    raise InvalidMatrixError(
                        "Matrix sizes are invalid! Must have same number of element in each sub list."
                    )
                return matrix

        raise InvalidMatrixError("Matrix sizes are invalid!")

    def _get_mat_dimension(self, matrix: list) -> list:
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

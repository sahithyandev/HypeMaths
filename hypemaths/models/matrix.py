from hypemaths.exceptions import InvalidMatrixError


class Matrix:
    def __init__(self, values: list) -> None:
        if self._is_valid_matrix(values):
            self.matrix = values

    def _is_valid_matrix(self, matrix: list) -> bool:
        """Checks if a matrix passed is valid or not."""
        if len(matrix) == 1:
            if isinstance(matrix[0], list):
                if not len(matrix[0]) >= 2:
                    raise InvalidMatrixError("Matrix size must be at least 1 column and 2 rows")
                return True
            raise InvalidMatrixError("Matrix size must be atleast 2 columns")

        if len(matrix) >= 2:
            for i in range(1, len(matrix)):
                if len(matrix[i]) != len(matrix[0]):
                    raise InvalidMatrixError(
                        "Matrix sizes are invalid! Must have same number of element in each sub list."
                    )
                return True

        raise InvalidMatrixError("Matrix sizes are invalid!")

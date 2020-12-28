import unittest

from hypemaths import Matrix
from hypemaths.exceptions import InvalidMatrixError


class ValidMatrixTests(unittest.TestCase):
    """Tests for checking the validation when a Matrix is initialized."""
    def test_valid_matrix(self) -> None:
        test_cases = (
            (Matrix(1), [[1]]),
            (Matrix([1, 2, 3, 4]), [[1, 2, 3, 4]]),
            (Matrix([[1, 2], [3, 4]]), [[1, 2], [3, 4]])
        )

        for matrix, matrix_value in test_cases:
            self.assertEqual(matrix.matrix, matrix_value)

    def test_invalid_matrix(self) -> None:
        test_cases = (
            "test",
            ["This", "is", "just", "a", "test"],
            [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        )

        for test in test_cases:
            with self.assertRaises((TypeError, InvalidMatrixError)):
                Matrix(test)


class MatrixAttributesTests(unittest.TestCase):
    """Tests for checking the attributes when a Matrix is created."""
    def test_matrix_rows(self) -> None:
        test_cases = (
            (Matrix(1), 1),
            (Matrix([1, 2, 3, 4]), 1),
            (Matrix([[1, 2], [3, 4]]), 2)
        )

        for matrix, row_value in test_cases:
            self.assertEqual(matrix.rows, row_value)

    def test_matrix_columns(self) -> None:
        test_cases = (
            (Matrix(1), 1),
            (Matrix([1, 2, 3, 4]), 4),
            (Matrix([[1, 2], [3, 4]]), 2),
            (
                Matrix([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]), 3
            )
        )

        for matrix, column_value in test_cases:
            self.assertEqual(matrix.cols, column_value)

    def test_matrix_dims(self) -> None:
        test_cases = (
            (Matrix(1), (1, 1)),
            (Matrix([1, 2, 3, 4]), (1, 4)),
            (Matrix([[1, 2], [3, 4]]), (2, 2)),
            (
                Matrix([
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9]
                ]), (3, 3)
            )
        )

        for matrix, matrix_dims in test_cases:
            self.assertEqual(matrix.dims, matrix_dims)


class MatrixOperationTests(unittest.TestCase):
    def test_matrix_addition(self) -> None:
        test_cases = (
            (Matrix(1), Matrix(1), Matrix([[2]])),
            (
                Matrix([1, 2, 3, 4]),
                Matrix([6, 6, 2, 6]),
                Matrix([[7, 8, 5, 10]])
            ),
            (
                Matrix([[5, 6], [9, 3]]),
                Matrix([[3, 8], [9, 2]]),
                Matrix([[8, 14], [18, 5]])
            )
        )

        for matrix_a, matrix_b, matrix_sum in test_cases:
            self.assertEqual(matrix_a + matrix_b, matrix_sum)

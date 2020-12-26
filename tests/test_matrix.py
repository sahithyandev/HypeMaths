import unittest

from hypemaths import Matrix
from hypemaths.exceptions import InvalidMatrixError


class ValidMatrixTests(unittest.TestCase):
    """Tests for checking the validation when a Matrix is initialized."""
    def test_valid_matrix(self) -> None:
        test_cases = (
            (Matrix(1), [[1]]),
            (Matrix([1, 2, 3, 4]), [1, 2, 3, 4]),
            (Matrix([[1, 2, 3, 4]]), [[1, 2, 3, 4]]),
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

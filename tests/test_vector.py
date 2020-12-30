import unittest

from hypemaths import Vector
from hypemaths.exceptions import (
    InvalidVectorError
)


class ValidVectorTests(unittest.TestCase):
    """Tests for checking the validation when a Vector is initialized."""
    def test_valid_vector(self) -> None:
        test_cases = (
            (Vector(1, 2, 3, 4), [1, 2, 3, 4]),
            (Vector([4, 9, 8, 1]), [4, 9, 8, 1]),
            (Vector(1), [1])
        )

        for vector, vector_values in test_cases:
            self.assertEqual(vector.points, vector_values)

    def test_invalid_vector(self) -> None:
        test_cases = (
            "test",
            ["This", "is", "just", "a", "test"],
            [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        )

        for test in test_cases:
            with self.assertRaises((TypeError, InvalidVectorError)):
                Vector(test)


class VectorComparisonTests(unittest.TestCase):
    def test_vector_equality(self) -> None:
        test_cases = (
            (
                Vector(1),
                Vector([1])
            ),
            (
                Vector(1, 7, 0),
                Vector([1, 7, 0])
            ),
            (
                Vector([13, 4, 7]),
                Vector([13, 4, 7])
            )
        )

        for vector_1, vector_2 in test_cases:
            self.assertEqual(vector_1, vector_2)

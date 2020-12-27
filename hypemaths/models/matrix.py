import typing as t

from hypemaths.exceptions import InvalidMatrixError


class Matrix:
    def __init__(
            self, matrix: t.Union[int, float, list] = None, dims: tuple = None, fill: t.Union[int, float] = None
    ) -> None:
        if not matrix:
            if not dims or fill != None:
                self.matrix = self._create_filled_matrix(dims, fill)
            else:
                raise ValueError("You need to pass the dimensions of the matrix or the fill value!")
        else:
            self.matrix = self._cleaned_matrix(matrix)

    def __getitem__(self, row_index):
        return self.matrix[row_index]

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

    def multiply_by_number(self, number):
        '''
        Multiplies the current matrix with a number.
        '''
        if type(number) is not int:
            raise TypeError(f"Expected `int` but got {type(number).__name__} ({number})")

        original_matrix = self.matrix
        new_matrix = Matrix(dims=[original_matrix.rows, original_matrix.cols], fill=0)

        for row_i in range(original_matrix.rows):
            for column_i in range(original_matrix.cols):
                new_matrix[row_i][column_i] = number * original_matrix[row_i][column_i]

        return new_matrix

    def transpose(self):
        '''
        Transposes the matrix
        '''
        # [A.cols, A.rows] is the dimension of the new matrix
        new_matrix = Matrix(dims=[self.cols, self.rows], fill=0)

        for row_i in range(self.rows):
            for column_i in range(self.cols):
                new_matrix[column_i][row_i] = self[row_i][column_i]

        return new_matrix

    @staticmethod
    def multiply_by_matrix(A, B) -> list:
        '''
        Multiplies two matrices and returns a new matrix
        Takes in 2 matrices a, b
        '''
        if not (Matrix.is_matrix(A) and Matrix.is_matrix(B)):
            raise TypeError(f"Expected 2 Matrices but got {type(A).__name__}, {type(B).__name__}")

        if A.cols != B.rows:
            raise Exception("For matrix multiplication, the number of columns in the first matrix must be equal to the number of rows in the second matrix.")

        new_matrix = Matrix(dims=[A.rows, B.cols], fill=0)

        for row_i in range(A.rows):
            for column_i in range(B.cols):
                sum = 0
                for k in range(A.cols):
                    sum += A[row_i][k] * B[k][column_i]

                new_matrix[row_i][column_i] = sum
                # print(row, column)

        return new_matrix

    @staticmethod
    def add_matrices(A, B):
        if not (Matrix.is_matrix(A) and Matrix.is_matrix(B)):
            raise TypeError(f"Expected 2 Matrices but got {type(A).__name__}, {type(B).__name__}")

        if A.cols != B.cols or A.rows != B.rows:
            raise Exception("Two matrices must have an equal number of rows and columns to be added.")

        added_matrix = Matrix(dims=[A.rows, A.cols], fill=0)
        for i in range(A.rows):
            for j in range(A.cols):
                added_matrix[i][j] = A[i][j] + B[i][j]

        return added_matrix

    @staticmethod
    def is_matrix(A):
        # TODO try not to use hard code "Matrix" here
        return type(A).__name__ == 'Matrix'

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

        # Reason:
        #   n = Matrix(dims=[2, 3], fill=0)
        #   n[1][1] = 45
        #   print(n) # Matrix([[0, 45, 0], [0, 45, 0]])
        # to stop this from happening

        matrix_structure = []
        first_row = [fill] * dims[1]
        for _ in range(dims[0]):
            matrix_structure.append(first_row.copy())

        return matrix_structure

    def _get_mat_dimension(self, matrix: list) -> list:
        if not isinstance(matrix, list):
            return []
        return [len(matrix)] + self._get_mat_dimension(matrix[0])

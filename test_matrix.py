import unittest
from matrix import Matrix


class TestMatrix(unittest.TestCase):

    def test_random_matrix(self):
        n = 3
        m = 4
        matrix = Matrix.random_by_size(n, m)
        self.assertEqual(matrix.n_rows, n)
        self.assertEqual(matrix.n_columns, m)

    def test_bad_row(self):
        matrix = Matrix([
            [1, 2],
            [3, 4]
        ])

        def bad_setting():
            matrix[2] = [1, 2, 3]
        self.assertRaises(ValueError, bad_setting)

    def test_bad_init(self):
        def bad_init_1():
            Matrix(3)
        self.assertRaises(ValueError, bad_init_1)

        def bad_init_2():
            Matrix([3])
        self.assertRaises(ValueError, bad_init_2)

    def test_transposing(self):
        matrix1 = Matrix([
            [1, 2],
            [3, 4]
        ])

        matrix2 = Matrix([
            [1, 3],
            [2, 4]
        ])

        self.assertEqual(matrix1.transponed(), matrix2)


if __name__ == "__main__":
    unittest.main()

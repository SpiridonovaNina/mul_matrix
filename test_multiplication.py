"""
Модуль для тестирования перемножения матриц.
Должен запускаться через MPI:
    mpirun -n 3 python3 test_multiplication.py
Само тестирование проходит для master-процесса
Slave-процессы работают без остановки
"""
import unittest
from master import MulMatrixApp
from matrix import Matrix


class TestMultiplication(unittest.TestCase):
    app = MulMatrixApp()

    @classmethod
    def tearDownClass(cls):
        """
        Метод для остановки Slave-процессов после завершения всех тестов
        этого класса
        """
        cls.app = MulMatrixApp(debug=False)
        cls.app.stop_slaves()

    def test_good_case(self):
        matrix1 = Matrix([
                [1, 2],
                [3, 4]
            ])
        matrix2 = matrix1
        result = self.app.multiply_matrixes(matrix1, matrix2)
        self.assertEqual(result, Matrix([
                [7, 10],
                [15, 22]
            ])
        )

    def test_small_matrixes(self):
        matrix1 = Matrix([[2]])
        matrix2 = Matrix([[3]])
        result = self.app.multiply_matrixes(matrix1, matrix2)
        self.assertEqual(result, Matrix([[6]]))

    def test_zero_matrix(self):
        matrix1 = Matrix([
                [0, 0],
                [0, 0]
            ])
        matrix2 = matrix1
        result = self.app.multiply_matrixes(matrix1, matrix2)
        self.assertEqual(result, Matrix([
                [0, 0],
                [0, 0]
            ])
        )


if __name__ == "__main__":
    app = MulMatrixApp(debug=False)
    if app.rank == 0:
        unittest.main()
    else:
        app.run_slave()

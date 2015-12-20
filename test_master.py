import unittest
import sys
import os
from subprocess import call
import master


class BaseCommand(object):

    """
    Класс для формирования базовой комманды для запуска скрипта
    """
    mpirun = 'mpirun'
    num_processes = 2
    python3 = sys.executable
    master_py = master.__file__
    args = ['2', '2', '2', '2']

    def as_list(self):
        """
        Возвращает список для вызова subprocess.call
        Пример:
        [mpirun, -n, 4, python3, master.py, 2, 2, 2, 2]
        """
        return [self.mpirun, '-n', str(self.num_processes), self.python3,
                self.master_py] + self.args

    def call(self):
        with open(os.devnull, 'w') as devnull_file:
            return call(self.as_list(), stdout=devnull_file,
                        stderr=devnull_file)


class TestMaster(unittest.TestCase):

    """
    Класс для тестирования параметров запуска перемножения матриц
    """

    def setUp(self):
        self.command = BaseCommand()

    def test_good_case(self):
        """
        Когда все параметры переданы верно
        """
        self.assertEqual(self.command.call(), 0)

    def test_edge_size(self):
        self.command.args = ['1', '1', '1', '1']
        self.assertEqual(self.command.call(), 0)

    def test_not_square_matrix(self):
        self.command.args = ['1', '2', '2', '3']
        self.assertEqual(self.command.call(), 0)

    def test_not_enough_params(self):
        self.command.args = ['1', '2']
        self.assertNotEqual(self.command.call(), 0)

    def test_too_many_params(self):
        self.command.args = ['1', '2', '3', '4', '5']
        self.assertNotEqual(self.command.call(), 0)

    def test_bad_matrix_size(self):
        self.command.args = ['1', '2', '3', '4']
        self.assertNotEqual(self.command.call(), 0)

    def test_negative_matrix_size(self):
        self.command.args = ['-1', '2', '3', '4']
        self.assertNotEqual(self.command.call(), 0)

    def test_single_process(self):
        self.command.num_processes = 1
        self.assertNotEqual(self.command.call(), 0)

    def test_overhead_processes(self):
        self.command.num_processes = 5
        self.assertEqual(self.command.call(), 0)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python
import logging
import argparse
from itertools import cycle
from time import sleep
from mpi4py import MPI
from matrix import Matrix

DEBUG = False

# настраиваем логирование и формат отладочной инфорамции
if DEBUG:
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s]: %(message)s')


class MulMatrixApp(object):

    def __init__(self, debug=False):
        self.debug = debug
        self.comm = MPI.COMM_WORLD           # получаем текущий коммуникатор
        self.size = self.comm.Get_size()     # узнаем количество процессов
        self.rank = self.comm.Get_rank()     # узнаем id процесса
        if self.size < 2:
            raise RuntimeError(
                "Должно быть запущено по крайней мере 2 процесса")

    def multiply_matrixes(self, matrix1, matrix2):
        """
        основная функция главного процесса, которая занимается перемножением
        матриц. Распределяет задачи для процессов, ожидает от них результатов.
        Суть - поочерёдно раздаем задачи для всех процессов.
        Как только встретился процесс, который уже выполняет задачу, ожидаем
        её завершения и выдаем ему новую задачу.
        После перемножения всех строк и столбцов, отправляем все процессам
        пустую задачу чтобы они завершили своё выполнение.
        Таким образом, задачу перемножения матриц может решить от 2-х до
        неограниченного числа процессов. Часть из них просто не будут ничего
        делать
        """
        reqs = [None] * self.size  # MPI.Request для работы с процессами
        results = []  # куда будут записаны результаты работы процессов

        # бесконечный итератор по идентификаторам slave-процессов
        slaves_id_iterator = cycle(range(1, self.size))
        for row1 in matrix1:
            for column2 in matrix2.transponed():
                slave_id = next(slaves_id_iterator)

                # если очередной slave уже выполняет какую-то задачу -
                # дождёмся завершения
                if reqs[slave_id] is not None:
                    res = reqs[slave_id].wait()
                    logging.debug("{} returned {}".format(slave_id, res))
                    results.append(res)

                # выдадим очередную задачу очередному slave
                self.comm.send([row1, column2], dest=slave_id)
                reqs[slave_id] = self.comm.irecv(source=slave_id)

        # соберём результаты работы со всех оставшихся slave
        slave_id = next(slaves_id_iterator)
        start_id = slave_id
        while True:
            # получаем очередной результат
            if reqs[slave_id]:
                res = reqs[slave_id].wait()
                logging.debug("{} returned {}".format(slave_id, res))
                results.append(res)

            # запишем None как отметку о том, что мы получили от этого slave
            reqs[slave_id] = None

            slave_id = next(slaves_id_iterator)
            if slave_id == start_id:
                break

        return Matrix.from_list(results, n_rows=matrix1.n_rows)

    def run_master(self):
        args = self.get_args()

        if args.m1 != args.n2:
            raise RuntimeError(
                "Невозможно перемножить матрицы заданного размера")

        matrix1 = Matrix.random_by_size(args.n1, args.m1)
        matrix2 = Matrix.random_by_size(args.n2, args.m2)
        print("Matrix 1:")
        print(matrix1)
        print("")
        print("Matrix 2:")
        print(matrix2)
        print("")

        result_matrix = self.multiply_matrixes(matrix1, matrix2)

        print("Result matrix:")
        print(result_matrix)

    def run_slave(self):
        while True:
            # получаем данные с прмощью блокирующегоо вызова
            row, column = self.comm.recv(source=0)
            logging.debug("{} received {}".format(self.rank, (row, column)))
            # если пришла пустая задача - выход
            if row is None or column is None:
                break

            # самая суть - перемножение строки на столбец
            res = sum([a * b for a, b in zip(row, column)])

            if self.debug:
                sleep(2)
            self.comm.send(res, dest=0)
        logging.debug("{} exited".format(self.rank))

    def stop_slaves(self):
        # отправим всем slave пустую задачу, чтобы они завершили работу
        for slave_id in range(1, self.size):
            self.comm.send([None, None], dest=slave_id)

    def get_args(self):
        """ Функция для парсинга аргументов командной строки """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            'n1', type=int, help="number of first matrix rows")
        parser.add_argument(
            'm1', type=int, help="number of first matrix columns")
        parser.add_argument(
            'n2', type=int, help="number of second matrix rows")
        parser.add_argument(
            'm2', type=int, help="number of second matrix columns")
        return parser.parse_args()

    def run(self):
        if self.rank == 0:
            try:
                return self.run_master()
            finally:
                self.stop_slaves()
        else:
            return self.run_slave()


if __name__ == "__main__":
    app = MulMatrixApp(DEBUG)
    app.run()

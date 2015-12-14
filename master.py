#!/usr/bin/env python
import sys
import logging
from mpi4py import MPI
from matrix import Matrix


logging.basicConfig(level=logging.DEBUG,					# сообщение отладочное
                    format='[%(levelname)s]: %(message)s')  # формат выводимого сообщения
														   
class MulMatrixApp(object):

    def start_childs(self):
        self.num_childs = self.matrix1.n_rows * self.matrix2.n_columns
        return MPI.COMM_SELF.Spawn(sys.executable, args=['slave.py'], # создание коммуникатора
                                   maxprocs=self.num_childs)

    def send_data(self, comm):
        i = 0
        reqs = []
        for row1 in self.matrix1:
            for column2 in self.matrix2.transponed():
                req = comm.isend([row1, column2], dest=i) # передача сообщения без блокирови, dest-id процесса
                reqs.append(req) # сохранение состояний ответов
                i += 1

        for i in reqs:
            i.wait()	# ждем получения ответов от всех процессов

    def receive_data(self, comm):
        reqs = []
        N = self.matrix1.n_rows * self.matrix2.n_columns
        for i in range(N):
            reqs.append(comm.irecv(source=i))

        results = [None] * N
        all_done = False
        while not all_done:			#cпрашиваем у каждого процесса, готов ли он, если да то выводим его результат,
            all_done = True			#если нет переходим к другому процессу, и так далее пока все процессы не будут готовы
            for i in range(N):
                if results[i] is not None:
                    continue
                finished, res = reqs[i].test()
                if finished:
                    results[i] = res
                    logging.debug("{} proccess returned {}".format(i, res))
                else:
                    all_done = False

        return Matrix.from_list(results, n_rows=self.matrix1.n_rows)

    def run(self):
        self.matrix1 = Matrix.from_file('matrix1.txt')
        self.matrix2 = Matrix.from_file('matrix2.txt')
        print("Matrix 1:")
        print(self.matrix1)
        print("")
        print("Matrix 2:")
        print(self.matrix1)
        print("")

        comm = self.start_childs()
        self.send_data(comm)
        result_matrix = self.receive_data(comm)
        print("Result matrix:")
        print(result_matrix)


if __name__ == "__main__":
    app = MulMatrixApp()
    app.run()

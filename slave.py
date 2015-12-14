#!/usr/bin/env python
from mpi4py import MPI
from time import sleep
from random import random


DEBUG = True


comm = MPI.Comm.Get_parent()    # получаем текущий коммуникатор
size = comm.Get_size()          # узнаем количество процессов
rank = comm.Get_rank()          #узнаем id процесса

row, column = comm.recv(source=0)      # получаем данные с прмощью блокирующегоо вызова

res = sum([a * b for a, b in zip(row, column)])

if DEBUG:
    sleep(random() * 10)

comm.send(res, dest=0)

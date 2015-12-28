# скрипт для запуска всех тестов
python3 test_matrix.py &&
	python3 test_master.py &&
	mpirun -n 4 python3 test_multiplication.py

import collections
from random import randint


class Matrix(list):

    def __init__(self, iterable):
        if iterable:
            if not isinstance(iterable, collections.Iterable):
                raise ValueError("{} is not iterable".format(iterable))

            for row in iterable:
                if not isinstance(row, collections.Iterable):
                    raise ValueError("{} is not iterable".format(row))

            if len(iterable):
                n_cols = len(iterable[0])
                for row in iterable:
                    if len(row) != n_cols:
                        raise ValueError(
                            "Different number of columns in matrix's rows")

        return super().__init__(iterable)

    def __setitem__(self, key, value):
        """
        присваивание элемента с данным ключом или индексом;
        key - индекс элемента, value - строка матрицы
        """
        if isinstance(key, int):
            if not isinstance(value, collections.Iterable):
                raise ValueError("{} is not iterable".format(value))
            if len(value) != self.n_columns:
                raise ValueError("Bad length of row")
        return super().__setitem__(key, value)

    @classmethod
    def from_file(cls, filename):
        with open(filename) as f:
            matrix = []
            for line in f:
                matrix.append(list(map(int, line.split())))
        return cls(matrix)

    @classmethod
    def from_list(cls, iterable, n_rows):
        n_cols = len(iterable) // n_rows
        matrix = []
        for i in range(0, len(iterable), n_cols):
            matrix.append(iterable[i: i + n_cols])
        return cls(matrix)

    @classmethod
    def random_by_size(cls, n, m):
        """
        Сгенерировать матрицу MxN со случайными значениями
        """
        if not (m > 0 and n > 0):
            raise ValueError("Matrix size must be greter 0")
        matrix = []
        for i in range(n):
            matrix.append([randint(0, 9) for i in range(m)])
        return cls(matrix)

    def __repr__(self):
        """
        получение строкового представления объекта.
        генерирование форм, которые могут быть прочитаны интерпретатором
        """
        spr = super().__repr__()
        return "Matrix({})".format(spr)

    def __str__(self):
        """
        Получение строкового представления объекта.
        возврат значений в читабельной форме
        """
        return "\n".join(" ".join(map(str,row)) for row in self)

    @property
    def n_columns(self):
        return len(self[0])

    @property
    def n_rows(self):
        return len(self)

    def transponed(self):
        transponed = []
        for i in range(self.n_columns):
            transponed.append([row[i] for row in self])
        return Matrix(transponed)

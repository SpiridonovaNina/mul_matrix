import collections


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

        return super().__init__(iterable) # super() - получение объекта родительского класса

    def __setitem__(self, key, value): # присваивание элемента с данным ключом или индексом; key - индекс элемента, value - строка
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

    def __repr__(self): #  получения строкового представления объекта.генерирование форм, которые могут быть прочитаны интерпретатором
        spr = super().__repr__()        
        return "Matrix({})".format(spr)

    def __str__(self): # получения строкового представления объекта. возврат значений в читабельной форме
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

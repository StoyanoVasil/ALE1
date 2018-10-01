import numpy as np
from src.models.Tree import Tree
from src.models.Simplifier import Simplifier


class TruthTable:
    def __init__(self, expression):
        self.tree = Tree(expression)
        self.simplifier = Simplifier()
        self.__set_rows_and_columns()
        self.normalization = []
        self.__create_table()
        self.simplifier.simplify()
        self.__normalize()

    def __set_rows_and_columns(self):
        self.predicates = len(self.tree.unique_predicates)
        self.rows = 2**self.predicates
        self.columns = self.predicates + 1

    def __create_table(self):
        if self.predicates == 0:
            self.__create_table_no_predicates()
        else:
            self.__create_table_predicates()

    def __create_table_no_predicates(self):
        self.identification = self.tree.evaluate({})
        self.table = np.array([[self.tree.get_infix_expression()], [self.identification]])

    def __create_table_predicates(self):
        self.table = np.array([arr for arr in self.__table_row_generator()])
        self.__set_identification()
        self.__add_predicates_to_table()

    def __table_row_generator(self):
        for r in range(self.rows):
            yield self.__get_row(str(r + 1), bin(r)[2:].zfill(self.columns - 1))

    def __get_row(self, i, values):
        values_array = [int(i) for i in values]
        evaluation = self.tree.evaluate(self.__create_dict(values_array))
        if evaluation == 1:
            self.__add_to_normalization(values_array)
            self.simplifier.add_implicant(i, values_array)
        values_array.append(evaluation)
        return values_array

    def __create_dict(self, values):
        dict = {}
        for i, v in enumerate(self.tree.unique_predicates):
            dict[v] = values[i]
        return dict

    def __set_identification(self):
        binary = ''.join(reversed([str(i[-1]) for i in self.table]))
        self.identification = hex(int(binary, 2))[2:]

    def __add_predicates_to_table(self):
        predicates = [x for x in self.tree.unique_predicates]
        predicates.append(self.tree.get_infix_expression())
        self.table = np.vstack((np.array(predicates), self.table))

    def __add_to_normalization(self, values):
        dict = self.__create_dict(values)
        predicates = []
        for k, v in dict.items():
            if v == 1: predicates.append(f'{k}')
            else: predicates.append(f'¬{k}')
        norm = ' ⋀ '.join(predicates)
        self.normalization.append(f'({norm})')

    def __normalize(self):
        self.normalization = ' ⋁ '.join(self.normalization)


if __name__ == '__main__':
    t = TruthTable('|(A,|(B,C))')
    print(t.normalization)

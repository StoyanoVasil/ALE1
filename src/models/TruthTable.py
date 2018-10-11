from functools import reduce
from src.models.Tree import Tree
from src.models.Simplifier import Simplifier


class TruthTable:
    def __init__(self, expression):
        self.tree = Tree(expression)
        self.__set_rows_and_columns()
        self.simplifier = Simplifier(self.predicates)
        self.normalization = []
        self.simplified_table = []
        self.__create_table()
        self.__normalize()

    def simplify(self):
        self.__create_simplified_table()
        self.simplified_normalization = self.simplifier.normalization

    def __set_rows_and_columns(self):
        self.predicates = self.tree.unique_predicates
        self.rows = 2**len(self.predicates)
        self.columns = len(self.predicates) + 1

    def __create_table(self):
        if len(self.predicates) == 0:
            self.__create_table_no_predicates()
        else:
            self.__create_table_predicates()

    def __create_table_no_predicates(self):
        self.identification = self.tree.evaluate({})
        self.normalization = ''
        self.table = [[self.tree.get_infix_expression()], [self.identification]]

    def __create_table_predicates(self):
        self.table = [arr for arr in self.__table_row_generator()]
        self.__set_identification()
        self.__add_predicates_to_table()

    def __table_row_generator(self):
        for r in range(self.rows):
            yield self.__get_row(str(r), bin(r)[2:].zfill(self.columns - 1))

    def __get_row(self, i, values):
        values_array = [int(i) for i in values]
        evaluation = self.tree.evaluate(self.__create_dict(values_array))
        if evaluation == 1:
            self.__add_to_normalization(values_array)
            self.simplifier.add_implicant(i, values_array)
        else:
            self.simplified_table.append(values_array)
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
        self.table = [predicates] + self.table

    def __add_to_normalization(self, values):
        dict = self.__create_dict(values)
        predicates = []
        for k, v in dict.items():
            if v == 1: predicates.append(f'{k}')
            else: predicates.append(f'~({k})')
        norm = reduce(lambda x, y: f'&({x},{y})', predicates)
        self.normalization.append(f'{norm}')

    def __normalize(self):
        if len(self.normalization) > 0:
            self.normalization = reduce(lambda x, y: f'|({x},{y})',self.normalization)

    def __create_simplified_table(self):
        sim = self.simplifier.simplify()
        if sim:
            self.simplified_table = [self.table[0]] + sim + self.simplified_table
            bin = ''.join(reversed([str(i[-1]) for i in self.simplified_table[1:]]))
            self.simplified_identification = hex(int(bin, 2))[2:]
        else:
            self.simplified_identification = ''


# TODO: remove this shid
if __name__ == '__main__':
    t = TruthTable('>(|(~(A),~(&(J,B))),=(C,|(D,F)))')
    t1 = TruthTable(str(t.tree.nandify()))
    print(t.tree.get_infix_expression())
    print(t.normalization)
    t.simplify()
    print(t.simplified_normalization)
    # print(t1.normalization)
    # print(t1.tree.get_infix_expression())

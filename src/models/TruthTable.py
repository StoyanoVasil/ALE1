import numpy as np
import json
from src.models.Tree import Tree


class TruthTable:
    def __init__(self, expression):
        self.tree = Tree(expression)
        self.__set_rows_and_columns()
        self.__create_table()

    def __set_rows_and_columns(self):
        #TODO: fix no predicate error
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
            yield self.__get_row(bin(r)[2:].zfill(self.columns - 1))

    def __get_row(self, values):
        values_array = [int(i) for i in values]
        values_array.append(self.tree.evaluate(self.__create_dict(values_array)))
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

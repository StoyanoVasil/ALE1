import numpy as np
from src.models.Tree import Tree


class TruthTable:
    def __init__(self, expression):
        self.tree = Tree(expression)
        self._set_rows_and_columns()
        self._create_table()

    def _set_rows_and_columns(self):
        predicates = len(self.tree.unique_predicates)
        self.rows = 2**predicates
        self.columns = predicates + 1

    def _create_table(self):
        self.table = np.array([arr for arr in self._table_row_generator()])

    def _table_row_generator(self):
        for r in range(self.rows):
            yield self._get_row(bin(r)[2:].zfill(self.columns-1))

    def _get_row(self, values):
        values_array = [int(i) for i in values]
        values_array.append(self.tree.evaluate(self._create_dict(values_array)))
        return values_array

    def _create_dict(self, values):
        dict = {}
        for i, v in enumerate(self.tree.unique_predicates):
            dict[v] = values[i]
        return dict

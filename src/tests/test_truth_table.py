import unittest
from unittest.mock import MagicMock

from src.models.TruthTable import TruthTable


class TestTruthTabel(unittest.TestCase):

    def test_init(self):
        print('test_truth_table_init')
        expressions = ['&(A,B)', '|(A,B)', '=(A,B)', '>(A,B)', '~(A)', '1', 'A']
        normalizations = ['&(A,B)', '|(|(&(~(A),B),&(A,~(B))),&(A,B))', '|(&(~(A),~(B)),&(A,B))',
                          '|(|(&(~(A),~(B)),&(~(A),B)),&(A,B))', '~(A)', '', 'A']

        for i, exp in enumerate(expressions):
            table = TruthTable(exp)
            self.assertEqual(table.tree.get_infix_expression(), exp)
            self.assertEqual(table.normalization, normalizations[i])

    def test_simplification(self):
        print('test_truth_table_simplify')

        # contradiction
        table = TruthTable('&(A,~(A))')
        table.simplifier.simplify = MagicMock(return_value=None)
        table.simplify()
        self.assertEqual(table.simplified_table, [])
        self.assertEqual(table.simplified_identification, '')

        # any other expression
        table = TruthTable('&(A,A)')
        table.simplifier.simplify = MagicMock(return_value=[[0, 1], [1, 0]])
        table.simplify()
        self.assertEqual(table.simplified_table[1:3], [[0, 1], [1, 0]])


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock

from src.models.Simplifier import Simplifier


class TestSimplifier(unittest.TestCase):

    def setUp(self):
        self.s = Simplifier(['A', 'B'])

    def test_init(self):
        print('test_simplifier_init')
        self.assertEqual(self.s.predicates, ['A', 'B'])

    def test_add_implicant(self):
        print('test_simplifier_add_implicant')
        self.s.add_implicant(1, [0, 0])
        self.assertEqual(self.s.implicants, {0: [[1, '00', False]]})
        self.s.add_implicant(2, [0, 1])
        self.assertEqual(self.s.implicants, {0: [[1, '00', False]], 1: [[2, '01', False]]})
        self.s.add_implicant(3, [1, 0])
        self.assertEqual(self.s.implicants, {0: [[1, '00', False]], 1: [[2, '01', False], [3, '10', False]]})
        self.s.add_implicant(4, [1, 1])
        self.assertEqual(self.s.implicants, {0: [[1, '00', False]],
                                             1: [[2, '01', False], [3, '10', False]],
                                             2: [[4, '11', False]]})

    def test_simplify(self):
        print('test_simplifier_simplify')
        arr = {
            '0': [0, 0, 0, 0],
            '4': [0, 1, 0, 0],
            '5': [0, 1, 0, 1],
            '7': [0, 1, 1, 1],
            '8': [1, 0, 0, 0],
            '11': [1, 0, 1, 1],
            '12': [1, 1, 0, 0],
            '15': [1, 1, 1, 1]
        }
        s = Simplifier(['A', 'B', 'C', 'D'])
        for k, v in arr.items():
            s.add_implicant(k, v)
        s.simplify()
        self.assertEqual(s.final_implicants, [('11-15', '1*11'), ('0-4-8-12', '**00'), ('5-7', '01*1')])

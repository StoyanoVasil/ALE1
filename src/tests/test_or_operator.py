import unittest
from unittest.mock import MagicMock

from src.models.Nodes import Predicate, OrOperator, NandOperator


class TestOrOperator(unittest.TestCase):

    def setUp(self):
        self.l_child = Predicate('A')
        self.r_child = Predicate('B')
        self.binary = OrOperator('|', self.l_child, self.r_child)

    def test_evaluate(self):
        print('test_or_evaluate')

        # children returns 1 and 1
        self.l_child.evaluate = MagicMock(return_value=1)
        self.r_child.evaluate = MagicMock(return_value=1)
        self.assertEqual(self.binary.evaluate({}), True)

        # children returns 1 and 0
        self.l_child.evaluate = MagicMock(return_value=1)
        self.r_child.evaluate = MagicMock(return_value=0)
        self.assertEqual(self.binary.evaluate({}), True)

        # children returns 0 and 1
        self.l_child.evaluate = MagicMock(return_value=0)
        self.r_child.evaluate = MagicMock(return_value=1)
        self.assertEqual(self.binary.evaluate({}), True)

        # children returns 0 and 0
        self.l_child.evaluate = MagicMock(return_value=0)
        self.r_child.evaluate = MagicMock(return_value=0)
        self.assertEqual(self.binary.evaluate({}), False)

    def test_nandify(self):
        print('test_or_nandify')
        and_nand = self.binary.nandify()

        self.assertIsInstance(and_nand, NandOperator)
        self.assertEqual(and_nand.label, '%')
        self.assertEqual(and_nand.evaluate({'A': 1, 'B': 1}), self.binary.evaluate({'A': 1, 'B': 1}))
        self.assertEqual(and_nand.evaluate({'A': 1, 'B': 0}), self.binary.evaluate({'A': 1, 'B': 0}))
        self.assertEqual(and_nand.evaluate({'A': 0, 'B': 1}), self.binary.evaluate({'A': 0, 'B': 1}))
        self.assertEqual(and_nand.evaluate({'A': 0, 'B': 0}), self.binary.evaluate({'A': 0, 'B': 0}))

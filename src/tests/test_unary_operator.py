import unittest
from unittest.mock import MagicMock

from src.models.Nodes import UnaryOperator, Predicate, NandOperator


class TestUnaryOperator(unittest.TestCase):

    def setUp(self):
        self.child = Predicate('A')
        self.unary = UnaryOperator('~', self.child)

    def test_init(self):
        print('test_unary_init')
        self.assertEqual(self.unary.label, '~')
        self.assertEqual(self.unary.child, self.child)

    def test_str(self):
        print('test_unary_str')
        self.assertEqual(str(self.unary), '~(A)')

    def test_get_predicate(self):
        print('test_unary_get_predicate')

        # with empty list
        list = []
        self.unary.get_predicates(list)
        self.assertEqual(list, ['A'])

        # with non-empty list
        self.child.label = 'B'
        self.unary.get_predicates(list)
        self.assertEqual(list, ['A', 'B'])

    def test_evaluate(self):
        print('test_unary_evaluate')

        # child returns 1
        self.child.evaluate = MagicMock(return_value=1)
        self.assertEqual(self.unary.evaluate({}), False)

        # child returns 0
        self.child.evaluate = MagicMock(return_value=0)
        self.assertEqual(self.unary.evaluate({}), True)

    def test_nandify(self):
        print('test_unary_nandify')
        unary_nand = self.unary.nandify()
        unary_nand.right_child.evaluate = MagicMock(return_value=1)
        unary_nand.left_child.evaluate = MagicMock(return_value=1)
        self.child.evaluate = MagicMock(return_value=1)

        self.assertIsInstance(unary_nand, NandOperator)
        self.assertEqual(unary_nand.label, '%')
        self.assertEqual(unary_nand.evaluate({}), self.unary.evaluate({}))

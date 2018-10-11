import unittest
from unittest.mock import MagicMock

from src.models.Tree import Tree
from src.models.Nodes import AndOperator, NandOperator


class TestTree(unittest.TestCase):

    def setUp(self):
        self.tree = Tree('&(A,B)')

    def test_init(self):
        print('test_tree_init')
        self.assertIsInstance(self.tree.root, AndOperator)
        self.assertEqual(self.tree.unique_predicates, ['A', 'B'])

    def test_evaluate(self):
        print('test_tree_evaluate')
        self.tree.root.evaluate = MagicMock(return_value=1)
        self.assertEqual(self.tree.evaluate({}), 1)
        self.tree.root.evaluate = MagicMock(return_value=0)
        self.assertEqual(self.tree.evaluate({}), 0)

    def test_nandify(self):
        print('test_tree_nandify')
        tree_nand = self.tree.nandify()
        self.assertIsInstance(tree_nand, NandOperator)
        self.assertEqual(tree_nand.evaluate({'A': 1, 'B': 1}), self.tree.evaluate({'A': 1, 'B': 1}))
        self.assertEqual(tree_nand.evaluate({'A': 1, 'B': 0}), self.tree.evaluate({'A': 1, 'B': 0}))
        self.assertEqual(tree_nand.evaluate({'A': 0, 'B': 1}), self.tree.evaluate({'A': 0, 'B': 1}))
        self.assertEqual(tree_nand.evaluate({'A': 0, 'B': 0}), self.tree.evaluate({'A': 0, 'B': 0}))

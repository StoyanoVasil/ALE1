import unittest

from src.models.Nodes import Predicate, BinaryOperator


class TestBinaryOperator(unittest.TestCase):

    def setUp(self):
        self.l_child = Predicate('A')
        self.r_child = Predicate('B')
        self.binary = BinaryOperator('?', self.l_child, self.r_child, '?')

    def test_init(self):
        print('test_binary_init')
        self.assertEqual(self.binary.label, '?')
        self.assertEqual(self.binary.left_child, self.l_child)
        self.assertEqual(self.binary.right_child, self.r_child)

    def test_str(self):
        print('test_binary_str')
        self.assertEqual(str(self.binary), '?(A,B)')

    def test_get_predicate(self):
        print('test_binary_get_predicate')

        # with empty list
        list = []
        self.binary.get_predicates(list)
        self.assertEqual(list, ['A', 'B'])

        # with non-empty list
        self.r_child.label = 'A'
        self.l_child.label = 'B'
        self.binary.get_predicates(list)
        self.assertEqual(list, ['A', 'B', 'B', 'A'])


if __name__ == '__main__':
    unittest.main()

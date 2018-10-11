import unittest

from src.models.Nodes import Predicate


class TestPredicate(unittest.TestCase):

    def setUp(self):
        self.predicate_with_letter = Predicate('A')
        self.predicate_with_number = Predicate('1')

    def test_init(self):
        print('test_predicate_init')
        self.assertEqual(self.predicate_with_letter.label, 'A')
        self.assertEqual(self.predicate_with_number.label, '1')

    def test_str(self):
        print('test_predicate_str')
        self.assertEqual(str(self.predicate_with_letter), 'A')
        self.assertEqual(str(self.predicate_with_number), '1')

    def test_get_predicate(self):
        print('test_predicate_get_predicate')

        # with empty list
        list = []
        self.predicate_with_letter.get_predicates(list)
        self.predicate_with_number.get_predicates(list)
        self.assertEqual(list, ['A'])

        # with non-empty list
        self.predicate_with_letter.label = 'B'
        self.predicate_with_letter.get_predicates(list)
        self.predicate_with_number.get_predicates(list)
        self.assertEqual(list, ['A', 'B'])

    def test_evaluate(self):
        print('test_predicate_evaluate')

        # for predicates with 0 or 1
        self.assertEqual(self.predicate_with_number.evaluate({}), True)
        self.predicate_with_number.label = '0'
        self.assertEqual(self.predicate_with_number.evaluate({}), False)

        # for predicates with letter
        self.assertEqual(self.predicate_with_letter.evaluate({'A': 1}), True)
        self.assertEqual(self.predicate_with_letter.evaluate({'A': 0}), False)

    def test_nandify(self):
        print('test_predicate_nandify')
        letter_nand = self.predicate_with_letter.nandify()
        number_nand = self.predicate_with_number.nandify()

        self.assertIsInstance(letter_nand, Predicate)
        self.assertEqual(letter_nand.label, 'A')
        self.assertEqual(letter_nand.evaluate({'A': 1}), self.predicate_with_letter.evaluate({'A': 1}))

        self.assertIsInstance(number_nand, Predicate)
        self.assertEqual(number_nand.label, '1')
        self.assertEqual(number_nand.evaluate({}), self.predicate_with_number.evaluate({}))


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock

import src.models.utils as parse
from src.models.Errors import *


class TestParsing(unittest.TestCase):

    def test_remove_expression_whitespaces(self):
        print('test_parsing_removing_whitespaces')
        exps = ['  a  b     1  ', '', 'a   b', 'a b ', ' a b']
        ress = ['ab1', '', 'ab', 'ab', 'ab']

        for i, e in enumerate(exps):
            self.assertEqual(parse._remove_expression_whitespaces(e), ress[i])

    def test_validate_length(self):
        print('test_parsing_validate_length')
        with self.assertRaises(ParserError):
            parse._validate_length('')

    def test_validate_matching_brackets(self):
        print('test_parsing_validate_matching_brackets')
        with self.assertRaises(BracketError):
            parse._validate_matching_brackets(')')
            parse._validate_matching_brackets('(()')
            parse._validate_matching_brackets('())')
            parse._validate_matching_brackets('(')

    def test_validate_bracket_operator_ratio(self):
        print('test_parsing_validate_bracket_operator_ratio')
        with self.assertRaises(BracketError):
            parse._validate_bracket_operator_ratio('~((')
            parse._validate_bracket_operator_ratio('(~&')
            parse._validate_bracket_operator_ratio(')|')

    def test_expression_starts_with_operator(self):
        print('test_parsing_expression_starts_with_operator')
        with self.assertRaises(OperatorError):
            parse._expression_starts_with_operator('(~)')
            parse._expression_starts_with_operator(')&')
            parse._expression_starts_with_operator('()')

    def test__expression_is_single_predicate(self):
        print('test_parsing_expression_is_single_predicate')
        with self.assertRaises(PredicateError):
            parse._expression_is_single_predicate('~')
            parse._expression_is_single_predicate('(')
            parse._expression_is_single_predicate('+')
        self.assertEqual(parse._expression_is_single_predicate('AA'), False)
        self.assertEqual(parse._expression_is_single_predicate('A'), True)
        self.assertEqual(parse._expression_is_single_predicate('0'), True)
        self.assertEqual(parse._expression_is_single_predicate('1'), True)

    def test_is_proper_predicate(self):
        print('test_parsing_is_proper_predicate')
        with self.assertRaises(PredicateError):
            parse._is_proper_predicate('(')
            parse._is_proper_predicate(')')
            parse._is_proper_predicate('+')
            parse._is_proper_predicate('?')
            parse._is_proper_predicate('2')
        self.assertEqual(parse._is_proper_predicate('a'), True)
        self.assertEqual(parse._is_proper_predicate('1'), True)
        self.assertEqual(parse._is_proper_predicate('0'), True)
        self.assertEqual(parse._is_proper_predicate('A'), True)
        self.assertEqual(parse._is_proper_predicate('z'), True)

    def test_predicate_is_letter(self):
        print('test_parsing_predicate_is_letter')
        self.assertEqual(parse._predicate_is_letter('a'), True)
        self.assertEqual(parse._predicate_is_letter('A'), True)
        self.assertEqual(parse._predicate_is_letter('z'), True)
        self.assertEqual(parse._predicate_is_letter('Z'), True)
        self.assertEqual(parse._predicate_is_letter('1'), False)
        self.assertEqual(parse._predicate_is_letter('0'), False)

    def test_operators_are_followed_by_bracket(self):
        print('test_parsing_operators_are_followed_by_bracket')
        with self.assertRaises(OperatorError):
            parse._operators_are_followed_by_bracket('(~)')
            parse._operators_are_followed_by_bracket('(|')
            parse._operators_are_followed_by_bracket('&')
        parse._operators_are_followed_by_bracket('')
        parse._operators_are_followed_by_bracket('>(')

    def test_validate_unary_operator_predicate_count(self):
        print('test_parsing_validate_unary_operator_predicate_count')
        with self.assertRaises(PredicateError):
            parse._validate_unary_operator_predicate_count('~(,)')
            parse._validate_unary_operator_predicate_count('~(A,)')
            parse._validate_unary_operator_predicate_count('~(,A)')

    def test_validate_binary_operator_predicate_count(self):
        print('test_parsing_validate_binary_operator_predicate_count')
        with self.assertRaises(PredicateError):
            parse._validate_binary_operator_predicate_count('&()')
            parse._validate_binary_operator_predicate_count('~(A,)')
            parse._validate_binary_operator_predicate_count('~(,A)')

    def test_get_binary_operator_comma_index(self):
        print('test_parsing_get_binary_operator_comma_index')
        with self.assertRaises(PredicateError):
            parse._get_binary_operator_comma_index('&(,,)')
        self.assertEqual(parse._get_binary_operator_comma_index('(,)'), 1)
        self.assertEqual(parse._get_binary_operator_comma_index(',)'), -1)
        self.assertEqual(parse._get_binary_operator_comma_index('()'), -1)

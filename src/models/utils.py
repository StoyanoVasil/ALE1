from src.models.Nodes import *
from src.models.Errors import *


NODES = {
    '~': UnaryOperator,
    '>': ImplicationOperator,
    '=': BiImplicationOperator,
    '&': AndOperator,
    '%': NandOperator,
    '|': OrOperator
}


def parse_expression(expression):
    exp = _remove_expression_whitespaces(expression)
    _validate_expression(exp)
    return _parse_expression(exp)

def _remove_expression_whitespaces(expression):
    exp = ''.join(expression.split(' '))
    return exp

def _validate_expression(expression):
    _validate_length(expression)
    _validate_brackets(expression)
    _validate_operators(expression)
    _validate_predicate(expression)

def _validate_length(expression):
    if len(expression) < 1:
        raise ParserError('Please enter an expression')

def _validate_brackets(expression):
    _validate_matching_brackets(expression)
    _validate_bracket_operator_ratio(expression)

def _validate_matching_brackets(expression):
    bracket_count = 0
    for char in expression:
        if char == '(': bracket_count += 1
        if char == ')': bracket_count -= 1
        if bracket_count < 0: raise BracketError('Check your closing brackets')
    if bracket_count != 0: raise BracketError('Check your opening brackets')

def _validate_bracket_operator_ratio(expression):
    bracket_count = 0
    operator_count = 0
    for char in expression:
        if char in NODES: operator_count += 1
        if char == '(': bracket_count += 1
    if operator_count != bracket_count:
        raise BracketError('Check your brackets/operators')

def _validate_operators(expression):
    if not(_expression_is_single_predicate(expression)):
        _expression_starts_with_operator(expression)
    _operators_are_followed_by_bracket(expression)

def _expression_starts_with_operator(expression):
    if not(expression[0]) in NODES:
        raise OperatorError('Expressions must start with an operator')

def _expression_is_single_predicate(expression):
    if len(expression) == 1:
        if _is_proper_predicate(expression[0]): return True
        else: raise PredicateError('Not a proper predicate')

def _is_proper_predicate(char):
    print(char)
    if _predicate_is_capital_letter(char) or str(char) in ['0', '1']:
        return True
    raise PredicateError('Predicates must be a letter, 0 or 1')

def _predicate_is_capital_letter(char):
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if char.capitalize() in letters: return True
    return False

def _operators_are_followed_by_bracket(expression):
    try:
        for i, char in enumerate(expression):
            if char in NODES and expression[i + 1] != '(':
                raise OperatorError('An opening bracket is expected after an operator')
    except IndexError:
        raise OperatorError('Cannot end expression with an operator')

def _validate_predicate(expression):
    if not(_validate_predicate_length(expression)):
        if expression[0] == '~':
            _validate_unary_operator_predicate_count(expression)
        else:
            _validate_binary_operator_predicate_count(expression)

def _validate_predicate_length(expression):
    if not(expression[0] in NODES):
        l = len(expression)
        if l > 1: raise PredicateError('Predicates must consist of a single character')
        if l < 1: raise PredicateError('Missing predicate')
        return True

def _validate_unary_operator_predicate_count(expression):
    index = _get_binary_operator_comma_index(expression)
    if index != -1:
        raise PredicateError('Negation operator takes only one predicate')
    _validate_predicate(expression[2:-1])

def _validate_binary_operator_predicate_count(expression):
    index = _get_binary_operator_comma_index(expression)
    if index == -1:
        raise PredicateError('Binary operators take two predicates')
    if len(expression[2:index]) < 1 or len(expression[index+1:-1]) < 1:
        raise PredicateError('Binary operator is missing a predicate')
    _validate_predicate(expression[2:index])
    _validate_predicate(expression[index+1:-1])

def _parse_expression(expression):
    try:
        operator = expression[0]
        node = NODES[operator]
        if operator == '~':
            return node(operator, _parse_expression(expression[2:-1]))
        else:
            index = _get_binary_operator_comma_index(expression)
            return node(operator,
                        _parse_expression(expression[2:index]),
                        _parse_expression(expression[index+1:-1]))
    except KeyError:
        return Predicate(expression)

def _get_binary_operator_comma_index(expression):
    index = -1
    coma_count = 0
    bracket_count = 0
    for i, char in enumerate(expression):
        if char == '(': bracket_count += 1
        if char == ')': bracket_count -= 1
        if bracket_count == 1 and char == ',':
            index = i
            coma_count += 1
    if coma_count > 1: raise PredicateError('Operators take not more than two predicates, check your comas')
    return index

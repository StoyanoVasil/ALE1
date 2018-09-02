from src.models.Nodes import *

class Tree:
    NODES = {
        '~': UnaryOperator,
        '>': BinaryOperator,
        '=': BinaryOperator,
        '&': BinaryOperator,
        '|': BinaryOperator
    }

    def __init__(self, expression):
        self.expression = self._remove_expression_whitespaces(expression)
        self.root = self._parse_expression(self.expression)

    def get_expression(self):
        return self.root

    def _remove_expression_whitespaces(self, expression):
        return ''.join(expression.split(' '))

    def _parse_expression(self, expression):
        try:
            operator = expression[0]
            node = self.NODES[operator]
            if operator == '~':
                return node(operator, self._parse_expression(expression[2:-1]))
            else:
                index = self._get_binary_operator_comma_index(expression)
                return node(operator,
                            self._parse_expression(expression[2:index]),
                            self._parse_expression(expression[index+1:-1]))
        except KeyError:
            return Predicate(expression)
        except TypeError:
            raise OperatorException('Binary operators take 2 predicates and unary operators take 1')

    def _get_binary_operator_comma_index(self, expression):
        bracket_count = 0
        for i, char in enumerate(expression):
            if char == '(': bracket_count += 1
            if char == ')': bracket_count -= 1
            if bracket_count == 1 and char == ',': return i
        raise BinaryOperatorException('Either check your opening/closing brackets or a missing comma')


def run():
    t = Tree('   =( ~ (  A   ) , >  (~( A ),     B )  )')
    print(t.get_expression())

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)

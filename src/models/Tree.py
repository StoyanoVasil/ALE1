from src.models.Nodes import *
from graphviz import Digraph

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

    # just to test for now
    def get_expression(self):
        print(self.root)

    def get_dot(self):
        dot = Digraph(comment='Parse tree')
        self.root.insert_in_dot(dot)
        dot.render(f'../static/images/{str(id(self))}.gv', view=False)

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
            raise OperatorException('Invalid expression')

    def _get_binary_operator_comma_index(self, expression):
        bracket_count = 0
        for i, char in enumerate(expression):
            if char == '(': bracket_count += 1
            if char == ')': bracket_count -= 1
            if bracket_count == 1 and char == ',': return i
        raise BinaryOperatorException('Invalid expression')


# just for testing
def run():
    t = Tree('   =( >  (~( z ),     x ), ~ (  y   )   )')
    t.get_expression()
    t.get_dot()

if __name__ == '__main__':
    try:
        run()
    except Exception as e:
        print(e)

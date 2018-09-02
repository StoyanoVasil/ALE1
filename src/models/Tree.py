from src.models.Nodes import *
from graphviz import Digraph
import pydot


class Tree:
    NODES = {
        '~': UnaryOperator,
        '>': BinaryOperator,
        '=': BinaryOperator,
        '&': BinaryOperator,
        '|': BinaryOperator
    }

    def __init__(self, expression):
        self.id = str(id(self))
        self.expression = self._remove_expression_whitespaces(expression)
        self.root = self._parse_expression(self.expression)

    def get_infix_expression(self):
        print(self.root)

    def get_graph_image_name(self):
        self._create_graph_image()
        return f'{self.id}.png'

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

    def _create_graph_image(self):
        self._get_dot()
        self._convert_dot_to_image()

    def _get_dot(self):
        dot = Digraph(comment='Parse tree')
        self.root.insert_in_dot(dot)
        dot.save(f'src/static/images/{self.id}.gv')

    def _convert_dot_to_image(self):
        (graph, ) = pydot.graph_from_dot_file(f'src/static/images/{self.id}.gv')
        graph.write_png(f'src/static/images/{self.id}.png')

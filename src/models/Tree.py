from src.models.utils import parse_expression
from graphviz import Digraph
import pydot


class Tree:
    def __init__(self, expression):
        self.id = str(id(self))
        self.root = parse_expression(expression)

    def get_infix_expression(self):
        return self.root

    def get_graph_image_name(self):
        self._create_graph_image()
        return f'{self.id}.png'


    def _create_graph_image(self):
        self._get_dot()
        self._convert_dot_to_image()

    def _get_dot(self):
        dot = Digraph()
        self.root.insert_in_dot(dot)
        dot.save(f'src/static/images/{self.id}.gv')

    def _convert_dot_to_image(self):
        (graph, ) = pydot.graph_from_dot_file(f'src/static/images/{self.id}.gv')
        graph.write_png(f'src/static/images/{self.id}.png')

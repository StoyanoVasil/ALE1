from src.models.utils import parse_expression
from graphviz import Digraph
import pydot


class Tree:
    def __init__(self, expression):
        self.id = str(id(self))
        self.root = parse_expression(expression)
        self.__set_unique_predicates()

    def get_infix_expression(self):
        return str(self.root)

    def get_graph_image_name(self):
        self.__create_graph_image()
        return f'{self.id}.png'

    def __create_graph_image(self):
        self.__get_dot()
        self.__convert_dot_to_image()

    def __get_dot(self):
        dot = Digraph()
        self.root.insert_in_dot(dot)
        dot.save(f'src/static/images/{self.id}.gv')

    def __convert_dot_to_image(self):
        (graph, ) = pydot.graph_from_dot_file(f'src/static/images/{self.id}.gv')
        graph.write_png(f'src/static/images/{self.id}.png')

    def __set_unique_predicates(self):
        predicates = []
        self.root.get_predicates(predicates)
        self.unique_predicates =  sorted({p for p in predicates})

    def evaluate(self, dict):
        return self.root.evaluate(dict)

    def nandify(self):
        return self.root.nandify()

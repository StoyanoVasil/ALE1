import abc
from src.models.Errors import *


class Node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert_in_dot(self, dot):
        pass


class Predicate(Node):
    def __init__(self, label):
        super().__init__()
        self.id = str(id(self))
        if len(label) == 1:
            self.label = label
        else:
            raise NotAProperPredicateException("Invalid expression")

    def __repr__(self):
        return self.label

    def insert_in_dot(self, dot):
        dot.node(self.id, self.label)


class UnaryOperator(Node):
    def __init__(self, label, child):
        super().__init__()
        self.id = str(id(self))
        self.label = label
        self.child = child

    def __repr__(self):
        return f'¬({self.child})'

    def insert_in_dot(self, dot):
        self.child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.child.id)


class BinaryOperator(Node):
    OPERATORS = {
        '>': '⇒',
        '=': '⇔',
        '&': '⋀',
        '|': '⋁'
    }

    def __init__(self, label, left_child, right_child):
        super().__init__()
        self.id = str(id(self))
        self.label = label
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        return f'({self.left_child}{self.OPERATORS[self.label]}{self.right_child})'

    def insert_in_dot(self, dot):
        self.left_child.insert_in_dot(dot)
        self.right_child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.left_child.id)
        dot.edge(self.id, self.right_child.id)

from src.models.Errors import *


class Node:
    def __init__(self):
        pass

    def __repr__(self):
        raise NotImplementedError


class Predicate(Node):
    def __init__(self, label):
        super().__init__()
        if len(label) == 1:
            self.label = label
        else:
            raise NotAProperPredicateException("Invalid expression")

    def __repr__(self):
        return self.label

    def insert_in_dot(self, dot):
        dot.node(str(id(self)), self.label)


class UnaryOperator(Node):
    def __init__(self, label, child):
        super().__init__()
        self.label = label
        self.child = child

    def __repr__(self):
        return f'¬({self.child})'

    def insert_in_dot(self, dot):
        self.child.insert_in_dot(dot)
        dot.node(str(id(self)), self.label)
        dot.edge(str(id(self)), str(id(self.child)))


class BinaryOperator(Node):
    OPERATORS = {
        '>': '⇒',
        '=': '⇔',
        '&': '⋀',
        '|': '⋁'
    }

    def __init__(self, label, left_child, right_child):
        super().__init__()
        self.label = label
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        return f'({self.left_child}{self.OPERATORS[self.label]}{self.right_child})'

    def insert_in_dot(self, dot):
        self.left_child.insert_in_dot(dot)
        self.right_child.insert_in_dot(dot)
        dot.node(str(id(self)), self.label)
        dot.edge(str(id(self)), str(id(self.left_child)))
        dot.edge(str(id(self)), str(id(self.right_child)))

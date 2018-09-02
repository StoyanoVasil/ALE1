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
            raise NotAProperPredicateException("One of your predicates is either missing or more than 1 letter")

    def __repr__(self):
        return self.label


class UnaryOperator(Node):
    def __init__(self, label, child):
        super().__init__()
        self.label = label
        self.child = child

    def __repr__(self):
        return f'{self.label}({self.child})'


class BinaryOperator(Node):
    def __init__(self, label, left_child, right_child):
        super().__init__()
        self.label = label
        self.left_child = left_child
        self.right_child = right_child

    def __repr__(self):
        return f'{self.label}({self.left_child},{self.right_child})'

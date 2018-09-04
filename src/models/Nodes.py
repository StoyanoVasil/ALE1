import abc


class Node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert_in_dot(self, dot):
        pass
    #
    # @abc.abstractmethod
    # def get_value(self):
    #     pass


class Predicate(Node):
    def __init__(self, label):
        self.id = str(id(self))
        self.label = label

    def __repr__(self):
        return self.label

    def insert_in_dot(self, dot):
        dot.node(self.id, self.label)


class UnaryOperator(Node):
    def __init__(self, label, child):
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
    def __init__(self, label, left_child, right_child, infix):
        self.id = str(id(self))
        self.label = label
        self.left_child = left_child
        self.right_child = right_child
        self.infix = infix

    def __repr__(self):
        return f'({self.left_child}{self.infix}{self.right_child})'

    def insert_in_dot(self, dot):
        self.left_child.insert_in_dot(dot)
        self.right_child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.left_child.id)
        dot.edge(self.id, self.right_child.id)


class AndOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '&')


class OrOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '|')


class ImplicationOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⇒')


class BiImplicationOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⇔')

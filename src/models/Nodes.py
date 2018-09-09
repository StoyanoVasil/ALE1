import abc


class Node(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def insert_in_dot(self, dot):
        pass

    @abc.abstractmethod
    def get_predicates(self, list):
        pass

    @abc.abstractmethod
    def evaluate(self, dict):
        pass


class Predicate(Node):
    def __init__(self, label):
        self.id = str(id(self))
        self.label = label

    def __str__(self):
        return self.label

    def insert_in_dot(self, dot):
        dot.node(self.id, self.label)

    def get_predicates(self, list):
        if self.label not in ['0', '1']: list.append(self.label)

    def evaluate(self, dict):
        if self.label in dict: return dict[self.label]
        return int(self.label)

    def _true_of_false(self, num):
        return True if int(num) == 1 else False


class UnaryOperator(Node):
    def __init__(self, label, child):
        self.id = str(id(self))
        self.label = label
        self.child = child

    def __str__(self):
        return f'¬({self.child})'

    def insert_in_dot(self, dot):
        self.child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.child.id)

    def get_predicates(self, list):
        self.child.get_predicates(list)

    def evaluate(self, dict):
        return 0 if self.child.evaluate(dict) == 1 else 1


class BinaryOperator(Node):
    def __init__(self, label, left_child, right_child, infix):
        self.id = str(id(self))
        self.label = label
        self.left_child = left_child
        self.right_child = right_child
        self.infix = infix

    def __str__(self):
        return f'({self.left_child}{self.infix}{self.right_child})'

    def insert_in_dot(self, dot):
        self.left_child.insert_in_dot(dot)
        self.right_child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.left_child.id)
        dot.edge(self.id, self.right_child.id)

    def get_predicates(self, list):
        self.right_child.get_predicates(list)
        self.left_child.get_predicates(list)

    def evaluate(self, dict):
        raise NotImplementedError


class AndOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⋀')

    def evaluate(self, dict):
        return self.right_child.evaluate(dict) and self.left_child.evaluate(dict)


class OrOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⋁')

    def evaluate(self, dict):
        return self.right_child.evaluate(dict) or self.left_child.evaluate(dict)


class ImplicationOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⇒')

    def evaluate(self, dict):
        return not(self.right_child.evaluate(dict)) or self.left_child.evaluate(dict)


class BiImplicationOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⇔')

    def evaluate(self, dict):
        return self.right_child.evaluate(dict) == self.left_child.evaluate(dict)

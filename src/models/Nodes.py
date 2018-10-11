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

    @abc.abstractmethod
    def nandify(self):
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

    def nandify(self):
        return Predicate(self.label)


class UnaryOperator(Node):
    def __init__(self, label, child):
        self.id = str(id(self))
        self.label = label
        self.child = child

    def __str__(self):
        # return f'¬({self.child})'
        return f'{self.label}({self.child})'

    def insert_in_dot(self, dot):
        self.child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.child.id)

    def get_predicates(self, list):
        self.child.get_predicates(list)

    def evaluate(self, dict):
        return 0 if self.child.evaluate(dict) == 1 else 1

    def nandify(self):
        child = self.child.nandify()
        return NandOperator('%', child, child)


class BinaryOperator(Node):
    def __init__(self, label, left_child, right_child, infix):
        self.id = str(id(self))
        self.label = label
        self.left_child = left_child
        self.right_child = right_child
        self.infix = infix

    def __str__(self):
        # return f'({self.left_child}{self.infix}{self.right_child})'
        return f'{self.label}({self.left_child},{self.right_child})'

    def insert_in_dot(self, dot):
        self.left_child.insert_in_dot(dot)
        self.right_child.insert_in_dot(dot)
        dot.node(self.id, self.label)
        dot.edge(self.id, self.left_child.id)
        dot.edge(self.id, self.right_child.id)

    def get_predicates(self, list):
        self.left_child.get_predicates(list)
        self.right_child.get_predicates(list)

    def evaluate(self, dict):
        raise NotImplementedError

    def nandify(self):
        raise NotImplementedError


class AndOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⋀')

    def evaluate(self, dict):
        return 1 if self.left_child.evaluate(dict) and self.right_child.evaluate(dict) else 0

    def nandify(self):
        left_child_nand = self.left_child.nandify()
        right_child_nand = self.right_child.nandify()
        return NandOperator('%',
                            NandOperator('%', left_child_nand, right_child_nand),
                            NandOperator('%', left_child_nand, right_child_nand))


class OrOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⋁')

    def evaluate(self, dict):
        return 1 if self.left_child.evaluate(dict) or self.right_child.evaluate(dict) else 0

    def nandify(self):
        left_child_nand = self.left_child.nandify()
        right_child_nand = self.right_child.nandify()
        return NandOperator('%',
                            NandOperator('%', left_child_nand, left_child_nand),
                            NandOperator('%', right_child_nand, right_child_nand))


class ImplicationOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⇒')

    def evaluate(self, dict):
        return 1 if not(self.left_child.evaluate(dict)) or self.right_child.evaluate(dict) else 0

    def nandify(self):
        left_child_nand = self.left_child.nandify()
        right_child_nand = self.right_child.nandify()
        return NandOperator('%', left_child_nand, NandOperator('%', right_child_nand, right_child_nand))


class BiImplicationOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '⇔')

    def evaluate(self, dict):
        return 1 if self.left_child.evaluate(dict) == self.right_child.evaluate(dict) else 0

    def nandify(self):
        left_child_nand = self.left_child.nandify()
        right_child_nand = self.right_child.nandify()
        return OrOperator('|',
                          NandOperator('%',
                                       NandOperator('%',
                                                    NandOperator('%', left_child_nand, left_child_nand),
                                                    NandOperator('%', right_child_nand, right_child_nand)),
                                       NandOperator('%',
                                                    NandOperator('%', left_child_nand, left_child_nand),
                                                    NandOperator('%', right_child_nand, right_child_nand))),
                          NandOperator('%',
                                       NandOperator('%', left_child_nand, right_child_nand),
                                       NandOperator('%', left_child_nand, right_child_nand))).nandify()


class NandOperator(BinaryOperator):
    def __init__(self, label, left_child, right_child):
        super().__init__(label, left_child, right_child, '%')

    def evaluate(self, dict):
        return 1 if not(self.left_child.evaluate(dict) and self.right_child.evaluate(dict)) else 0

    def nandify(self):
        # return self
        return NandOperator(self.label, self.left_child, self.right_child)

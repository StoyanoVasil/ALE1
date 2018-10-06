
class Simplifier:
    def __init__(self, predicates):
        self.predicates = predicates
        self.minterm = []
        self.implicants = {}
        self.step = {}
        self.reduced_implicants = []
        self.final_implicants = []
        self.normalization = []

    def add_implicant(self, i, implicant):
        mt = ''.join([str(s) for s in implicant])
        ones = self.__get_number_of_ones(mt)
        if ones not in self.implicants:
            self.implicants[ones] = [[i, mt[:], False]]
        else:
            self.implicants[ones].append([i, mt[:], False])
        self.minterm.append(i)

    def __get_number_of_ones(self, imp):
        ones = 0
        for c in imp:
            if c == '1': ones += 1
        return ones

    def simplify(self):
        self.__reduce_implicants()
        self.__populate_final_implicants()


    def __reduce_implicants(self):
        self.__step()
        while self.__not_done():
            self.implicants = self.step.copy()
            self.step = {}
            self.__step()

    def __populate_final_implicants(self):
        self.__add_essential_prime_implicants()
        self.__normalize()

    def __not_done(self):
        not_done = False
        for k, v in self.implicants.items():
            for arr in v:
                if arr[2]: not_done = True
        return not_done

    def __step(self):
        groups = sorted([k for k in self.implicants.keys()])
        for i, k in enumerate(groups[:-1]):
            self.__match_group(self.implicants[k], self.implicants[groups[i + 1]])
        self.__add_reduced_implicants()

    def __match_group(self, a, b):
        for arr_a in a:
            for arr_b in b:
                self.__match_implicants(arr_a, arr_b)

    def __match_implicants(self, a, b):
        index = self.__different_char_index(a[1], b[1])
        if index != -1:
            self.__add_to_step(index, a, b)
            self.__check_implicants(a, b)

    def __different_char_index(self, a, b):
        diff = 0
        index = -1
        for i in range(len(a)):
            if a[i] != b[i]:
                diff += 1
                index = i
        if diff == 1: return index
        return -1

    def __add_to_step(self, i, a, b):
        arr = [f'{a[0]}-{b[0]}', f'{a[1][:i]}*{a[1][i+1:]}', False]
        ones = self.__get_number_of_ones(arr[1])
        if ones not in self.step: self.step[ones] = [arr]
        else: self.step[ones].append(arr)

    def __check_implicants(self, a, b):
        if not(a[2]): a[2] = True
        if not(b[2]): b[2] = True

    def __add_reduced_implicants(self):
        for k, v in self.implicants.items():
            for arr in v:
                if not(arr[2]): self.__add_if_not_inside((arr[0], arr[1]))

    def __add_if_not_inside(self, tuple):
        for x, y in self.reduced_implicants:
            if y == tuple[1]: return
        self.reduced_implicants.append(tuple)

    def __add_essential_prime_implicants(self):
        self.__add_unique_minterm_implicants()
        self.__add_rest_of_essential_implicants()

    def __add_unique_minterm_implicants(self):
        to_remove = []
        for row in self.reduced_implicants:
            if self.__check_essential_implicants(row):
                to_remove.append(row)
                self.__add_implicant(row)
        for r in to_remove:
            self.reduced_implicants.remove(r)

    def __add_rest_of_essential_implicants(self):
        index = 0
        while index != -1:
            index = -1
            max_diff = 0
            for i, row in enumerate(self.reduced_implicants):
                diff = self.__get_diff(row)
                if diff > max_diff:
                    max_diff = diff
                    index = i
            if index != -1:
                implicant = self.reduced_implicants[index]
                self.__add_implicant(implicant)
                self.reduced_implicants.remove(implicant)

    def __get_diff(self, row):
        diff = 0
        for minterm in row[0].split('-'):
            is_contained = False
            for implicant in self.final_implicants:
                if self.__minterm_in_implicant(minterm, implicant[0]): is_contained = True
            if not is_contained: diff += 1
        return diff

    def __check_essential_implicants(self, row):
        for minterm in row[0].split('-'):
            add_check = True
            for implicant in self.reduced_implicants:
                if row != implicant:
                    if self.__minterm_in_implicant(minterm, implicant[0]): add_check = False
            if add_check: return True
        return False

    def __minterm_in_implicant(self, minterm, implicant):
        for i in implicant.split('-'):
            if i == minterm: return True
        return False

    def __add_implicant(self, tuple):
        self.final_implicants.append(tuple)
        self.__add_to_normalization(tuple)

    def __add_to_normalization(self, tuple):
        predicates = []
        for i, t in enumerate(tuple[1]):
            if t == '1': predicates.append(f'{self.predicates[i]}')
            elif t == '0': predicates.append(f'¬{self.predicates[i]}')
        norm = ' ⋀ '.join(predicates)
        self.normalization.append(f'({norm})')

    def __normalize(self):
        self.normalization = ' ⋁ '.join(self.normalization)


if __name__ == '__main__':
    arr = {
        '0': [0, 0, 0, 0],
        '4': [0, 1, 0, 0],
        '5': [0, 1, 0, 1],
        '7': [0, 1, 1, 1],
        '8': [1, 0 ,0 ,0],
        '11': [1, 0, 1, 1],
        '12': [1, 1, 0, 0],
        '15': [1, 1, 1, 1]
    }
    s = Simplifier(['A', 'B', 'C', 'D'])
    for k, v in arr.items():
        s.add_implicant(k, v)
    s.simplify()
    print(s.reduced_implicants)
    print(s.final_implicants)

import numpy as np


class Simplifier:
    def __init__(self):
        self.midterm_indexes = []
        self.midterms = {}
        self.step = {}
        self.reduced_midterms = []
        self.final_midterms = []

    def add_implicant(self, i, midterm):
        mt = ''.join([str(s) for s in midterm])
        ones = self.__get_number_of_ones(mt)
        if ones not in self.midterms:
            self.midterms[ones] = [[i, mt[:], False]]
        else:
            self.midterms[ones].append([i, mt[:], False])
        self.midterm_indexes.append(i)

    def __get_number_of_ones(self, imp):
        ones = 0
        for c in imp:
            if c == '1': ones += 1
        return ones

    def simplify(self):
        self.__reduce_midterms()
        print(self.reduced_midterms, self.midterm_indexes)
        self.__reduce_reduced_midterms()
        #self.__create_table()

    def __reduce_midterms(self):
        self.__step()
        while self.__not_done():
            self.midterms = self.step.copy()
            self.step = {}
            self.__step()

    def __reduce_reduced_midterms(self):
        reduce_table = self.__create_reduce_table()
        print(reduce_table)

    def __not_done(self):
        not_done = False
        for k, v in self.midterms.items():
            for arr in v:
                if arr[2]: not_done = True
        return not_done

    def __step(self):
        groups = sorted([k for k in self.midterms.keys()])
        for i, k in enumerate(groups[:-1]):
            self.__match_group(self.midterms[k], self.midterms[groups[i+1]])
        self.__add_final_midterms()

    def __match_group(self, a, b):
        for arr_a in a:
            for arr_b in b:
                self.__match_midterms(arr_a, arr_b)

    def __match_midterms(self, a, b):
        index = self.__different_char_index(a[1], b[1])
        if index != -1:
            self.__add_to_step(index, a, b)
            self.__check_midterms(a, b)


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
        arr = [f'{a[0]}-{b[0]}', f'{a[1][:i]}_{a[1][i+1:]}', False]
        ones = self.__get_number_of_ones(arr[1])
        if ones not in self.step: self.step[ones] = [arr]
        else: self.step[ones].append(arr)

    def __check_midterms(self, a, b):
        if not(a[2]): a[2] = True
        if not(b[2]): b[2] = True

    def __add_final_midterms(self):
        for k, v in self.midterms.items():
            for arr in v:
                if not(arr[2]): self.__add_if_not_inside((arr[0], arr[1]))

    def __add_if_not_inside(self, tuple):
        for x, y in self.reduced_midterms:
            if y == tuple[1]: return
        self.reduced_midterms.append(tuple)

    def __create_reduce_table(self):
        reduce_table = []
        for tuple in self.reduced_midterms:
            temp = [0] * len(self.midterm_indexes)
            for c in ''.join(tuple[0].split('-')):
                temp[self.midterm_indexes.index(c)] = 1
            reduce_table.append(temp)
        return reduce_table

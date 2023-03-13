import json
import os.path
import time
from itertools import product

import numpy
import sympy
from multiset import FrozenMultiset

start_time = time.time()


def shift(unshifted):
    Shifted_list = []
    for unshifted_element in unshifted:
        Shifted_list.append((unshifted_element - unshifted[0]) % 1)
    return Shifted_list


def shifted(unshifted):
    Shifted_list = []
    for k in range(1, len(unshifted)):
        Shifted_list.append((unshifted[k] - unshifted[0] + sympy.Rational(1, 2)) % 1)
    return Shifted_list


def cyclotomic(mylist, k, t):
    new_list = []
    for element in mylist:
        new_list.append(element + sympy.Rational(k, t))
    return new_list


def create(old_solutions):
    new_solution = []
    t = len(old_solutions)
    for k in range(0, t):
        new_solution.extend(cyclotomic(old_solutions[k], k, t))
    return new_solution


def valid_partition(k, p):

    def possible_degree_list(c):
        for s in range(0, p):
            if s not in c:
                return False
        return True

    p_fold_product_of_Z_p = list(product(range(p), repeat=k))
    possible_c_values = list(filter(possible_degree_list, p_fold_product_of_Z_p))
    dedupped_possible_c_values = set([FrozenMultiset(c) for c in possible_c_values])

    return dedupped_possible_c_values


def cross_sum(c):
    sums = []
    for i in range(len(c)):
        for j in range(len(c)):
            sums.append((c[j] - c[i]) % 1)
    return sorted(sums)


def solve(n, all_old_dict, shifted_old_dict):
    all_solutions = all_old_dict
    shifted_solutions = shifted_old_dict

    for k in range(max(all_solutions.keys()) + 1, n + 1):
        k_TempSolutions = []
        for p in sympy.primerange(3, k + 1):
            for c in valid_partition(k, p):
                partitions = [shifted_solutions[list(c).count(d)] for d in range(p)]
                for old_solutions in list(product(*partitions)):
                    k_TempSolutions.append(shift(list(create(old_solutions))))
        p = 2
        k_2_TempSolutions = []
        for c in valid_partition(k, p):
            if list(c).count(0) in range(1, p-1):
                partitions = [shifted_solutions[list(c).count(d)] for d in range(p)]
                for old_solutions in list(product(*partitions)):
                    k_2_TempSolutions.append(shift(list(create(old_solutions))))

        k_TempSolutions = k_TempSolutions + k_2_TempSolutions

        def Primitive(c):
            for l in range(2, k):
                for d in all_solutions[l]:
                    if set(d) <= set(c):
                        return False
            return True

        Primitive_k_TempSolutions = list(filter(Primitive, k_TempSolutions))

        UniqueSolutions = []
        for c in Primitive_k_TempSolutions:
            if c not in UniqueSolutions:
                UniqueSolutions.append(c)

        final_temp_solutions = []

        if len(UniqueSolutions) > 0:
            final_temp_solutions.append(UniqueSolutions[0])

        CrossSumSolutions = []

        for c in final_temp_solutions:
            CrossSumSolutions.append(cross_sum(c))

        for c in UniqueSolutions:
            if not cross_sum(c) in CrossSumSolutions:
                final_temp_solutions.append(c)
                CrossSumSolutions.append(cross_sum(c))

        all_solutions[k] = final_temp_solutions

        k_ShiftedSolutions = [shifted(c) for c in all_solutions[k]]

        shifted_solutions[k - 1] = k_ShiftedSolutions

    return all_solutions, shifted_solutions


def serialize_solutions_dict(json_file, dict):
    stringyfied_dict = {degree: [[str(number) for number in solution]
                                 for solution in solutions] for (degree, solutions) in dict.items()}
    json_object = json.dumps(stringyfied_dict, indent=4)
    json_file.write(json_object)


def deserialize_solutions_dict(json_file):
    old_dict = json.loads(json_file.read())
    return {int(degree): [[sympy.Rational(number) for number in solution] for solution in solutions] for (degree, solutions) in old_dict.items()}


if __name__ == "__main__":
    if os.path.isfile("all_solution_dictionary.json") and os.path.isfile("shifted_solution_dictionary.json"):
        all_json_file = open("all_solution_dictionary.json", "r")
        shifted_json_file = open("shifted_solution_dictionary.json", "r")

        all_old_dict = deserialize_solutions_dict(all_json_file)
        shifted_old_dict = deserialize_solutions_dict(shifted_json_file)

        all_json_file.close()
        shifted_json_file.close()
    else:
        all_old_dict = {2: [[sympy.Rational(0, 1), sympy.Rational(1, 2)]]}
        shifted_old_dict = {1: [[sympy.Rational(0, 1)]]}

    all_json_file = open("all_solution_dictionary.json", "w+")
    shifted_json_file = open("shifted_solution_dictionary.json", "w+")

    all_solutions, shifted_solutions = solve(
        int(input('Enter a size: ')), all_old_dict, shifted_old_dict)

    serialize_solutions_dict(all_json_file, all_solutions)
    serialize_solutions_dict(shifted_json_file, shifted_solutions)

    all_json_file.close()
    shifted_json_file.close()

    print(f'--- {time.time() - start_time} seconds ---')

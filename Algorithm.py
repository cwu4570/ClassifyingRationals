from itertools import product

import os.path
import json
import numpy
import sympy
from multiset import FrozenMultiset

import time

start_time = time.time()

AllSolutions = {2: [[sympy.Rational(0,1), sympy.Rational(1,2)]]}
ShiftedSolutions = {1: [[sympy.Rational(0,1)]]}

# # to initialize your dict
# if os.path.isfile('All_Solutions.txt'):
#     with open('All_Solutions.txt', 'r') as f:
#         AllSolutions = json.load(f)



def Shift(unshifted):
    Shifted_list = []
    for k in range(0, len(unshifted)):
        Shifted_list.append((unshifted[k] - unshifted[0]) % 1)
    return Shifted_list

def Shifted(unshifted):
    Shifted_list = []
    for k in range(1, len(unshifted)):
        Shifted_list.append((unshifted[k] - unshifted[0] + sympy.Rational(1,2))% 1)
    return Shifted_list

def Cyclotomic(mylist, k , t):
    new_list = []
    for s in range(len(mylist)):
        new_list.append(mylist[s] + sympy.Rational(k,t))
    return new_list

def Create(old_solutions):
    new_solution = []
    t = len(old_solutions)
    for k in range(0, t):
        new_solution.extend(Cyclotomic(old_solutions[k],k, t))
    return new_solution



def Valid_Partition(k,p):

    def possible_degree_list(c):
        for s in range(0,p):
            if s not in c:
                return False
        return True
    
    p_fold_product_of_Z_p = list(product(range(p), repeat=k))
    possible_c_values = list(filter(possible_degree_list, p_fold_product_of_Z_p))
    dedupped_possible_c_values = set([FrozenMultiset(c) for c in possible_c_values])

    return dedupped_possible_c_values


def CrossSum(c):
    sums = []
    for i in range(len(c)):
        for j in range(len(c)):
            sums.append((c[j] - c[i]) % 1)
    return sorted(sums)


def solve(n):

    for k in range(3, n + 1):
        k_TempSolutions = []
        for p in sympy.primerange(3,k + 1):
            for c in Valid_Partition(k,p):
                partitions = [ShiftedSolutions[list(c).count(d)] for d in range(p)]
                for old_solutions in list(product(*partitions)):
                    k_TempSolutions.append(Shift(list(Create(old_solutions))))
        p = 2
        k_2_TempSolutions = []
        for c in Valid_Partition(k,p):
            if list(c).count(0) in range(1,p-1):
                partitions = [ShiftedSolutions[list(c).count(d)] for d in range(p)]
                for old_solutions in list(product(*partitions)):
                    k_2_TempSolutions.append(Shift(list(Create(old_solutions))))

        k_TempSolutions = k_TempSolutions + k_2_TempSolutions

        def Primitive(c):
            for l in range(2,k):
                for d in AllSolutions[l]:
                    if set(d) <= set(c):
                        return False
            return True

        Primitive_k_TempSolutions = list(filter(Primitive, k_TempSolutions))

        # print(Primitive_k_TempSolutions)

        # if len(Primitive_k_TempSolutions) > 0:
        #     FinalTempSolutions = [Primitive_k_TempSolutions[0]]

        UniqueSolutions = []
        [UniqueSolutions.append(c) for c in Primitive_k_TempSolutions if c not in UniqueSolutions]


        FinalTempSolutions = []

        if len(UniqueSolutions) > 0:
            FinalTempSolutions.append(UniqueSolutions[0])
        
        CrossSumSolutions = []

        for c in FinalTempSolutions:
            CrossSumSolutions.append(CrossSum(c))

        for c in UniqueSolutions:
                if CrossSum(c) in CrossSumSolutions:
                    continue
                else:
                    FinalTempSolutions.append(c)
                    CrossSumSolutions.append(CrossSum(c))


        AllSolutions[k] = FinalTempSolutions

        k_ShiftedSolutions = []

        for c in AllSolutions[k]:
            k_ShiftedSolutions.append(Shifted(c))

        ShiftedSolutions[k - 1] = k_ShiftedSolutions
        
    # with open('All_Solutions.txt', 'w') as f:
    #     json.dump(AllSolutions, f)
    #     f.write(AllSolutions)
    #     f.close()
    
    return AllSolutions


if __name__ == "__main__":
    output_dict = solve(int(input('Enter a size: ')))
    stringyfied_dict =  {degree:[[str(number) for number in solution] for solution in solutions] for (degree, solutions) in output_dict.items()}
    json_object = json.dumps(stringyfied_dict, indent=4)

    with open("solution_dictionary.json", "w") as outfile:
        outfile.write(json_object)

    print(f'--- {time.time() - start_time} seconds ---')
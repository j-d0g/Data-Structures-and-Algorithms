import sys
import numpy as np
import time

from knapsack import knapsack

class dp(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)

    # hard1.200.11
    # value: 126968
    # weight: 101268/101268
    def DP(self, solution):
        start_time = time.time()
        # Renaming things to keep track of them wrt. names used in algorithm
        v = self.item_values;
        w = self.item_weights;
        n = self.Nitems
        c = self.Capacity

        # the dynamic programming function for the knapsack problem
        # the code was adapted from p17 of http://www.es.ele.tue.nl/education/5MC10/solutions/knapsack.pdf

        # v array holds the values / profits / benefits of the items
        # wv array holds the sizes / weights of the items
        # n is the total number of items
        # W is the constraint (the weight capacity of the knapsack)
        # solution: True in position n means pack item number n+1. False means do not pack it.

        # V and Keep should be 2d arrays for use in the dynamic programming solution
        # The are both of size (n + 1)*(W + 1)

        # Initialise V and keep
        # ADD CODE HERE

        # Set the values of the zeroth row of the partial solutions V to False
        # ADD CODE HERE

        # main dynamic programming loops, adding on item at a time and looping through weights from 0 to W
        # ADD CODE HERE

        # now discover which iterms were in the optimal solution
        # ADD CODE HERE
        V = np.zeros([n+1, c+1], dtype=int)
        progress = 0

        # i represents item(row) and j represents column(capacity)
        for i in range(1, n+1): #T(n)
            for j in range(1, c+1): #T(c)
                #if item exceeds capacity, take best from above row
                if w[i] > j:
                    V[i][j] = V[i-1][j]
                else:
                    # if item can be included, take max between above and including current
                    remainder = j - w[i]
                    V[i][j] = max(V[i-1][j], v[i] + V[i-1][remainder])
                    print(f"Progress: {progress}/{n*c}, Row: {i}, Col: {j}, Insert: {V[i][j]}")
                    progress += 1


        i, j = n, c
        while i > 0 and j > 0: #T(n)
            while V[i-1][j] == V[i][j] and i > 0:
                i-=1
            solution[i] = True
            j-=w[i]
            i-=1

        print("Run time: %fs" % (time.time() - start_time))

knapsk = dp(sys.argv[1])
solution = [False]*(knapsk.Nitems + 1)
knapsk.DP(solution);
knapsk.check_evaluate_and_print_sol(solution)

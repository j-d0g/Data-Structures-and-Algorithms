import sys
import time

from knapsack import knapsack

DOUB_MAX = 10e30 # a large number, must be greater than  max value of any solution
SIZE = 100000 # an estimate of how large the priority queue should become
NITEMS = 2000 # an upper limit of the number of itmes

class struc_sol:
    def __init__(self):
        self.solution_vec = [None]*(NITEMS + 1) # "binary" solution vector
        # solution_vec[1] = True means first item is packed in knapsack
        # solution_vec[1] = False means first item is NOT in knapsack
        # soltion_vec[0] is meaningless

        # objects of this class will also have self.val, self.bound and self.fixed for the value, upper bound of the solutoin and number of items fixed to either True (1) or False (0), not '*"
        self.val = -1
        self.fixed = 0
        self.children = [None]*2
        self.bound = 0


    def copy(self):
        copy = struc_sol()
        for i in range(0, NITEMS + 1):
            copy.solution_vec[i] = self.solution_vec[i]
        copy.val = self.val
        copy.fixed = self.fixed
        copy.bound = self.bound
        return copy

class bnb(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)
        self.QueueSize = 0 # the number of items currently stored in the priority queue
        self.QUIET = False # can be set of 1 to suppress output

    # The following four functions implement a priority queue
    # They are based on the functions given in Robert Sedgwick's book, Algorithms in C

    def upheap(self, qsize):
        # upheap reoders the elements in the heap (queue) afer an insertion

        temp_element = self.pqueue[qsize]
        self.pqueue[0].bound = DOUB_MAX

        while (self.pqueue[qsize//2].bound <= temp_element.bound):
            self.pqueue[qsize]=self.pqueue[qsize//2]
            qsize = qsize//2
        self.pqueue[qsize]=temp_element

    def insert(self, element):
        assert(self.QueueSize<SIZE-1)
        self.QueueSize = self.QueueSize+1
        self.pqueue[self.QueueSize]=element
        self.upheap(self.QueueSize)

    def downheap(self,qindex):
        # down heap reorders the elements in the heap (queue) after a removal

        temp_element = self.pqueue[qindex]
        while (qindex <= self.QueueSize//2):
            j=qindex + qindex
            if (j<self.QueueSize and self.pqueue[j].bound < self.pqueue[j+1].bound):
                j = j + 1
            if (temp_element.bound >= self.pqueue[j].bound):
                break
            self.pqueue[qindex] = self.pqueue[j]
            qindex = j
        self.pqueue[qindex]=temp_element

    def removeMax(self):
        head = self.pqueue[1]
        self.pqueue[1] = self.pqueue[self.QueueSize]
        self.QueueSize = self.QueueSize-1
        self.downheap(1)
        return head

    # End priority queue functions

    def print_sol(self,sol):
        # prints a solution in the form 000100xxx etc
        # with x's denoting the part of the solution not yet fixed (determined)

        print("%d %g " % (sol.val,sol.bound), end="")
        for i in range(1, sol.fixed + 1):
            if (sol.solution_vec[i]):
                s = "1"
            else:
                s = "0"
            print(s, end="")
        for i in range(sol.fixed + 1, self.Nitems + 1):
            print("x", end="")
            i = i + 1;
        print("")

    def frac_bound(self, sol, fix):
        # Updates the values sol.val and sol.bound

        # Computes the fractional knapsack upper bound
        # given a binary vector of items (sol->solution_vec),
        # where the first
        # "fix" of them are fixed. All that must be done
        # is compute the value of the fixed part; then
        # add to that the value obtained by adding in
        # items beyond the fixed part until the capacity
        # is exceeded. For the exceeded capacity, the fraction
        # of the last item added which would just fill the knapsack
        # is taken. This fraction of profit/value is added to the
        # total. This is the required upper bound.

        # Everything above assumes items are sorted in decreasing
        # profit/weight ratio

        totalp = 0 # profit total
        totalw =0 # weight total
        sol.val=-1

        # compute the current value and weight of the fixed part
        for i in range (1, fix + 1):
            if (sol.solution_vec[i]):
                totalw = totalw + self.item_weights[self.temp_indexes[i]]
                totalp = totalp + self.item_values[self.temp_indexes[i]]
        if (totalw > self.Capacity):
            return

        sol.val = totalp
        #   print("%g %d" % (totalp, totalw))

        # add in the rest of the items until capacity is exceeded
        i = fix + 1

        while (i <= self.Nitems and totalw < self.Capacity):
            totalw = totalw + self.item_weights[self.temp_indexes[i]]
            totalp = totalp + self.item_values[self.temp_indexes[i]]
            i = i + 1

        # if over-run the capacity, adjust profit total by substracting that overrun fractio of the last item
        if (totalw > self.Capacity):
            i = i - 1
            totalp = totalp - ((totalw - self.Capacity)/(self.item_weights[self.temp_indexes[i]])*self.item_values[self.temp_indexes[i]])
        sol.bound = totalp

    def branch_and_bound(self):
        start_time = time.time()
        self.pqueue[0] = struc_sol()
        self.frac_bound(self.pqueue[0], 0)
        start = struc_sol()
        self.frac_bound(start, 0)

        self.upper_bound = start.bound
        self.pqueue[1] = start # set a blank first element
        self.QueueSize += 1
        self.current_best = start

        while self.QueueSize > 0:
            temp = self.removeMax()
            if self.isFull(temp) and not self.isBetter(temp):
                continue
            if self.isBest(temp):
                print("Run time: %fs" % (time.time() - start_time))
                return temp.solution_vec
            if self.isBetter(temp): self.current_best = temp
            for child in self.generateChildren(temp):
                print(f"bound: {child.bound} upper bound: {self.upper_bound} weight: {self.computeWeight(child)} capacity: {self.Capacity} best: {self.current_best.val}")
                # if feasible, add to priority queue. if not, ignore (discard/prune)
                if self.isFeasible(child):
                    self.insert(child)

        print("Run time: %fs" % (time.time() - start_time))
        return self.current_best.solution_vec

    def isFeasible(self, sol):
        return sol.bound >= self.current_best.val and self.computeWeight(sol) <= self.Capacity

    def isBetter(self, sol):
    	return sol.val > self.current_best.val

    def isBest(self, sol):
        return sol.val == self.upper_bound

    def isFull(self, sol):
        return sol.fixed == self.Nitems

    def generateChildren(self, sol):
        childT = sol.copy()
        childT.fixed+=1
        childT.solution_vec[sol.fixed] = True
        self.frac_bound(childT, childT.fixed)
        sol.children[1] = childT

        childF = sol.copy()
        childF.fixed+=1
        childF.solution_vec[sol.fixed] = False
        self.frac_bound(childF, childF.fixed)
        sol.children[0] = childF

        return sol.children

    def computeWeight(self, sol):
        weight = 0
        for idx, item in enumerate(sol.solution_vec):
            if idx == 0:
                continue
            if item:
                # print(item)
                weight += self.item_weights[self.temp_indexes[idx]]
                # print(weight)
        return weight


        # branch and bound

        # start with the empty solution vector
        # compute its value and its bound
        # put current_best = to its value
        # store it in the priority queue

        # LOOP until queue is empty or upper bound is not greater than current_best:
        #   remove the first item in the queue
        #   construct two children, 1 with a 1 added, 1 with a O added
        #   FOREACH CHILD:
        #     if infeasible, discard child
        #     else
        #       compute the value and bound
        #       if value > current_best, set current_best to it, and copy child to final_sol
        #       add child to the queue
        # RETURN


        # YOUR CODE GOES HERE

    def copy_array(self, array_from, array_to):
        # This copies Nitems elements of one boolean array to another
        # Notice it ignores the 0th item of the array
        for i in range(1, self.Nitems+1):
            array_to[i] = array_from[i]



knapsk = bnb(sys.argv[1])
assert(NITEMS >= knapsk.Nitems)
final_sol = [False]*(knapsk.Nitems + 1)
knapsk.sort_by_ratio()

knapsk.pqueue = [None]*SIZE

final_sol = knapsk.branch_and_bound()
print("Branch and Bound Solution of Knapack is:")
knapsk.check_evaluate_and_print_sol(final_sol)

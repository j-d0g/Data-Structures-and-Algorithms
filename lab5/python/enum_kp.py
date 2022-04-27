import sys

from knapsack import knapsack

class enum_knapsack(knapsack):
    def __init__(self, filename):
        knapsack.__init__(self, filename)

    def enumerate(self):
        # Do an exhaustive search (aka enumeration) of all possible ways to pack
        # the knapsack.
        # This is achived by creating every "binary" solution vectore of length Nitems.
        # For each solution vector, its value and weight is calculated

        solution = [False]*(self.Nitems + 1) # (binary/ true/false) solution vectore representing items pack
        best_solution = [False]*(self.Nitems + 1) # (binary) solution veectore for best solution found
        ideal_solution = [False, True, True, False, False, True, False, False, True, True, False, True, True, False, True, False, False, True, True, False, True]
        j = 0.0

        self.QUIET = True
        best_value = 0 # total value packed in the best solution
        progress = 0
        progress_bar_old = 0
        temp_value = 0

        while (not self.next_binary(solution, self.Nitems)):
            # ADD CODE IN HERE TO KEEP TRACK OF FRACTION OF ENUMERATION DONE
            progress += 1
            progress_bar = int((progress / 2 ** self.Nitems) * 100)
            if progress_bar != progress_bar_old:
                print(f"Current Progress: {progress_bar}%")
            progress_bar_old = progress_bar
            # calculates the value and weight and feasibility
            infeasible = self.check_evaluate_and_print_sol(solution)
            # ADD CODE TO PRINT OUT BEST SOLUTION
            curr_value = self.total_value
            if not infeasible and curr_value > best_value:
                best_solution = self.duplicate_array(solution)
                best_value = curr_value

        print(f"The maximum profit is: {best_value}")
        self.print_solution(best_solution)

    def duplicate_array(self, sol):
        temp = []
        for item in enumerate(sol):
            temp.append(item);
        return temp

    def print_solution(self, sol):
        for i in sol:
            print(i)

    # def current_profit(self, sol):
    #     curr_value = 0
    #     for i in range(1, self.Nitems):
    #         if sol[i] == True:
    #             curr_value += self.item_values[i]
    #     return curr_value

    def next_binary(self, sol, Nitems):
        # Called with a "binary" vector of length Nitmes, this
        # method "adds 1" to the vector, e.g. 0001 would turn to 0010.
        # If the string overflows, then the function returs True, else it returns False
        i = Nitems
        while (i > 0):
            if (sol[i]):
                sol[i] = False
                i = i -1
            else:
                sol[i] = True
                break
        if (i == 0):
            return True
        else:
            return False




knapsk = enum_knapsack(sys.argv[1])
knapsk.print_instance()
knapsk.enumerate()

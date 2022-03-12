import config

class bstree:
    def __init__(self, value=None):
        self.verbose = config.verbose
        self.left = None
        self.right = None
        self.value = value
        self.num_of_comparisons = 0

    def size(self):
        if (self.value != None):
            if self.left is not None and self.right is not None:
                return 1 + self.left.size() + self.right.size()
            elif self.left is not None:
                return 1 + self.left.size()
            elif self.right is not None:
                return 1 + self.right.size()
            else:
                return 1
        return 0

    def is_a_tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    def height(self):
        if self.value == None:
            return -1

        if self.left != None:
            left_tree_height = self.left.height()
        else:
            left_tree_height = 0

        if self.right != None:
            right_tree_height = self.right.height()
        else:
            right_tree_height = 0

        max_height = max(left_tree_height, right_tree_height)
        return max_height + 1

    # Done
    def insert(self, value):
        # if (self.is_a_tree()):
        if (self.value != None):
            self.num_of_comparisons += 1
            # if value at current node is equal to value to insert, exit
            if self.value == value:
                return
            # if value at current node < value to insert, recurse right
            if self.value < value:
                if self.right == None:
                    self.right = bstree(value)
                else:
                    self.right.insert(value)
            # if value at current node > value to insert, recurse left
            if self.value > value:
                self.num_of_comparisons += 1
                if self.left == None:
                    self.left = bstree(value)
                else:
                    self.left.insert(value)
        else:
            self.value = value

    # Done
    def find(self, value):
        # if self.is_a_tree():
        if self.value != None:
            self.num_of_comparisons += 1
        # if the value at the current node > value to find, recurse right
            if value > self.value and self.right != None:
                return self.right.find(value)
        # if the value at the current node < value to find, recurse left
            if value < self.value and self.left != None:
                return self.left.find(value)
        # if value at node = value to find, return True
            if self.value == value:
                return True
        return False


    # You can update this if you want
    def print_set_recursive(self, depth):
        # if self.is_a_tree():
        if (self.value != None):
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            if (self.left != None):
                self.left.print_set_recursive(depth + 1)
            if (self.right != None):
                self.right.print_set_recursive(depth + 1)

    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)

    def print_stats(self):
        # TODO update code to record and print statistic
        print("Size of tree: " + str(self.size()))
        print("Height of tree: " + str(self.height()))
        print("Average number of comparisons per operation: " + str(self.num_of_comparisons / self.size()))

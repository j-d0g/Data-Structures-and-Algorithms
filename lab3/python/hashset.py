from enum import Enum
import config

# # TODO:

class hashset:

    def __init__(self):
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size
        self.size = 0
        self.hash_table = [None for i in range(self.hash_table_size)]
        # self.hash_table_chain = [][]
        self.num_of_collisions = 0
        self.duplicates_removed = 0
        self.LOAD_FACTOR_LIMIT = 0.5

# --------------- Helper-Methods ---------------- #

    # Returns True if the table has reached full capacity
    def get_lf(self):
        return self.size / self.hash_table_size

    # Returns True if the index is empty
    def is_empty(self, index):
        if (self.hash_table[index] == None):
            return True
        return False

    # Helper functions for finding prime numbers
    def is_prime(self, n):
        i = 2
        while (i * i <= n):
            if (n % i == 0):
                return False
            i = i + 1
        return True

    def next_prime(self, n):
        while (not self.is_prime(n)):
            n = n + 1
        return n

    def prev_prime(self, n):
        while (not self.is_prime(n)):
            n = n - 1
        return n

    # Dynamically resizes table
    def resize_table(self):
        self.hash_table_size = self.next_prime(self.hash_table_size * 2)
        old_table = self.hash_table
        self.hash_table = [None for i in range(self.hash_table_size)]
        for value in old_table:
            if value is not None:
                self.insert(value)

# -------------------- Hashing ------------------- #

    # Basic hashing method
    def hash_1(self, value):
        total, n = 0, self.hash_table_size
        for chr in value:
            total += ord(chr)
        return total % n

    # Polynomial hashing method
    def hash_2(self, value):
        total, c, n = 0, 29, self.hash_table_size
        for idx, chr in enumerate(value):
            total += c**ord(chr)
        return abs(total) % n

    # Second hashing method (for double-hashing)
    def hash_3(self, value):
        prime = self.prev_prime(self.hash_table_size)
        return prime - (self.hash_1(value) % prime)

# ----------------- Main Methods ---------------- #

    # Inserts an element onto Hash Table
    def insert(self, value):
        print("Size of table: %d" % self.hash_table_size)
        print("Size: %d" % self.size)
        # Resizes table if specified lf load factor limit exceeded.
        if (self.get_lf() >= self.LOAD_FACTOR_LIMIT):
            self.resize_table()
        index = self.get_hash(value)
        # if duplicate, skip
        if (self.find(value)):
        # if (self.hash_table[index] == value):
            self.duplicates_removed += 1
            return
        # while there is a collision, handle it
        increment = 1
        while not(self.is_empty(index)):
            index = self.handle_collision(value, increment)
            increment += 1
            self.num_of_collisions += 1
        print("Available index found! :%d" %index)
        # Insert, update stats
        print("Inserting at index %d: " %index + value)
        self.hash_table[index] = value
        self.size += 1

    # Searches for a given word
    def find(self, value):
        index = self.get_hash(value)
        increment = 1
        # Given the slot isn't empty, while the value isn't the word we're looking for...
        while (not(self.is_empty(index)) and self.hash_table[index] != value):
            index = self.handle_collision(value, increment)
            increment += 1
            self.num_of_collisions += 1
        # Returns True if it's in the Hash Table, False if not.
        return (self.hash_table[index] == value)

# ----------------- Process Modes ---------------- #

    # Process correct hashing method
    def get_hash(self, value):
        if (self.mode >= 0 and self.mode <= 3):
            return self.hash_1(value)
        else :
            return self.hash_2(value)

    # Helper to processes correct collision-handling method
    def handle_collision(self, value, increment):
        # Double hashing 1
        if (self.mode == HashingModes.HASH_1_DOUBLE_HASHING.value):
            return self.double_hash(self.hash_1(value), self.hash_3(value), increment)
        # Double hashing 2
        if (self.mode == HashingModes.HASH_2_DOUBLE_HASHING.value):
            return self.double_hash(self.hash_3(value), self.hash_1(value), increment)
        # Linear-probing
        if (self.mode == HashingModes.HASH_1_LINEAR_PROBING.value or self.mode == HashingModes.HASH_2_LINEAR_PROBING.value):
            return self.linear_probe(self.get_hash(value), increment)
        # Quadratic-probing
        if (self.mode == HashingModes.HASH_1_QUADRATIC_PROBING.value or self.mode == HashingModes.HASH_2_QUADRATIC_PROBING.value):
            return self.quadratic_probe(self.get_hash(value), increment)
        # Separate chaining
        # if (self.mode == HashingModes.HASH_1_SEPARATE_CHAINING.value or self.mode == HashingModes.HASH_2_SEPARATE_CHAINING.value):
        #     return self.separate_chain(self.get_hash(value), increment)

# --------------- Collision-Handling -------------- #

    def linear_probe(self, index, increment):
        return (index + increment) % self.hash_table_size

    def quadratic_probe(self, index, increment):
        return (index + increment**2) % self.hash_table_size

    def double_hash(self, index, index2, increment):
        return (index + (increment * index2)) % self.hash_table_size

    # def separate_chain(self, index, increment):
    #     return self.hash_table_chaining[index][increment-1]

# ------------------- Diagnostics ------------------ #

    def print_set(self):
        for word in self.hash_table:
                print(word)

    def print_stats(self):
        print("Hash-set contains %d elements\n" % self.size)
        print("%d collisions occurred\n" % self.num_of_collisions)
        print("Duplicates removed: %d" %self.duplicates_removed)

# ------------------ Hashing Modes ----------------- #

class HashingModes(Enum):
    HASH_1_LINEAR_PROBING=0
    HASH_1_QUADRATIC_PROBING=1
    HASH_1_DOUBLE_HASHING=2
    HASH_1_SEPARATE_CHAINING=3
    HASH_2_LINEAR_PROBING=4
    HASH_2_QUADRATIC_PROBING=5
    HASH_2_DOUBLE_HASHING=6
    HASH_2_SEPARATE_CHAINING=7

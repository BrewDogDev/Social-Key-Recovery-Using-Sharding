import math
def is_power_of_two(n):
    return (math.ceil(math.log2(n)) == math.floor(math.log2(n)))
def is_even(n):
    return n%2 == 0
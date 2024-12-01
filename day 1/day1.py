import numpy as np
import operator
from functools import lru_cache
import time

######################## Part 1 ############################

# Open the file
with open('input.txt', 'r') as file:
    # Read each line and take out the separators
    lines = file.read().replace('\n','   ').split('   ')[:-1]
    
lines_int = [int(x) for x in lines]

# Get columns from odd/even items
left_list = sorted(lines_int[::2])
right_list = sorted(lines_int[1::2])

# Distance between everything - subtract, get abs value
distances = list(map(operator.sub,left_list,right_list))
abs_distances = [abs(x) for x in distances]

# Part 1 answer
print(np.sum(abs_distances))

######################## Part 2 ############################

start_time = time.time()

# For the right (even) set there are ~400 duplicated numbers
# If we want our cache results to speed it up, we have to calculate going from the right to left list - this gives the same result
@lru_cache
def get_score(item):
    filtered = filter(lambda x: x == item,left_list)
    occurrences = len(list(filtered))
    return item * occurrences

scores = [get_score(x) for x in right_list]

# Part 2 answer
print(np.sum(scores))

# Adding the cache saves a bit of time
end_time = time.time()
print(end_time-start_time)


import operator
from functools import lru_cache
import time

start_time = time.time()

######################## Part 1 ############################

data = list(map(int,open('input.txt').read()[:-1].replace('\n','   ').split('   ')))

# Get columns from odd/even items
left_list,right_list = sorted(data[::2]), sorted(data[1::2])

# Distance between everything - subtract, get abs value
distances = list(map(abs,map(operator.sub,left_list,right_list)))

# Part 1 answer
print(sum(distances))

######################## Part 2 ############################

# For the right (even) set there are ~400 duplicated numbers
# If we want our cache results to speed it up, we have to calculate going from the right to left list - this gives the same result
@lru_cache
def get_score(item):
    filtered = filter(lambda x: x == item,left_list)
    occurrences = len(list(filtered))
    return item * occurrences

scores = [get_score(x) for x in right_list]

# Part 2 answer
print(sum(scores))

###########################################################

# Adding the cache saves a bit of time
end_time = time.time()
print(end_time-start_time)

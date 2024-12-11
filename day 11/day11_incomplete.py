import time
import math
from functools import cache
from multiprocessing import cpu_count, Pool

######################## Part 1 ############################

file = open('input.txt').read()[:-1]
data = file

# Remove leading zeros from a numerical string
no_zero = lambda x: str(int(x)) 

# In an effort to faster return any previous inputs
@cache
def applyrules(stone):
    length = len(stone)
    # Rule 1
    if int(stone) == 0:
        return "1"
    # Rule 2
    elif length == 2:
        return stone[0] + " " + stone[1]
    # Rule 3
    elif length % 2 == 0:
        return no_zero(stone[:int(length/2)]) + " " + no_zero(stone[-int(length/2):])
    # Otherwise
    return str(int(stone)*2024)
    
# Processes a full blink for each stone 
def blink(stones):
    line = ""
    for stone in stones.split(" "):
        # Adding a space to separate stones
        line += applyrules(stone) + " "
    return line[:-1]

# Blink 25 times
for i in range(25):
    data = blink(data)
    
# Part 1 answer
splits = data.split(" ")
print(len(splits))

######################## Part 2 ############################

# Cannot process 75 blinks this way
# Not complete yet - sort list largest to smallest, process and cache to catch smaller numbers?
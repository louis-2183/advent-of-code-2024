import time
import numpy as np
from operator import add, mul

######################## Part 1 ############################

# File straight to array
data = [l[:-1] for l in open('input.txt')]

def process_line(l,operators):
    # Define the target number and remaining numbers in the equation and map to int
    goal, *equation = map(int,l.replace(':','').split())
    
    # Get the first number
    nums = [equation[0]]

    for rem in equation[1:]:
        # For every other number, apply all operations to numbers we have and construct the new list
        nums = [op(x,rem) for x in nums for op in operators]
    
    # If the goal number is in this list of combinations, return it
    if goal in nums:
        return goal
    
    return 0
        
score = 0

# Store bad lines since we only need to process these for part 2
bad_lines = []

for line in data:
    # Get combinations line by line with add and multiply
    result = process_line(line,[add,mul])
    
    if result == 0:
        bad_lines.append(line)
    else:
        score += result
    
# Part 1 answer
print(score)

######################## Part 2 ############################
        
score2 = 0

start_time = time.time()

# Define a function to concatenate 2 integers
concat = lambda x,y: int(str(x)+str(y))

# For each bad line, is there a possible score with the concat operation. If so, fetch the score
for idx,line in enumerate(bad_lines):
    score2 += process_line(line,[add,mul,concat])
    
end_time = time.time()
print(end_time-start_time)

# Part 2 (plus part 1 answer)
print(score2+score)

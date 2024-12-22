from math import pi,sin,cos
import numpy as np
from itertools import combinations

######################## Part 1 ############################

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 

data = [l[:-1] for l in open('input.txt')]

# Fetch start and end coords of the grid
for y,line in enumerate(data):
    if 'S' in line:
        start_y,start_x = y,line.index('S')
    if 'E' in line:
        end_y,end_x = y,line.index('E')
        
# List of already traversed positions
traversed = []

# Branches out from the current position and returns new position in the maze
def coord_check(x):
    # Add all directions
    new = [list(np.add(x,d)) for d in directions]
    for n in new:
        if n not in [x[:2] for x in traversed]:
            # If it is a free space that has not been traversed, return that position
            if data[n[0]][n[1]] == '.':
                return n
    
    # End has been reached
    return False

goal = False

# Iterate from the starting position
sy,sx = start_y,start_x

# Go through the grid, adding the cost and position of all traversed path items
while goal == False:
    traversed.append([sy,sx,len(traversed)])        
    # Keep updating coordinates
    result = coord_check([sy,sx])
    
    # If the path has finished, break the loop - we have all points we need
    if not result:
        # Plus the ending one
        traversed.append([end_y,end_x,len(traversed)])
        goal = True
    else:
        # Update coords for next iteration
        sy,sx = result
        
# List of cheats that meet criteria
solutions = []

# Combinations of all points that can be jumped from
comb = combinations(traversed,2)

for first,last in comb:
    # Distance between the two unique points, distance in scores
    dy,dx,t = map(abs,np.subtract(first,last))
    # If their manhattan distance is 2, we are jumping through a wall
    if (dy+dx == 2):
        # Saved time is the distance in scores - (dy+dx)
        saved = t-2
        # If any time is saved and it's more than 99 picoseconds
        if saved != 0 and saved >= 100:
            solutions.append(saved) 
            
# Part 1 answer
print(len(solutions))

######################## Part 2 ############################

solutions.clear()
comb = combinations(traversed,2)

# Slight variation of the previous function. Checks if manhattan distance is less than 21 but still above 2
for first,last in comb:
    dy,dx,t = map(abs,np.subtract(first,last))
    if (dy+dx > 1) and (dy+dx < 21):
        saved = (t-(dy+dx))
        # Is any time saved thats more than 99 picoseconds
        if saved != 0 and saved >= 100:
            solutions.append(saved) 

# Part 2 answer
print(len(solutions))
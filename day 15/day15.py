from math import pi,sin,cos
import numpy as np
from copy import deepcopy

######################## Part 1 ############################

data, instructions = open('input.txt').read().split('\n\n')

# Create the standard version of the grid and instructions
grid = [[char for char in x] for x in data.split('\n')]
instructions = instructions.replace('\n','')

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 
instructions_map = ['>','v','<','^']

# Fetch starting position
for y,line in enumerate(grid):
    if '@' in line:
        start_y,start_x = y,line.index('@')
        
# Loops through and returns whether there is a space free or blocked, updating grid positions if valid
def trymove(ch,py,px,instr):
    d = directions[instructions_map.index(instr)]
    new = list(np.add(d,[py,px]))
    char = grid[new[0]][new[1]]
    
    result = False
    if char == '.':
        # Space is at the end of the objects we checked, all movements are valid
        result = True
    elif char == 'O':
        # If there is another box, try to move the following box first
        result = trymove('O',new[0],new[1],instr)[0]
    
    if result:
        # Update the grid end to start if the given move is valid
        grid[py][px] = '.'
        grid[new[0]][new[1]] = ch
    else:
        # Revert 
        new = [py,px]
        
    return result, new[0], new[1]
        
# Execute the instructions and update the grid
py,px = start_y,start_x
for i in instructions:
    worked, py, px = trymove('@',py,px,i)
    
score = 0
    
# Add to the score for all end box positions
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == 'O':
            score += (100*y) + x
            
# Part 1 answer
print(score)

######################## Part 2 ############################

# Make the grid bigger and split again
grid = data.translate(str.maketrans({'#':'##','O':'[]','.':'..','@':'@.'}))
grid = [[char for char in x] for x in grid.split('\n')]

# Update starting position
start_x = start_x*2
        
# Based on how trymove_big() works, the all() function will create an infinite loop while trying to move both items from a box 
# Scan for any existing space from a given box and return the result if we know there is no possible space
def scan_hor(ny,nx,instr):
    char = grid[ny][nx]
    
    # Only for cases moving horizontally
    if instr == '^' or instr == 'v': 
        return True
    # Loop through until we get a wall or a space
    while char != '#' and char != '.':
        ny,nx = list(np.add([ny,nx],directions[instructions_map.index(instr)]))
        char = grid[ny][nx]
    if char == '#':
        return False
    else:
        return True

# Variant of the last function, accounting for validity of both box characters being able to move
def trymove_big(ch,py,px,instr,rec):
    d = directions[instructions_map.index(instr)]
    new = list(np.add(d,[py,px]))
    
    char = grid[new[0]][new[1]]
    
    result = False
    if char == '#':
        result = False
    elif char == '.':
        result = True
    elif char == ']':
        # Check we can move the item and its counterpart
        if scan_hor(py,px,instr):
            result = all([trymove_big('[',new[0],new[1]-1,instr,rec+1)[0],trymove_big(']',new[0],new[1],instr,rec+1)[0]])
        else:
            # No space for this box, revert
            result = False
    elif char == '[':
        # Check we can move the item and its counterpart
        if scan_hor(py,px,instr):
            result = all([trymove_big(']',new[0],new[1]+1,instr,rec+1)[0],trymove_big('[',new[0],new[1],instr,rec+1)[0]])
        else:
            # No space for this box, revert
            result = False
    
    if result:
        grid[py][px] = '.'
        grid[new[0]][new[1]] = ch
    else:
        new = [py,px]
        
    # The grid may be updated erroneously - value of result indicates if this happened
    return result, new[0], new[1]

# Copy the grid to revert back to in case there are erroneous updates
base = deepcopy(grid)

# Start from the new starting position
py,px = start_y,start_x

for i in instructions:
    # Update the grid and see if it was a valid update
    worked,py,px = trymove_big('@',py,px,i,0)
    if not worked:
        # If it was not, revert to the last valid version
        grid = deepcopy(base)
    else:
        # If it was, set the last valid version
        base = deepcopy(grid)
        
score = 0
        
# Add to the score for all end box positions (from the last valid grid)
for y in range(len(base)):
    for x in range(len(base[0])):
        if grid[y][x] == '[':
            score += (100*y) + x

# Part 2 answer
print(score)

############################################################
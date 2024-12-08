from math import pi, sin, cos
import numpy as np
import time

start_time = time.time()

######################## Part 1 ############################

data = [list(l[:-1]) for l in open('input.txt')]

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 

# Turn 90 degrees to the right
turn = lambda x: x+1 if x+1 <= 3 else 0

# Bounds of grid
ymax,xmax=len(data)-1,len(data[0])-1

# Define a function to check coords seeing if they are valid in the grid
bounds_check = lambda x: True if (0 <= x[0] <= ymax) and (0 <= x[1] <= xmax) else False

# Get guard position
for idx, line in enumerate(data):
    if '^' in line:
        initial_guard_pos = [idx,line.index('^')]
        break;
        
# Iterates across the grid from a starting position+angle. Takes an optional position for an additional obstacle
def run_grid(curr_pos,angle,obstacle):
    # Stores visited positions + angles
    visited = []
    end_reached = False
    while end_reached == False:
        # Add vector on to get future position
        future_pos = np.add(curr_pos,directions[angle])
        if bounds_check(future_pos):
            # If we are within bounds and hit an obstacle, turn to the right
            if data[future_pos[0]][future_pos[1]] == '#' or all(future_pos == obstacle):
                angle = turn(angle)
                continue
        else:
            # Out of bounds means we can stop
            end_reached = True
            
        # Register the current position as visited 
        visited.append(str(curr_pos[0])+','+str(curr_pos[1])+','+str(angle))
        
        # Angles are stored in addition to position. If the same position is visited at the same angle,
        # this shows that the guard is repeating their path. This will only occur in Part 2.
        if len(set(visited)) != len(visited):
            return False
        
        # If it is valid, take a step forward
        curr_pos = future_pos
    return visited

visited = run_grid(initial_guard_pos,3,None)

# Part 1 answer - all unique positions
print(len(set([v[:-2] for v in visited])))

######################## Part 2 ############################

score = 0

# Fetch starting variables
starting_pos = initial_guard_pos.copy()
starting_angle = 3

# Set for unique obstacle positions
obstacles = set()

# Go along the path we ran across before
for position in visited:
    # Get x, y and angle of the current path item
    y,x,a = map(int,position.split(','))
    # Activate motion for the guard (from the start) - placing an obstacle where the current path item is.
    result = run_grid(starting_pos,starting_angle,[y,x])
    
    # If the obstacle causes the guard to loop
    if result == False:
        # Assume the obstacle's position and start from there, instead of re-running the path from the start
        starting_pos = [y,x]
        starting_angle = a
        # Register the valid obstacle position
        obstacles.add(repr(starting_pos))
        
# Part 2 answer
print(len(obstacles))

###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")
    

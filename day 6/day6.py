from math import pi, sin, cos

######################## Part 1 ############################

# File straight to array
data = [list(l[:-1]) for l in open('input.txt')]

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 

# Turn 90 degrees to the right
turn = lambda x: x+1 if x+1 <= 3 else 0

# Bounds of grid
maxx = len(data[0])-1
maxy = len(data)-1

# Get guard position
for idx, line in enumerate(data):
    if '^' in line:
        initial_guard_pos = [idx,line.index('^')]
        break;
        
def run_path(guard_pos,starting_angle):
    # Starting angle (3=up)
    angle = starting_angle
    
    # Store all visited positions
    positions = []
    
    # Do until guard goes out of bounds
    while True:
        # Future position according to current angle
        future_pos = [guard_pos[0]+directions[angle][0],guard_pos[1]+directions[angle][1]]
        
        # If we are not out of bounds
        if (0 <= future_pos[0] <= maxy) and (0 <= future_pos[1] <= maxx):
            
            # If an obstacle is where we are about to go, turn in place instead 
            if data[future_pos[0]][future_pos[1]] == '#':
                angle = turn(angle)
                continue
            
            else:                
                # Take a step forward
                guard_pos = future_pos
        else:
            # We have reached the end of the guard's path
            return positions
    
        # Record position and angle as visited
        positions.append(str(guard_pos[0])+','+str(guard_pos[1])+','+str(angle))

visited = run_path(initial_guard_pos,3)

# Part 1 answer - all unique positions
print(len(set([v[:-2] for v in visited]))+1)

######################## Part 2 ############################
import numpy as np
from math import pi,sin,cos

######################## Part 1 ############################

data = [list(map(int,l[:-1].split(','))) for l in open('input.txt')]

# Size of grid for testing
SIZE = 71

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 

# Populate the grid, activate the first 1024 obstacles
grid = [["."]*SIZE for i in range(SIZE)]

for entry in data[:1024]:
    grid[entry[1]][entry[0]] = '#'
    
# Function to check if we are indexing within bounds
in_bounds = lambda x,y: 0<=x<SIZE and 0<=y<SIZE

# Checks surrounding areas to move and returns all valid next steps
def get_valid(y,x,t):
    # Valid future positions
    p = []
    
    # Add the directions to the current position
    new = [list(np.add([y,x],d)) for d in directions]
    
    for n in new:
        if in_bounds(n[0],n[1]):
            char = grid[n[0]][n[1]]
            if (n not in t) and (char == '.'):
                # If we are in bounds, not going into an obstacle, and this is a position we have not already traversed
                p.append(n)
    return p 

# Finds a path through the current grid state. If this is not possible returns 0
# Variation of Djikstra's
def traverse():
    # Variations of paths to branch off from
    paths = [[0,0]]
    
    # Already traversed positions
    traversed = []
    
    # Steps taken
    steps = 0
    
    # While there are still paths to explore
    while len(paths) > 0:
        # Store a list of new positions if the paths branch out
        new_paths = []
        
        # For all the new positions
        for p in paths:
            traversed.append(p)
            
            # If we have met the goal, we have found the fastest route (as we are already globally checking traversed positions)
            if p[0] == (SIZE-1) and p[1] == (SIZE-1):
                return steps
            
            # If not, see where the current branches branch to 
            result = get_valid(p[0],p[1],traversed)
            
            for r in result:
                if r not in new_paths:
                    # Only add unique new positions rather than computing multiple
                    new_paths.append(r)
        steps += 1
        paths = new_paths.copy()
        
    # Path is not possible - return 0
    return 0

# Traverse along the grid with 1024 fallen obstacles, return the shortest path steps
t = traverse()

# Part 1 answer
print(t[0])

######################## Part 2 ############################

# Since we don't want to compute every path for every new variation above 1024, find if there are no possible paths after every 100th iteration
for idx, entry in enumerate(data[1024:]):
    grid[entry[1]][entry[0]] = '#'
    
    if idx % 100 == 0:
        # Only need to check if the fallen obstacle was in the previously traversed path
        if [entry[1],entry[0]] in t[1]:
            if traverse()[0] == 0:
                # Path was not found - somewhere in the previous 100 iterations it was blocked! 
                # Set the upper limit
                upper_100 = 1024+idx+1
                break

# Go backwards by 100 checking every previous iteration
for i in reversed(data[upper_100-100:upper_100+1]):
    # Removing obstacles 
    grid[i[1]][i[0]] = '.'
    
    # If the path is not blocked now, get the coords of the removed obstacle
    if traverse()[0] != 0:
        position = f"{i[0]},{i[1]}"
        break
    
# Part 2 answer
print(position)

############################################################
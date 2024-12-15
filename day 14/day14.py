import re
import numpy as np
from collections import defaultdict
from math import dist
from itertools import combinations

######################## Part 1 ############################

data = [re.sub(r'[^\d-]+',' ',l[:-1])[1:] for l in open('input.txt')]

# Width, length of grid tiles
xlen,ylen = 101,103

# Midpoints to select quadrants from
midx,midy = (xlen-1)/2,(ylen-1)/2

# Robots per quadrant
quadrant_scores = defaultdict(int)

# Moves a robot by its velocity for a given amount of iters / seconds
def move_robot(iters,px,py,vx,vy):
    # Get final position, accounting for wrapping around the grid
    px,py = (px+(iters*vx)) % xlen,(py+(iters*vy)) % ylen

    # If we are in a valid position for a quadrant upon finishing
    if px != midx and py != midy:
        # Binary of the conditions of which half the robot in represents its quadrant
        quadrant = int(f"{int(px > midx)}{int(py > midy)}",2)
        # Increment the amount of robots in the given quadrant
        quadrant_scores[quadrant] += 1

for line in data:
    # Fetch position, velocity for a given robot
    args = list(map(int,line.split(' ')))
    # Move for 100 seconds
    move_robot(100,*args)

# Part 1 answer - Quadrant scores multiplied    
print(np.prod(list(quadrant_scores.values())))

######################## Part 2 ############################

# Wow, this was an unexpected twist

# Updates a robot's position for 1 iteration instead of skipping to the end
def move_robot_update(px,py,vx,vy):
    px,py = (px+(vx)) % xlen,(py+(vy)) % ylen
    return (px,py)

# Average distance between every point to indicate if robots are crowding
def get_sparsity(pos):
    distances = [dist(p1, p2) for p1, p2 in combinations(pos, 2)]
    return np.mean(distances)

# Store all initial positions and velocities of robots
positions = []
velocity = []

for line in data:
    args = list(map(int,line.split(' ')))
    positions.append(args[:2])
    velocity.append(args[-2:])

# Store sparsity of robots for every iteration
sparsities = []

for i in range(0,10000):
    # Increment robot positionss for a single iteration
    positions = [move_robot_update(*positions[x],*velocity[x]) for x in range(len(positions))]
    # Fetch the measure of sparsity between all robots
    sparsities.append(get_sparsity(positions))
    
# Get the indexes of all iterations
ls = [[i,d] for i,d in enumerate(sparsities)]
# Sort for the indexes where the robots are less sparse
ls = sorted(sparsities,key=lambda x: x[1])

# Part 2 answer - index of where sparsity is the lowest + 1
print(ls[0][0]+1)

############################################################
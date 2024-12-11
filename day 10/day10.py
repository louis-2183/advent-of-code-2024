import numpy as np
from math import pi,sin,cos
import time

start_time = time.time()

######################## Part 1 ############################

data = [l[:-1] for l in open('input.txt')]

# List of possible ends of a trail
trail_ends = []

# Grid bounds
xmax,ymax = len(data),len(data[0])

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 

# Function to check if a pair of coords is within bounds
in_bounds = lambda x: 0<=x[0]<=ymax-1 and 0<=x[1]<=xmax-1

# Takes a step through the trail one by one
def follow_trail(start_pos):
    # Add all the possible directions to the point and make it iterable
    points = [np.add(start_pos,x) for x in directions]
    for p in points:
        # Only if a point is in bounds
        if in_bounds(p):
            # Get current and next pos
            curr_pos,next_pos = data[start_pos[0]][start_pos[1]],data[p[0]][p[1]]
            # If we are moving from an 8 to a 9, record the end position
            if next_pos == '9' and curr_pos == '8':
                trail_ends.append(f"{p[0]},{p[1]}")
            # If it is not the finish, but a valid advancement, take the next step
            elif int(next_pos) == int(curr_pos)+1:
                follow_trail([p[0],p[1]])

score = 0

# Loop through grid
for y in range(ymax):
    for x in range(xmax):
        # If we are at a 0 (starting position)
        if data[y][x] == '0':
            trail_ends.clear()
            # Append to trail ends based on current trail only
            follow_trail([y,x])
            # Set of trail ends gives us all possible trail ends we can reach
            score += len(set(trail_ends))
                
# Part 1 answer
print(score)

######################## Part 2 ############################

# Part 2 is simpler - add 1 when the end of a trail is encountered regardless of whether it is a duplicate position
# Simple change to the previous function. Just don't make trailheads a set

score = 0

for y in range(ymax):
    for x in range(xmax):
        if data[y][x] == '0':
            trail_ends.clear()
            follow_trail([y,x])
            # No deduplication gets us all the possible paths regardless of if they finish on the same point
            score += len(trail_ends)
            
print(score)

###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")
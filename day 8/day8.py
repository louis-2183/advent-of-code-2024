from collections import defaultdict
from itertools import combinations
import numpy as np

######################## Part 1 ############################

# File straight to array
data = [l[:-1] for l in open('input.txt')]

# Define a defaultdict for antenna locations since we need to populate lists for each antenna
antennas = defaultdict(list)

# Y and X bounds of grid
ymax,xmax = len(data)-1,len(data[0])-1

# Define a function to check coords seeing if they are valid in the grid
bounds_check = lambda x: True if (0 <= x[0] <= ymax) and (0 <= x[1] <= xmax) else False

# Define an empty set of unique positions
locations = set()

# Harvest antenna coords in the grid and append them
for y in range(len(data)):
    for x in range(len(data[y])):
        char = data[y][x]
        if char != '.':
            # If an antenna is present, append coords
            antennas[char].append([y,x])
         
# Checks each location and applies add/subtract function to see valid positions for antinodes
def check_location(loc,diff,func):
    # Apply add/subtract function
    loc = func(loc,diff)
    # If position is valid, add it to the set of positions
    if bounds_check(loc):
        locations.add(str(loc[0])+','+str(loc[1]))
         
# Check all antennas, applying check_func to all possible pairs of antenna
def check_antennas(check_func):
    # For each frequency of antenna
    for k in antennas.keys():
        # Coordinates of antennas with selected frequency
        coords = antennas[k]
        # Get all possible pairs of antennas
        pairs = list(combinations(coords,2))
        for p in pairs:
            # Work out dy/dx for pair
            diff = np.subtract(p[0],p[1])
            
            # Add to the first point, subtract for the second and add to positions if not OOB
            check_func(p[0],diff,np.add)
            check_func(p[1],diff,np.subtract)
        
# Part 1 answer
check_antennas(check_location)
print(len(locations))

######################## Part 2 ############################

# Define an empty set of unique positions
locations = set()

# Slight variation of the previous function. Simply iterates across and applies function multiple times
def check_location_many(loc,diff,func):
    oob = False
    # If OOB hasn't been reached yet
    while oob == False:        
        if bounds_check(loc):
            # Apply the function and add/subtract from the current position
            locations.add(str(loc[0])+','+str(loc[1]))
            loc = func(loc,diff)
        else:
            oob = True

# Part 2 answer
check_antennas(check_location_many)
print(len(locations))



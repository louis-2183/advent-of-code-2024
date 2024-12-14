from collections import defaultdict
import numpy as np
from math import pi,sin,cos
from copy import deepcopy
import time

start_time = time.time()

######################## Part 1 ############################

data = [l[:-1] for l in open('input.txt')]

# Grid bounds
xmax,ymax = len(data),len(data[0])

# Work out the vectors of directions
directions = [[round(sin(a*(pi/2))),round(cos(a*(pi/2)))] for a in range(0,4)] 

# Lists of coords grouped by plant type
data_plants = defaultdict(list)

# Populate these lists
for y,line in enumerate(data):
    for x,char in enumerate(line):
        data_plants[char] += [[y,x]]
        
# Store coordinates that have already been checked
checked = defaultdict(list)

# For part 2, store positions that are bordering the plants
edges = defaultdict(list)
        
# For a specific plant type, goes through and checks for any neighbouring plants.
def process_plot(plant_type,pos):
    global area, perimeter
    # Since we are checking a plot of the same type, increase the area 
    area += 1
    # Add the plant we are checking, remove the same plant from the existing plants to check
    checked[plant_type] += [groups[plant_type].pop(groups[plant_type].index(pos))]
    # For each direction to follow
    for idx,d in enumerate(directions):
        # Calculate the new position based on the direction
        new_pos = list(np.add(pos,d))
        # If a neighbouring plot of the same plant type exists
        if new_pos in groups[plant_type]:
            # Check the neighbours of this one
            process_plot(plant_type,new_pos)
        elif new_pos not in checked[plant_type]:
            # If there is not a valid adjacent plot on this direction, we know to add to the perimeter
            perimeter += 1
            # Keep the position of the edge for later, according to where the edge is placed (U,D,L,R)
            edges[idx].append(tuple(new_pos))

score = 0
# For copying a dict of lists
groups = deepcopy(data_plants)

# For each type of plant
for plant_type in groups.keys():
    # Since we are eliminating as we go along checking the plots
    while len(groups[plant_type]) > 0:
        perimeter,area = 0,0
        edges.clear()
        # Only need to keep checked for a specific group 
        checked.clear()
        # Check the first remaining item in the groups of plants for all their neighbours and remove them
        # Since any groups of the same plant may not be neighbouring, the groups are separated
        process_plot(plant_type,groups[plant_type][0])
        # The perimeter and area of the specific group
        score += (perimeter*area)
        
print(score)
        
######################## Part 2 ############################
        
score = 0
# Re-copy
groups = deepcopy(data_plants)

# Variation of the previous code block using the different perimeter calculation
for plant_type in groups.keys():
    while len(groups[plant_type]) > 0:
        perimeter,area = 0,0
        edges.clear()
        checked.clear()
        process_plot(plant_type,groups[plant_type][0])
        
        # Discount perimeter
        perimeter_disc = 0
        
        # For each identified edge sitting on the same direction
        for direction in range(4):
            # Get whether we need to compare the X or Y axis
            axis = (direction % 2)
            # Sort the edges, since we want to be able to take the first item and increment to check if they are in a row
            edges_dir = sorted(edges[direction],key=lambda x: x[axis])
            # First item is the start position
            currpos = edges_dir[0]
            
            # Same approach as before, check for neighbouring edges on the same axis and eliminate to find groups
            while len(edges_dir) > 0:
                edges_dir.remove(currpos)
                # Get the new position of the edge based on the axis (which we sorted by)
                newpos = tuple(np.add(list(currpos),directions[(direction+1) % 2]))
                # If there is a neighbouring edge
                if newpos in edges_dir:
                    # Keep checking for further edges
                    currpos = newpos
                else:
                    # If not, we have run along one edge
                    perimeter_disc += 1
                    # If there are still any remaining, repeat the process for that one
                    if len(edges_dir) > 0:
                        currpos = edges_dir[0]

        # Increment price with the new perimeter
        score += (perimeter_disc*area)
        
# Part 2 answer
print(score)

###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")
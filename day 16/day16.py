import numpy as np

######################## Part 1 ############################

data = [l[:-1] for l in open('input.txt')]

# Define directions - starting East at 0th index
directions = [[0,1],[1,0],[0,-1],[-1,0]]
# Use the mod for cycling directions
to_dir = lambda x: x % 4

# Find starting position
for y,line in enumerate(data):
    for x,char in enumerate(line):
        if char == 'S':
            start_y,start_x = y,x
            
# Best scores along with traversed tiles
goals = [[1e9,[]]]

# List of items to perform BFS for (start y,start x, angle, steps taken, traversed tiles)
ls = [[start_y,start_x,0,0,[]]]

# Used to check if the position has been previously visited with fewer steps (eliminating bogus iterations)
visited = {}

# While we have positions to search
while len(ls) > 0:
    positions = []
    
    # Traverses and finds all branching locations for a given position
    for item in ls:
        # Fetch params from current item to traverse path with
        sy,sx,angle,steps,seen = item
        
        # If we have already visited this position with fewer steps, don't search any further
        if str(sy)+','+str(sx) in visited.keys():
           if visited[str(sy)+','+str(sx)] < steps:
                continue
        
        # Whether the position directly ahead is blocked
        blocked = False
        
        while blocked == False:
            # If end is reached, stop searching and record score + seen tiles for P2
            if data[sy][sx] == 'E':
                goals.append([steps,seen])
                blocked = True
            else:
                # Try the position in front
                ny,nx = np.add(directions[angle],[sy,sx])
                
                # Get positions turning 90 degrees either way 
                turn1,turn2 = np.add(directions[to_dir(angle-1)],[sy,sx]),np.add(directions[to_dir(angle+1)],[sy,sx])
                
                # If these are viable positions, store them for later recording the steps+1001 and seen tiles
                if data[turn1[0]][turn1[1]] == '.':
                    positions.append([turn1[0],turn1[1],to_dir(angle-1),steps+1001,seen+[tuple([turn1[0],turn1[1]])]])
                if data[turn2[0]][turn2[1]] == '.':
                    positions.append([turn2[0],turn2[1],to_dir(angle+1),steps+1001,seen+[tuple([turn2[0],turn2[1]])]])
                
                # If we cannot run forwards anymore, check the all tiles from the 90 degree turns we found instead
                if data[ny][nx] == '#':
                    blocked = True
                else:
                    # Move forward
                    steps += 1
                    visited[str(sy)+','+str(sx)] = steps
                    sy,sx = ny,nx
                    seen += [tuple([ny,nx])]
                    
    # If all linear paths are blocked, repeat with the found branching positions
    ls = positions.copy()
    
# Part 1 answer
print(min([v[0] for v in goals]))
    
######################## Part 2 ############################

# Unique tiles only
tiles = set()

# Goals stores first versions of best paths
for g in goals:
    # If the goal score = P1 answer, fetch the seen tiles from it and update the set (as it is tiles seen in one or more best paths)
    if g[0] == min([v[0] for v in goals]):
        tiles.update(g[1])

# Part 2 answer - adding one for the start position
print(len(tiles)+1)

############################################################

# Maybe use of a priority queue could speed it up a bit more
from functools import cache
from itertools import combinations
import numpy as np

######################## Part 1 ############################

data = [l[:-1] for l in open('input.txt')]

# Y,X coords of keypads and their related buttons
keypad = [[0,0,'7'],[0,1,'8'],[0,2,'9'],[1,0,'4'],[1,1,'5'],[1,2,'6'],[2,0,'1'],[2,1,'2'],[2,2,'3'],[3,1,'0'],[3,2,'A']]
dir_keypad = [[0,1,'^'],[0,2,'A'],[1,0,'<'],[1,1,'v'],[1,2,'>']]

# Directions of movement for the robot arms + associated instructions for a direction
directions = [[0,1],[1,0],[0,-1],[-1,0]]
instructions = ['>','v','<','^']

# Avoid 'robot panic' - check if a desired position to move to is on the keypad
def in_bounds(pos,t,k):
    if pos in [x[:2] for x in k] and pos not in [e[:2] for e in t]:
        return True
    return False

# Move out from a position and get all valid points to move to
def update_positions(p,t,k):
    n = [list(np.add(d,p)) for d in directions]
    out = []
    for idx,item in enumerate(n):
        # Check if in bounds for a specified keypad k
        if in_bounds(item,t,k):
            # Append instructions
            out.append(item+[instructions[idx]])
    return out

# Fetch all valid paths from start to end (or button to button)
def get_paths(sy,sx,ey,ex,k):
    validpaths = []

    # Positions to traverse from + already traversed positions
    positions = [[[sy,sx]]]
    # Branches available from the current path
    new_positions = []

    while len(positions) > 0:
        new_positions.clear()
        # While we still have paths to explore, take a step in any possible direction
        for p in positions:
            # Fetch the parameters for the given position record
            pos = p[-1][:2]
            traversed = p[:-1]
            # Take possible steps
            result = update_positions(pos,traversed,k)
            
            for r in result:
                # If the goal is reached, output instructions
                if r[:2] == [ey,ex]:
                    out = p+[r]
                    validpaths.append("".join([o[2] for o in out[1:]]))
                else:
                    # Take a step and add to traversed record
                    new_positions.append(p+[r])
        positions = new_positions.copy()

    # All valid paths
    return validpaths

# Fetch all the possible paths for all the button pairs on the keypad
def process_keypad(k):
    # Get button pairs
    comb = list(combinations(k,2))
    paths = {}
    
    # For pairs of buttons, get the possible paths and add to the dict
    for item1, item2 in comb:
        paths[str(item1[2])+'-'+str(item2[2])] = get_paths(*item1[:2],*item2[:2],k)
        paths[str(item2[2])+'-'+str(item1[2])] = get_paths(*item2[:2],*item1[:2],k)
        
    return paths

# Takes a list of strings and returns a list of strings which have the smallest length within it
def minlength(lis):
    minlen = min([len(x) for x in lis])
    return [l for l in lis if len(l) == minlen]

# Gets all keys needed a layer above from the code c using the specified path
def getkeys(c,paths):
    # Since the robot will always have to start from A in between inputs add it to the start
    code = 'A' + c   
    ls = []

    # If there is no movement required, the upper layer can just press A to input twice
    if code[0] == code[1]:
        items = ['A']
    else:
        # Get all shortest paths
        items = minlength(paths[code[0]+'-'+code[1]])
    
    for i in range(1,len(code)-1):    
        ls.clear()
        if code[i] == code[i+1]:
            for item in items:
                # Press A for no movement
                ls.extend([item + 'A'])            
        else:
            # Append the shortest paths for the next movement
            newitems = minlength(paths[code[i]+'-'+code[i+1]])
            for item in items:
                # Add A again for the separation
                ls.extend([item + 'A' + new for new in newitems])
        items = ls.copy()
        
    # All shortest paths along a variable amount of key presses
    return minlength([l + 'A' for l in items])

# This cache does most of the heavy lifting - redesigned for P2
@cache
def split_expand(val,rec,lim):
    # Limit the recursions to however many keypads we are controlling
    if rec == lim:
        return len(val)
    else:
        # In order to map these values efficiently, separate them by the A button
        splits = val[:-1].split('A')
        
        # Recursively get the sum of the shortest possible lengths of the next set (a layer up)
        cnt = 0
        for s in splits:
            # For each key path in between pressing A
            if s != "":
                # For all possible expansions, expand them to the limit, find the shortest key inputs of the shortest key inputs, ... 
                result = getkeys(s+'A',keypaths)
                o = [split_expand(r,rec+1,lim) for r in result]
                # Add them together
                cnt += min(o)
            else:
                cnt+=1
        
        return cnt
    
# Create dictionaries of all possible points of travel for the digit keypad and directional keypad
digitpaths = process_keypad(keypad)
keypaths = process_keypad(dir_keypad)

score = 0

# Store all min values for all possible paths from the digit pad, then stack 2 robots and get the min length for each code
for c in data:
    ls = []
    keys = getkeys(c,digitpaths)
    
    for k in keys:
        ls.append(split_expand(k,0,2))

    score += (int(c[:3]) * min(ls))
    
# Part 1 answer
print(score)

######################## Part 2 ############################

score = 0

# Store all min values for all possible paths from the digit pad, then stack 2 robots and get the min length for each code
for c in data:
    ls = []
    keys = getkeys(c,digitpaths)
    
    for k in keys:
        ls.append(split_expand(k,0,25))

    score += (int(c[:3]) * min(ls))
    
# Part 2 answer
print(score)

############################################################

# After redesigning split_expand(), it performs suprisingly well to me
# It was difficult to account for the shortest path possibly being a huge list of paths with the same length + processing every combination for every split action 
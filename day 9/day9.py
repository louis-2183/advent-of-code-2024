
######################## Part 1 ############################

data = open('input.txt').read()[:-1]

# Store expanded numbers
expanded = []

for i in range(0,len(data)):
    # Even entry = amount of digits for ID
    if i % 2 == 0:
        expanded += [int(i/2)] * int(data[i])
    # Odd = amount of spaces
    else:
        expanded += [None] * int(data[i])
        
def condense(ls):
    # Get indexes of numbers and spaces
    numbers,spaces = [i for i,x in enumerate(ls) if x is not None],[i for i,x in enumerate(ls) if x is None]

    # For every space, pop the last number and reassign its index to where the space was
    for space in spaces:
        value = numbers.pop()
        numbers.insert(space,value)
        
    # Index the numbers in the new order
    return [ls[number] for number in numbers]

# Expand the list and rearrange
ls = condense(expanded)

# Get the number multiplied by its index for the checksum
checksum = sum([idx * x for idx,x in enumerate(ls)])

# Part 1 answer
print(checksum)

######################## Part 2 ############################

# Expands a list of IDs/spaces and their associated counts
def expand(pos):
    expand = []
    for p in pos:
        # Append for the amount of times
        for i in range(p[1]):
            expand.append(p[0])
    return expand

# Counts all ID numbers and gaps from an expanded list
def minimise(ex):
    # Combined lengths of numbers and spaces
    ls = []
    
    # Blend all expanded positions and spaces together - accounting for multiple spaces / numbers in a row
    curr_item = 0
    tick = -1
    for item in ex:
        # If we are moving to a new item, restart the count
        if curr_item != item:
            ls.append([curr_item,tick+1])
            curr_item = item
            tick = 0
        else:
            tick+=1
    ls.append([curr_item,tick+1])
    return ls

# Tries to move the item ID of numid backward from the expanded list ex
def moveone(ex,numid):
    # Contracted list of ID/spaces and counts
    positions = minimise(ex)
    
    # Go backwards through the list of IDs while searching forwards for valid spaces
    for numidx,p in enumerate(reversed(positions)):
        # Find the ID we want to move
        if p[0] is not None and p[0] == numid:
            for spaceidx,s in enumerate(positions):
                # If we are not moving a given ID forwards
                if len(positions)-1-numidx > spaceidx:
                    if s[0] is None:
                        # If there is space to fit the item ID we want to move
                        if p[1] <= s[1]:                       
                            # Save the value we are moving
                            val = positions[len(positions)-1-numidx]
                            
                            # Set the moved value to a space
                            positions[len(positions)-1-numidx] = [None,val[1]]
                            
                            # Decrement the space left in the space moved to
                            positions[spaceidx] = [None,s[1] - p[1]]
                            
                            # Re-insert the ID to the left of the space
                            positions.insert(spaceidx,val)

                            # Re-expand the list (since new spaces could be formed in a row)
                            return expand(positions)
                        
    # This ID cannot be moved
    return ex

# IDs make up half of the initial data 
tick = int((len(data)-1)/2)

# Move one ID at a time decrementing from the last id (tick)
while tick > 0:
    # Try to move that ID
    expanded = moveone(expanded,tick)
    tick -= 1
        
# Get the checksum where spaces are not multiplied
checksum = sum([idx * x for idx,x in enumerate(expanded) if x is not None])

# Part 2 answer
print(checksum)

############################################################

# Part 2 could be improved - no need to iterate through the full lists
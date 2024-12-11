import time

#start_time = time.time()

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

# Not complete yet
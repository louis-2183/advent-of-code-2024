import numpy as np

######################## Part 1 ############################

# Read all grids
data = open('input.txt').read()[:-1].split('\n\n')
data = [line.split('\n') for line in data]

# Hold the list of int values for each lock and key
locks = []
keys = []

for item in data:
    # Int values of given lock/key
    ls = []
    # Locks
    if item[0].count('#') == len(item[0]):
        # Count present blocks column-wise ignoring first row
        for idx in range(0,len(item[0])):
            chars = [i[idx] for i in item[1:]]
            ls.append(chars.count('#'))
        locks.append(ls)
    # Keys
    else:
        # Count present blocks column-wise ignoring last row
        for idx in range(0,len(item[0])):
            chars = [i[idx] for i in item[:-1]]
            ls.append(chars.count('#'))
        keys.append(ls)
       
count = 0

# Try each key with every lock
for lidx,lock in enumerate(locks):
    for idx,key in enumerate(keys):
        # If the sum of key and lock values has a value bigger than 5, key does not fit
        if not any([x > 5 for x in np.add(lock,key)]):
            # If it does, this is a valid pair
            count+=1
           
# Part 1 answer
print(count)
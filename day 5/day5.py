import numpy as np
import time

start_time = time.time()

######################## Part 1 ############################

data = open('input.txt').read()[:-1].split("\n\n")

# Since file is split into rules, entries
rules = [x.split('|') for x in data[0].split('\n')]
entries = [x.split(',') for x in data[1].split('\n')]

# Keep bad items for part 2
bad_items = []

def check_items(items):
    for rule in rules:
        # If the rule is worth checking (it is in the entry)
        if rule[0] in items and rule[1] in items:
            # Check if the entries appear in the correct order
            if items.index(rule[0]) < items.index(rule[1]):
                # Correct, do nothing
                pass
            else:
                # Entry order is wrong
                return 0 
    # If all correct, return the middle number
    return int(items[round((len(items)-1)/2)])

score = 0

for entry in entries:
    # Check, check returns 0 if the entry is invalid
    check = check_items(entry)
    score += check  
    
    # If invalid save for part 2
    if check == 0:
        bad_items.append(entry)
            
# Part 1 answer
print(score)

######################## Part 2 ############################

# Convert to np array for in1d operation
rules = np.asarray(rules)
score = 0

# Rearranges invalid entries
def rearrange_line(l):
    # Dict containing keys of numbers mapping to unique sets of what comes after them
    rules_condensed = {}
    
    # Populate it, go through each unique predecessor
    for item in set([i[0] for i in rules]):
        # Get a set of any possible numbers that come after the number 
        rules_condensed[item] = set([x[1] for x in rules[np.in1d(rules[:, 0], item)] if x[1] in l])
    
    # Here is the hack - store the length of what comes after the predecessors
    # Since rules are by default defined for every item and we only store the appropriate ones, we don't need to sort using the rules. Just the length of the rules
    lens = []
    
    # Fetch lengths
    for item in l:
        lens.append(len(rules_condensed[item]))
        
    # Space for the newly arranged list
    finals = []
        
    i = 0
    while i < len(lens):
        # Loop up from 0 and sort, since the item with 0 items after it is the first so on, so forth
        finals.append(l[lens.index(i)])
        i+=1
        
    # Get the middle number
    return int(finals[round((len(finals)-1)/2)])
        
score = 0

# Fetch middle numbers of the rearranged sets of invalid entries
for bad in bad_items:
    score += rearrange_line(bad)
            
# Part 2 answer
print(score)

###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")

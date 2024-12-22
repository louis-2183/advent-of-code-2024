from math import floor
from functools import cache
import numpy as np
from collections import defaultdict

######################## Part 1 ############################

data = list(map(int,[l[:-1] for l in open('input.txt')]))

# Mix and prune operations
mix = lambda x,y: (x ^ y)
prune = lambda x: (x % 16777216)

# Mixes and prunes or something
@cache
def mix_prune(sec):   
    # 16777216 = '0b1000000000000000000000000', powers of 2 used also, there may be a better solution than this
    sec = prune(mix(sec,sec*64))
    sec = prune(mix(sec,floor(sec/32)))
    sec = prune(mix(sec,sec*2048))
    return sec
    
count = 0

for num in data:
    # Perform the operation 2000 times
    for i in range(2000):
        num = mix_prune(num)
    count += num

# Part 1 answer
print(count)
    
######################## Part 2 ############################

# List of the first unique instances of patterns, with the collective amounts of bananas won
sums = defaultdict(int)

for num in data:
    # Get the last digit of the starting number as the first price
    prices = [int(str(num)[-1])]
    
    # Perform the operations while storing the price in a separate list
    for i in range(2000):
        num = mix_prune(num)
        prices.append(int(str(num)[-1]))
       
    # Difference between them all
    diffs = np.diff(prices)

    # Stack this into a 4 period rolling window, and also store the price associated with selling at this window
    rolling = list(zip(map(str,zip(diffs,diffs[1:],diffs[2:],diffs[3:])),prices[4:]))
    
    # Since the monkey will only sell at the 1st occurrence, refer to this list to ensure only the 1st is stored
    checked = []

    for result in rolling:
        # Checks for a first occurrence only
        if result[0] not in checked:
            # Add to the collective amounts of bananas, using the pattern as a key
            sums[result[0]] += result[1]
            checked.append(result[0])
            
# Part 2 answer
print(max(sums.values()))

############################################################

# There may be some bit hacks I have left out(?), but this one was very fun

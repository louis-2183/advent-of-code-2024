from functools import cache
from collections import defaultdict
import time

start_time = time.time()

######################## Part 2 ############################

file = open('input.txt').read()[:-1].split(" ")

# Remove leading zeros from a numerical string
no_zero = lambda x: str(int(x)) 

# Processes a single stone, returns a list of created stones. 
# Cache in an effort to catch repeated inputs
@cache
def func(stone):
    length = len(stone)
    
    # Rule 1 - If it is zero, make it 1
    if int(stone) == 0:
        return ["1"]
    
    # Rule 2 - Split if there is an even length of digits
    elif length % 2 == 0:
        return [
            no_zero(stone[:int(length/2)]), # First stone 
            no_zero(stone[-int(length/2):]) # Second stone
        ]
    
    # Otherwise multiply by 2024
    return [str(int(stone)*2024)]
    
# Create a dict holding each value and the amount of occurrences 
current_stones = defaultdict(int)
for f in file:
    current_stones[f] += 1
    
# Blink a set amount of times
for i in range(75):
    # Create another dict to hold values after the blink
    new_stones = defaultdict(int)
    
    # Go through the unique stones in the blink
    for item in current_stones.keys():
        
        # Process the item
        processed = func(item)
        
        # For the amount of stones we have, increment unique values for the new dict 
        for p in processed:
            
            # Multiply by the amount of stones we 'processed'
            new_stones[p] += 1 * current_stones[item]
    
    current_stones = new_stones.copy()
    
# Part 2 answer - the sum of the amounts of unique stones from the dict
print(sum(current_stones.values()))

###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")

# 1000 iterations in 2.19s
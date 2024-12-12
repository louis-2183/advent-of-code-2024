from functools import cache

######################## Part 1 ############################

data = open('input.txt').read()[:-1]

# Remove leading zeros from a numerical string
no_zero = lambda x: str(int(x)) 

# Processes a single stone, returns a string of created stones
# Cache in an effort to catch repeated inputs
@cache
def applyrules(stone):
    length = len(stone)
    
    # Rule 1 - If it is zero, make it 1
    if int(stone) == 0:
        return "1"
    
    # Rule 2 - Split if there is an even length of digits
    elif length % 2 == 0:
        return no_zero(stone[:int(length/2)]) + " " + no_zero(stone[-int(length/2):])
    
    # Otherwise multiply by 2024
    return str(int(stone)*2024)
    
# Processes a full blink for each stone in the current timeframe
def blink(stones):
    line = ""
    
    # Go through each stone applying the rules
    for stone in stones.split(" "):
        
        # Add result string to a line, with a space to separate stones
        line += applyrules(stone) + " "
    
    return line[:-1]

# Blink 25 times
for i in range(25):
    data = blink(data)
    
# Part 1 answer
all_stones = data.split(" ")
print(len(all_stones))

######################## Part 2 ############################

# Cannot process 75 blinks this way! Script has been revised in day11_pt2.py


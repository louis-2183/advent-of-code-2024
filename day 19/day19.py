from functools import cache
import time

start_time = time.time()

######################## Part 1 ############################

data = open('input.txt').read()[:-1].split('\n\n')
towels,designs = data[0].split(', '),data[1].split('\n')
towels = sorted(towels,key=lambda x: len(x),reverse=True)

score = 0

# Checks a given design and iteratively removes towels, removing them where applicable.
# Caching speeds this up a lot, as we will be processing lots of similar designs once towels start getting removed
@cache
def check_design(design):
    # If we have removed all towels from a single design it is valid
    if len(design) == 0:
        return 1
    
    # If we are able to remove any combinations of towel and get a length of 0 it is a possible design
    return any([check_design(design.removeprefix(x)) for x in towels if design.startswith(x)])

# Check all designs for combinations of towels
for des in designs:
    score += check_design(des)
    
# Part 1 answer
print(score)
    
######################## Part 2 ############################

# Same idea. Just getting a sum() of all possible designs instead of any()

score = 0

@cache
def check_design_all(design):
    if len(design) == 0:
        return 1
    
    # Sum the validities of the combinations instead
    return sum([check_design_all(design.removeprefix(x)) for x in towels if design.startswith(x)])

# Check all designs for combinations of towels
for des in designs:
    score += check_design_all(des)
    
# Part 2 answer
print(score)

############################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")
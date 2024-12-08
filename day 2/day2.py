import time

start_time = time.time()

######################## Part 1 ############################

data = [list(map(int,l.split())) for l in open('input.txt')]

# Function for whether change in pair meets condition (1<=x<=3) 
diff = lambda x,y: 1 <= abs(x - y) <= 3

def check_line(ls):
    # Condition for whether the a pair of ints increase or decrease
    increasing = ls[0] < ls[1]
    
    # Scan every pair we haven't scanned with an established increase/decrease
    for idx,item in enumerate(ls[:-1]):
        # Define boolean for whether we are still increasing/decreasing
        condition = ls[idx] < ls[idx+1]
        
        # If it's the opposite or we are not changing within constraints, break
        if (condition != increasing) or not diff(ls[idx],ls[idx+1]):
            return 0
        
    return 1

score = sum([check_line(line) for line in data])
        
# Part 1 answer
print(score)

######################## Part 2 ############################

def check_removing(l):
    # Not the best possible method. Creating a list of checks, removing (and iterating over) items to switch out
    checks_valid = []

    # Loop through items
    for idx,item in enumerate(l):
        # Take out the item in current position, check everything else
        checks_valid.append(check_line(l[:idx]+l[idx+1:]))

    # If no checks valid, more than 1 bad item exists
    return any(checks_valid)

score = sum([check_removing(line) for line in data])
        
# Part 2 answer
print(score)

###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")

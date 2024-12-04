
######################## Part 1 ############################

# Function for whether change in pair meets condition (1<=x<=3) 
diff = lambda x,y: 1 <= abs(x - y) <= 3

def check_line(line_str):
    # Convert our digits to integers
    ls = [int(x) for x in line_str]
    
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
        
score = 0

# Open the file
with open('input.txt', 'r') as file:
    # Read each line into an array
    for line in file:
        l = line.replace('\n','').split(' ')
        
        score += check_line(l)
        
# Part 1 answer
print(score)

######################## Part 2 ############################

score = 0

def check_removing(l):
    # Not the best possible method. Creating a list of checks, removing (and iterating over) items to switch out
    checks_valid = []

    # Loop through items
    for idx,item in enumerate(l):
        # Take out the item in current position, check everything else
        checks_valid.append(check_line(l[:idx]+l[idx+1:]))

    # If no checks valid, more than 1 bad item exists
    return (sum(checks_valid) > 0)

# Open the file
with open('input.txt', 'r') as file:
    # Read each line into an array
    for line in file:
        l = line.replace('\n','').split(' ')
        
        score += check_removing(l)
        
# Part 2 answer
print(score)

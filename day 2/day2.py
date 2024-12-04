
######################## Part 1 ############################

# Function for whether change in pair meets condition (1<=x<=3) 
diff = lambda x,y: 1 <= abs(x - y) <= 3

def check_line(line_str):
    # Convert our digits to integers
    ls = [int(x) for x in line_str]
    
    # Condition for whether the a pair of ints increase or decrease
    increasing = ls[0] < ls[1]
    
    # Scan every pair we need to with an established increase/decrease
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
        

import re
import time

start_time = time.time()

######################## Part 1 ############################

data = open('input.txt').read()[:-1].split('\n\n')

def attempt_game(ax,ay,bx,by,gx,gy):
    # Simultaneous equations - solve for a    
    a = (((gx*by)+(gy*(-bx)))/((ax*by)+(ay*(-bx))))
    
    # Button presses have to be a whole number to be valid. 
    # If we do not have a whole number the game cannot be won
    if a % 1 == 0:
        # Solve for b in terms of a
        b = (gx-(a*ax))/bx
        
        # Return the amount of tokens
        return ((3*a)+b)
    
    return 0

score = 0

for idx,line in enumerate(data):
    # Remove everything that's not a digit
    clean = re.sub(r'\D+',' ',line)[1:]
    
    # Attempt a game with the parameters
    score += attempt_game(*list(map(int,clean.split(' '))))
    
# Part 1 answer
print(score)
        
######################## Part 2 ############################

score = 0

for idx,line in enumerate(data):
    # Remove everything that's not a digit
    clean = re.sub(r'\D+',' ',line)[1:]
    
    items = list(map(int,clean.split(' ')))
    # Add 10 trillion to the last 2 numbers
    correct_format = items[:-2]+[1e13 + x for x in items[-2:]]
    
    score += attempt_game(*correct_format)
    
# Part 2 answer
print(score)

############################################################

# Vindication!!!! O(1)

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")

import re
import math

######################## Part 1 ############################

score = 0

# Open the file
with open('input.txt', 'r') as file:
    # Read each line into an array
    for line in file:
        # Gets all mul(N,N)
        muls = re.findall(r'(mul\([0-9]+,[0-9]+\))', line)
        
        for item in muls:
            # Straight into a tuple.. :D
            nums = eval(item.replace("mul",""))
            
            # Multiply the two numbers
            score += math.prod(nums)
            
# Part 1 answer
print(score)
        
######################## Part 2 ############################

score2 = 0

# Open the file
with open('input.txt', 'r') as file:
    do = True
    
    # Read each line into an array
    for line in file:
        # Gets all muls(N,N), do()s and don't()s
        muls = re.findall(r'(mul\([0-9]+,[0-9]+\))|(do\(\))|(don\'t\(\))', line)
        
        for item in muls:
            # Toggle whether we have to increment the score
            if item[1] == "do()":
                do = True
                continue
            if item[2] == "don't()":
                do = False
                
            # If we are under a don't() instruction
            if not do:
                continue
            
            # Straight into a tuple
            nums = eval(item[0].replace("mul",""))
            
            # Multiply the two numbers
            score2 += math.prod(nums)
            
# Part 2 answer
print(score2)
            
        
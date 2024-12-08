import re
import math
import time

start_time = time.time()

######################## Part 1 ############################

data = open('input.txt').read()[:-1].replace('\n',' ')

score = 0

# Gets all mul(N,N)
muls = re.findall(r'(mul\([0-9]+,[0-9]+\))', data)
        
for item in muls:
    # Straight into a tuple and multiply.. :D
    score += math.prod(eval(item.replace("mul","")))
            
# Part 1 answer
print(score)
        
######################## Part 2 ############################

score2 = 0

# Gets all muls(N,N), do()s and don't()s
muls = re.findall(r'(mul\([0-9]+,[0-9]+\))|(do\(\))|(don\'t\(\))', data)

do = True 

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
    
    # Straight into a tuple and multiply
    score2 += math.prod(eval(item[0].replace("mul","")))
            
# Part 2 answer
print(score2)
            
###########################################################

end_time = time.time()
print(f"Time elapsed: {end_time-start_time}s")
        

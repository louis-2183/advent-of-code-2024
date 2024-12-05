
######################## Part 1 ############################

# File straight to array
data = [l[:-1] for l in open('input.txt')]

score = 0

# Define word to iterate across
word = 'XMAS'

# Define axes increments/max boundaries
yaxis, xaxis = list(range(0,len(data))), list(range(0,len(data[0])))
ymax, xmax = max(yaxis), max(xaxis)

# Bounds check for the grid
within_bounds = lambda x,y: (0 <= x <= xmax) and (0 <= y <= ymax)

# Checks a point on the wordsearch for neighbouring additional characters. 
# Takes a vector if direction has been established (needed for X -> M only)
def check_surrounding(xpos,ypos,c,vec):
    global score
    
    # If we are looking for the direction X goes out from
    if vec == None:
        # Lower/upper boundaries of wordsearch to check
        xlb, ylb = max(xpos-1,0), max(ypos-1,0)
        xub, yub = min(xpos+1,xmax)+1, min(ypos+1,ymax)+1        
        
        # For each item we need to check on the ~3x3 grid
        for y in range(ylb,yub):
            for x in range(xlb,xub):
                # If the character we are on is a continuation
                if data[y][x] == word[c+1]:
                    # Establish vector 
                    v = [y-ypos,x-xpos]
                    
                    # Check the tile with our vector in place
                    check_surrounding(x,y,c+1,vec=v)
    
    # If we know the direction
    else:
        # Immediately fetch next position along the direction
        newx, newy = xpos+vec[1], ypos+vec[0]
        
        # If it would not be going out of bounds
        if within_bounds(newx,newy):
            # Continuation found
            if data[newy][newx] == word[c+1]:
                # Full word is found
                if word[c+1] == 'S':
                    score += 1
                else:
                    # Otherwise, keep going
                    check_surrounding(newx,newy,c+1,vec=vec)     

# Loop and check for any Xs to start the function
for y in yaxis:
    for x in xaxis:
        if data[y][x] == 'X':
            check_surrounding(x,y,0,None)
            
# Part 1 answer
print(score)
            
######################## Part 2 ############################

score = 0

def check_surrounding_xmas(xpos,ypos):
    # Get the corners, since if they are both sets of M and S then it is a valid X-MAS 
    diag1 = set([data[ypos+1][xpos+1],data[ypos-1][xpos-1]])
    diag2 = set([data[ypos-1][xpos+1],data[ypos+1][xpos-1]])
    
    # Are both sets spelling out the X-MAS
    return (diag1 == {'M','S'}) and (diag2 == {'M','S'})
    
# Loop and check for any As to start the function this time (where they would be valid to count)
for y in yaxis[1:-1]:
    for x in xaxis[1:-1]:
        if data[y][x] == 'A':
            score += check_surrounding_xmas(x,y)
            
# Part 2 answer
print(score)

         

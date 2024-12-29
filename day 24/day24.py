######################## Part 1 ############################

data = open('input.txt').read()[:-1].split('\n\n')

# Split data into initial X+Y values and the values to find
values,equations = [part.split('\n') for part in data]

# Split the words of operations into their symbols so an eval() can be performed on them
operations = {'AND':' & ','OR':' | ','XOR':' ^ '}

# Runs through the values and updates until the Z gates have all been populated
def compute(vals,eq):
    lookup = {}

    # Set the initial x and y values for the mappings
    for v in vals:
        key, val = v.split(': ')
        lookup[key] = val
    
    # While there are still missing entries
    while len(lookup) < len(vals) + len(eq):
        for e in eq:
            # Get the values we need from the line
            key1,op,key2,ans = e.replace('-> ','').split(' ')
            
            if key1 in lookup.keys() and key2 in lookup.keys():
                # If we know what both keys are we can calculate the value of the answer key
                lookup[ans] = str(eval(lookup[key1] + operations[op] + lookup[key2]))
    
    # Sort all z values
    zvalues = sorted([l for l in lookup.keys() if 'z' in l])
    
    # Get the reversed binary representation
    sumz = "".join(reversed([lookup[v] for v in zvalues]))
    return sumz

result = compute(values,equations)

# Part 1 answer - binary of Z gates
print(int(result,base=2))

######################## Part 2 ############################

# Gates which need to be swapped
wrong = set()
lastz = sorted([e[-3:] for e in equations if e[-3] == 'z'],reverse=True)[0]

# We don't need to calculate the actual sum of X and Y. This answer is a bit implicit - the gates make up a Ripple Carry Adder
# So we can look at the gates which compose the final Z values instead

# Slight variation of the above function - but also finds the wrong gates throughout the calculation
def compute_findwrong(vals,eq):
    lookup = {}

    for v in vals:
        key, val = v.split(': ')
        lookup[key] = val
    
    while len(lookup) < len(vals) + len(eq):
        for e in eq:
            key1,op,key2,ans = e.replace('-> ','').split(' ')
            
            # Z gate results should always come from a XOR apart from the last one
            if ans[0] == 'z' and op != 'XOR' and ans != lastz:
                wrong.add(ans)
            
            # XORs are always associated with at least one input/output gate
            if op == "XOR" and (key1[0] not in 'xyz' and key2[0] not in 'xyz' and ans[0] not in 'xyz'):
                wrong.add(ans)
                
            # For ANDs, check all other gates to see if an AND or XOR is performed with the current result
            if op == "AND" and (key1 != 'x00' and key2 != 'x00'):
                for sube in eq:
                    subkey1,subop,subkey2,subans = sube.replace('-> ','').split(' ')
                    if (ans == subkey1 or ans == subkey2) and subop != "OR":
                        wrong.add(ans)
                  
            # For XORs, check all other gates to see if an OR is performed with the current result
            if op == "XOR":
                for sube in eq:
                    subkey1,subop,subkey2,subans = sube.replace('-> ','').split(' ')
                    if (ans == subkey1 or ans == subkey2) and subop == "OR":
                        wrong.add(ans)
            
            if key1 in lookup.keys() and key2 in lookup.keys():
                lookup[ans] = str(eval(lookup[key1] + operations[op] + lookup[key2]))
                
    zvalues = sorted([l for l in lookup.keys() if 'z' in l])
    sumz = "".join(reversed([lookup[v] for v in zvalues]))
    return sumz

compute_findwrong(values,equations)

# Part 2 answer - all wrong gates, no pair checks needed 
print(",".join(sorted(wrong)))

############################################################
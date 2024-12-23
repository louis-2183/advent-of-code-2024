from collections import defaultdict, Counter
from itertools import chain

data = [l[:-1].split('-') for l in open('input.txt')]

# List of unique computers in the data
computers = set(list(chain(*data)))

# Stores the 1st jump of connections for a given computer
connections = defaultdict(list)

# Fetch the connections from the pairs of computers
for pair in data:
    connections[pair[0]] += [pair[1]]
    connections[pair[1]] += [pair[0]] 
    
# Stores the unique triplets of connected computers
final = []

# Check the main computer (where it starts with t)
for main in [c for c in computers if c[0] == 't']:
    # Gets the connections associated with this main computer
    con = connections[main]
    
    for c in con:
        # Get the connections of the main computer's connections
        others = connections[c].copy()
        
        # Remove the label of the main computer since we know it is connected
        others.remove(main)
        
        for o in others:
            if o in con:
                # Create the triplet - If the connections share another computer, sort them to dedupe 
                result = sorted([o,c,main])
                
                # If this doesn't result in duplication, it is a valid combo
                if result not in final:
                    final.append(result)
                    
# Part 1 answer
print(len(final))

##########################################################

scores = {}

# Fetches amounts of similar connections between connections from a given computer
for main in computers:
    # Stores all connections from the connections of a single computer
    ls = []
    
    # Get connections of the main computer
    con = connections[main]
    
    # Get the connections of the main computer's connections, plus the resulting connections of those
    ls.append(con)
    for c in con:
        ls.append(connections[c] + [c])
    
    # The more computers shared between these lists, the more people are in the LAN party
    occurrences = list(chain(*ls))
    c = Counter(occurrences)
    
    # Get the highest amount of connected computers along with their IDs
    newlabel = sorted([key for key in c.keys() if c[key] == max(c.values())])
    
    # Assign this set of computers to a score, indicating how many other computers share this network
    scores[",".join(newlabel)] = len(newlabel)
    
# Part 2 answer - the group of computers with the most shared connections
print([key for key in scores.keys() if scores[key] == max(scores.values())])
from itertools import combinations, permutations
from functools import cache
import numpy as np
from collections import defaultdict, Counter

#
# WIP - Part 2 answer needs a counter
#

data = [l[:-1] for l in open('input.txt')]

keypad = [
    [0,0,'7'],[0,1,'8'],[0,2,'9'],
    [1,0,'4'],[1,1,'5'],[1,2,'6'],
    [2,0,'1'],[2,1,'2'],[2,2,'3'],
              [3,1,'0'],[3,2,'A']
]

dir_keypad = [
              [0,1,'^'],[0,2,'A'],
    [1,0,'<'],[1,1,'v'],[1,2,'>']
]

comb = list(combinations(keypad,2))

directions = [[0,1],[1,0],[0,-1],[-1,0]]
instructions = ['>','v','<','^']

def in_bounds(pos,t,k):
    if pos in [x[:2] for x in k]:
        if pos not in [e[:2] for e in t]:
            return True
    return False

def update_positions(p,t,k):
    n = [list(np.add(d,p)) for d in directions]
    out = []
    for idx,item in enumerate(n):
        if in_bounds(item,t,k):
            out.append(item+[instructions[idx]])
    return out

def get_paths(sy,sx,ey,ex,k):
    validpaths = []

    positions = [[[sy,sx]]]
    new_positions = []

    while len(positions) > 0:
        new_positions.clear()
        for i in positions:
            pos = i[-1][:2]
            
            traversed = i[:-1]
            
            result = update_positions(pos,traversed,k)
            
            for r in result:
                if r[:2] == [ey,ex]:
                    out = i+[r]
                    validpaths.append("".join([o[2] for o in out[1:]]))
                else:
                    new_positions.append(i+[r])
        positions = new_positions.copy()

    return validpaths

def process_keypad(k):
    comb = list(combinations(k,2))
    paths = {}
    
    for item1, item2 in comb:
        paths[str(item1[2])+'-'+str(item2[2])] = get_paths(*item1[:2],*item2[:2],k)
        paths[str(item2[2])+'-'+str(item1[2])] = get_paths(*item2[:2],*item1[:2],k)
        
    return paths

def digitcombs(c,path):
    code = "A"+c   
    ls = []
    items = minlength(path[code[0]+'-'+code[1]])
    
    for i in range(1,len(code)-1):    
        ls.clear()
        if code[i] == code[i+1]:
            for item in items:
                ls.extend([item + 'A'])            
        else:
            newitems = minlength(path[code[i]+'-'+code[i+1]])
            for item in items:
               ls.extend([item + 'A' + new for new in newitems])
        items = ls.copy()
    return [l + 'A' for l in items]

def minlength(lis):
    minlen = min([len(x) for x in lis])
    return [l for l in lis if len(l) == minlen]

def sim_keypad(c,times):
    poss = minlength(digitcombs(c,digitpaths))
    
    for i in range(times):
        sets = []
        
        for p in poss:
            newposs = minlength(digitcombs(p,keypaths))
            for n in newposs:
                sets.append(n) 
                
        poss = minlength(sets)
    
    return poss

digitpaths = process_keypad(keypad)
keypaths = process_keypad(dir_keypad)

all_codes = data
score = 0

"""all_codes = ['029A',
'980A',
'179A',
'456A',
'379A']"""

for cod in all_codes:

    poss = sim_keypad(cod,2)
    m = min([len(p) for p in poss])
    
    score += int(cod[:-1]) * m
    

import re

######################## Part 1 ############################

data = open('input.txt').read()
rega,regb,regc,*program = map(int,re.sub(r'\D+',' ',data[:-1]).split(" ")[1:])

# Collects outputs for a given input
def try_program(rega,regb,regc,program):
    # Instruction pointer
    instr = 0
    # List of all outputs from the program
    outputs = []
    
    # Interpret a given opcode and operand from the instruction pointer i
    def interpret(i,op,l,ra,rb,rc):
        # Map literal operands to combo operands 
        combo_map = {0:0,1:1,2:2,3:3,4:rega,5:regb,6:regc}
        c = combo_map[l]
        
        # Decides the operation to do
        match op:
            case 0: ra = ra >> c              # ADV - Equivalent to floor(register / 2**(c))
            case 1: rb = rb ^ l               # BXL
            case 2: rb = c % 8                # BST
            case 3: i = l-2 if ra != 0 else i # JNZ
            case 4: rb = rb ^ rc              # BXC
            case 5: outputs.append(c % 8)     # OUT
            case 6: rb = ra >> c              # BDV
            case 7: rc = ra >> c              # CDV
        return i,ra,rb,rc
    
    # Go through the program moving the instruction pointer
    while instr < len(program):
        # Fetch opcode/operand
        opcode,lit_operand = program[instr:instr+2]
        # Perform the current instruction
        instr,rega,regb,regc = interpret(instr,opcode,lit_operand,rega,regb,regc)
        instr += 2
        
    return outputs
        
# Outputs of the initial program
goal = try_program(rega,regb,regc,program)
ans = ",".join(map(str,goal))
print(ans)

######################## Part 2 ############################

# Hold the values within the current layer of recursive checks
lowest = []

# Recursively check reg A (val) in multiples of 8, since outputs are % 8
def check(val,inc):
    result = try_program(val,0,0,program)
    
    # Matching reg A value has been found
    if result == program:
        # Since there could be multiple values found, get the lowest at the end
        lowest.append(val)    
        
    # If the bits on register A are matching for part of the solution
    if result == program[-inc:] or inc == 0:
        for i in range(8):
            # Check the multiples of 8 for this one with the incremented check criteria
            check(8*val+i,inc+1)

check(0, 0)

# Part 2 answer
print(min(lowest))

############################################################
instructions = open("challenge.bin", "rb").read()

newInstr = []
for i in range(0, len(instructions), 2):
    p1 = bin(instructions[i+1])
    p2 = bin(instructions[i])[2:]
    p2 = "0" * (8-len(p2)) + p2
    
    n = int(p1 + p2, 2)
    
    newInstr.append(n)
instructions = newInstr

                
registers = [0] * 8
address = 0
stack = []

from save import *

def get(address):
    val = instructions[address]
    if val < 32768:
        return val
    return registers[val - 32768]

def set(address, value):
    if instructions[address] >= 32768:
        #print(instructions[address])
        registers[instructions[address] - 32768] = value
    else:
        instructions[address] = value

for i in range(5489, 5498):
    instructions[i] = 21

def save():
    with open("save.py", "w") as f:
        f.write("registers = "+str( registers))
        f.write("\naddress = "+str( address))
        f.write("\ninstructions = "+str( instructions))
        f.write("\nstack="+str( stack))

def reset():
    with open("save.py", "w") as f:
        pass
    
def load():
    swapLoad = False
##    from save import address
##    from save import instructions
##    from save import registers
##    from save import stack
    
    global address, instructions, registers, stack
    read = ""
    i = 0
    while True:
        
        instr = instructions[address]
        if swapLoad and 6000 < address < 6500:
            
            print(address, instr, instructions[address+1], registers, stack)
        #print(instr)
        i+=1
        if instr == 0:
            break
        elif instr == 1:
            set(address + 1, get(address + 2))
            address +=3
            
        elif instr == 2:
            value = get(address + 1)
            
            stack.append(value)
            address += 2

        elif instr == 3:
            assert(len(stack) > 0)
            set(address + 1, stack.pop())
            address += 2

        elif instr == 4:
            b = get(address + 2)
            c = get(address + 3)
            if b == c:
                set(address + 1, 1)
            else:
                set(address + 1, 0)
            address +=4
            
        elif instr == 5:
            b = get(address + 2)
            c = get(address + 3)
            if b > c:
                set(address + 1, 1)
            else:
                set(address + 1, 0)
            address +=4
            
        elif instr == 6:
            address = get(address + 1)
            
        elif instr == 7:
            a = get(address + 1)
            if a != 0:
                address = get(address + 2)
            else:
                address += 3

        elif instr == 8:
            a = get(address + 1)
            if a == 0:
                address = get(address + 2)
            else:
                address += 3

        elif instr == 9:
            b = get(address + 2)
            c = get(address + 3)
            set(address + 1, (b + c) % 32768)
            address += 4
            
        elif instr == 10:
            b = get(address + 2)
            c = get(address + 3)
            set(address + 1, (b * c) % 32768)
            address += 4
            
        elif instr == 11:
            b = get(address + 2)
            c = get(address + 3)
            set(address + 1, (b % c) % 32768)
            address += 4

        elif instr == 12:
            b = get(address + 2)
            c = get(address + 3)
            set(address + 1, (b & c) % 32768)
            address += 4

        elif instr == 13:
            b = get(address + 2)
            c = get(address + 3)
            set(address + 1, (b | c) % 32768)
            address += 4

        elif instr == 14:
            b = get(address + 2)
            set(address + 1, (~b) % 32768)
            address += 3

        elif instr == 15:
            #print("rmem")
            set(address +1, instructions[get(address+2)])
            address += 3

        elif instr == 16:
            #print("wmem")
            b = get(address + 2)
            a = get(address + 1)
            toPrint = str(b)

            if swapLoad:
                if 64 < b < 128:
                    toPrint += " (" + chr(b) + ")"
                print("writing ", toPrint, " to address ", a)
            
            instructions[a] = b
            address += 3

        elif instr == 17:
            stack.append(address + 2)
            address = get(address + 1)

        elif instr == 18:
            if len(stack) == 0:
                break
            address = stack.pop()
            if swapLoad:
                print("returning to " + str(address))
            
            
        elif instr == 19:
            print(chr(get(address + 1)), end = "")
            address += 2

        elif instr == 20:
            if read == "":
                read = input()
                #print(read[:5])
                if read == "print":
                    print("stack: ", stack)
                    print("registers: ", registers)
                    print("address: ", address)
                    read = input()
                if read[:5] == "write":
                    v = read.split(" ")
                    if v[1] == "reg":
                        registers[int(v[2])] = int(v[3])
                    if v[1] == "add":
                        instructions[int(v[2])] = int(v[3])
                    read = input()
                if read == "swapLoad":
                    swapLoad = not swapLoad
                    read = input()
                    
                read += "\n"
                
            set(address + 1, ord(read[0]))
            read = read[1:]
            address += 2
            
        elif instr == 21:
            address += 1
        else:
            print("unimplemented instruction error: ", instr)
            break

load()
#_ + _ * _^2 + _^3 - _ = 399      
    
#5. ZwLmZgLCNEzW
# red - 2
# shiny - 5
# corroded - 3
# concave - 7
# blue - 9
 # blue, red, shiny, concave, corroded

#6. NMYcHLveqGZd


r7 = 3
def call(r0, r1):
    if r0 == 0:
        r0 = r1 + 1
        return [r0, r1]
    if r1 == 0:
        r0 -= 1
        r1 = r7
        return call(r0, r1)
    temp = r0
    r1 -= 1
    r0, r1 = call(r0, r1)
    r1 = r0
    r0 = temp
    r0 -= 1
    return call(r0, r1)

#from functools import cache
import sys
import math
sys.setrecursionlimit(33000)

def sumTriangle(n):
    if n == 0:
        return ((1,3,1),(1,2,1))
    current, adds = sumTriangle(n-1)
    current = list(current)
    adds = list(adds)
    
    current.insert(0, 0)
    newAdds = [0] * (len(adds) + 1)
    newAdds[0] = 1
    newAdds[-1] = 1
    for i in range(1, len(adds)):
        newAdds[i] = adds[i-1] + adds[i]

    for i in range(len(newAdds)):
        current[i] += newAdds[i]
        
    return (tuple(current), tuple(newAdds))

def getCoefficients(n):
    v = [1,3,1]
    for row in range(3,n+3):
        v.insert(0,0)
        for col in range(row + 1):
            v[row - col] += math.comb(row, col)
    return v

def call(r0, r1):
    if r0 == 1:
        return r7 + r1 + 1
    if r0 == 2:
        return ((r1 + 2) * r7 + r1 + 1) % 32767
    if r0 == 3:
        coefficients = getCoefficients(r1)[::-1]
        total = 0
        for i in range(len(coefficients)):
            total += coefficients[i] * pow(r7, i, 32767)
        return total % 32767
        
    if r1 == 0:
        return call(r0-2, call(r0-1, r7-1))
    
    return call(r0 - 1, call(r0,r1-1) % 32767) % 32767

    
    #print(r0, r1)
    while r0 != 0:
        
        if r1 == 0:
            r0 -= 1
            r1 = r7
            continue
        
        r1 -= 1

        #print("calling with ", r0, r1)
        r1 = call(r0, r1)
        #print("got result", r0, r1)
        
        r0 -= 1
    return r1 + 1

#r0 has to be 6 at the end of this?
#32775 is the interesting register

#1 - 4,1
#5 - 4,1

#
# for i in range(430,32767):
#     r7 = i
#     c = call(4,0)
#
#
#     if c > 1000:
#         #print("skipping", i)
#         continue
#     c = call(4,1)
#     print("i: ", i, "call(4,1)", c)
#     if c == 6:
#         print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#
    

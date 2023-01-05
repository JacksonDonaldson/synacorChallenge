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


#_ + _ * _^2 + _^3 - _ = 399      
    
#5. ZwLmZgLCNEzW
# red - 2
# shiny - 5
# corroded - 3
# concave - 7
# blue - 9
 # blue, red, shiny, concave, corroded

#6. NMYcHLveqGZd

def call(r0, r1):
    if r0 == 0:
        r0 = r1 + 1
        return
    if r1 == 0:
        r0 -= 1
        r1 = 32775
        call(r0,r1)
        return
    stack.append(r0)
    r1-=1
    call(r0,r1)
    r1 = r0
    r0 = stack.pop()
    r0 = r0-1
    call(r0,r1)
    return
#r0 has to be 6 at the end of this?
#32775 is the interesting register

#1 - 4,1
#5 - 4,1

    

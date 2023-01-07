import jcksn

grid = [
    ["*", "8", "-", "1"],
    ["4", "*", "11", "*"],
    ["+", "4", "-", "18"],
    ["22", "-", "9", "*"]
    ]

class Position:
    def __init__(self, r, c, value, locations):
        self.r = r
        self.c = c
        self.value = value + grid[r][c]
        #print(self.value)
        self.locations = locations + [(r,c)]

    def move(self, direction):
        return Position(self.r + direction[0], self.c + direction[1], self.value, self.locations)
    
    def eval(self):
        try:
            v = eval(self.value)
            self.value = str(v)
            #print(self.value)
            return int(self.value)
        except:
            return 0
    
positions = [Position(3, 0, "", [])]

depth = 0
while True:
    
    depth+=1
    print(f"{depth=}, {positions[0].value=}")
    cont = []
    if depth % 2 != 2:
        for p in positions:
            if p.eval() == 30 and p.r == 0 and p.c == 3:
                print(p.locations, p.value)
                quit()
            #print("trying ", p)
            if p.r != 0 or p.c != 3:
                #print(p)
                cont.append(p)
    positions = cont
    #print(cont)
    newPositions = []
    for p in positions:
        for d in ((1,0),(-1,0),(0,1), (0,-1)):
            if (p.r + d[0], p.c + d[1]) != (3,0) and jcksn.exists((p.r + d[0],p.c + d[1]), grid):
                newPositions.append(p.move(d))

    positions = newPositions
            
        



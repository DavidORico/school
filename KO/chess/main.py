#!/usr/bin/env python3
import sys
import gurobipy as g
import numpy as np


f = open(sys.argv[1], "r")
line = f.readline()
num_rooks = int(line)
Lines = f.readlines()
rook_positions = np.zeros((num_rooks, 2), dtype=int)

indx = 0
for line in Lines:
    if line[0] == 'a':
        rook_positions[indx][0] = 2
    elif line[0] == 'b':
        rook_positions[indx][0] = 3
    elif line[0] == 'c':
        rook_positions[indx][0] = 4
    elif line[0] == 'd':
        rook_positions[indx][0] = 5
    elif line[0] == 'e':
        rook_positions[indx][0] = 6
    elif line[0] == 'f':
        rook_positions[indx][0] = 7
    elif line[0] == 'g':
        rook_positions[indx][0] = 8
    elif line[0] == 'h':
        rook_positions[indx][0] = 9

    rook_positions[indx][1] = int(line[1]) + 1
    indx += 1

f.close()

m = g.Model()

# vars
x = m.addVars(12, 12, vtype=g.GRB.BINARY, name="x")

# constraints
m.addConstr(x.sum(0, "*") + x.sum(1, "*") + x.sum(10, "*") + x.sum(11, "*")
            + x.sum("*", 0) + x.sum("*", 1) + x.sum("*", 10) + x.sum("*", 11) == 0)
for i in range(num_rooks):
    m.addConstr(x.sum(rook_positions[i][0], "*")+x.sum("*", rook_positions[i][1]) == 0)
for i in range(2, 10):
    for j in range(2, 10):
        m.addConstr(8*(1-x[i,j]) >= x[i+2, j+1] + x[i+2, j-1]
                    + x[i+1, j+2] + x[i+1, j-2]
                    + x[i-1, j+2] + x[i-1, j-2]
                    + x[i-2, j+1] + x[i-2, j-1])

#objective
m.setObjective(x.sum("*", "*"), sense=g.GRB.MAXIMIZE)

#m.write("model.lp")
m.optimize()

#print('\nSOLUTION:')
#for i in range(2, 10):
#    for j in range(2, 10):
#        print(x[i,j].X)
f = open(sys.argv[2], "w")
line = ""
count = 0
for i in range(2, 10):
    for j in range(2, 10):
        if int(x[i,j].X) == 1:
            if i == 2:
                line = line + 'a'
            elif i == 3:
                line = line + 'b'
            elif i == 4:
                line = line + 'c'
            elif i == 5:
                line = line + 'd'
            elif i == 6:
                line = line + 'e'
            elif i == 7:
                line = line + 'f'
            elif i == 8:
                line = line + 'g'
            elif i == 9:
                line = line + 'h'

            line = line + str(j-1) + '\n'

            count += 1
line = str(count) + '\n' + line
f.write(line)
f.close()
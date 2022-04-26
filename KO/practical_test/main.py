#!/usr/bin/env python3
import sys
import gurobipy as g


f = open(sys.argv[1], "r")
Lines = f.readlines()
filled_numbers = []
blank_symbols = []
for i in range(9):
    for j in range(9):
        if Lines[i][j] == '0':
            filled_numbers.append([0, i, j])
        elif Lines[i][j] == '1':
            filled_numbers.append([1, i, j])
        elif Lines[i][j] == '2':
            filled_numbers.append([2, i, j])
        elif Lines[i][j] == '3':
            filled_numbers.append([3, i, j])
        elif Lines[i][j] == '4':
            filled_numbers.append([4, i, j])
        elif Lines[i][j] == '5':
            filled_numbers.append([5, i, j])
        elif Lines[i][j] == '6':
            filled_numbers.append([6, i, j])
        elif Lines[i][j] == '7':
            filled_numbers.append([7, i, j])
        elif Lines[i][j] == '8':
            filled_numbers.append([8, i, j])
        elif Lines[i][j] == 'B':
            blank_symbols.append([i, j])
f.close()

m = g.Model()

#vars
x = m.addVars(9, 9, 9, vtype=g.GRB.BINARY, name="x")
k = m.addVars(len(blank_symbols), vtype=g.GRB.INTEGER, name="k")

#constr
#only one number can be chosen
for i in range(9):
    for j in range(9):
        m.addConstr(x.sum(i, j, "*") == 1)

for i in range(9):
    for j in range(9):
        m.addConstr(x.sum(i, "*", j) == 1)

for i in range(9):
    for j in range(9):
        m.addConstr(x.sum("*", i, j) == 1)

for i in range(3):
    for j in range(3):
        for s in range(9):
            m.addConstr(g.quicksum(x[k,l,s] for k in range(i*3, i*3+3) for l in range(j*3, j*3+3)) == 1)

for set_num in filled_numbers:
    m.addConstr(x[set_num[1], set_num[2], set_num[0]] == 1)

inc = 0
for pos_b in blank_symbols:
    for i in range(9):
        if pos_b[0] != 0 and pos_b[1] != 0:
            m.addConstr(k[inc] <= x[pos_b[0] - 1, pos_b[1] - 1, i] * i)
        if pos_b[0] != 0:
            m.addConstr(k[inc] <= x[pos_b[0] - 1, pos_b[1], i]*i)
        if pos_b[1] != 0:
            m.addConstr(k[inc] <= x[pos_b[0], pos_b[1] - 1, i]*i)
    inc += 1

#objective
id_obj = [[0,0], [8,0], [0,8], [8,8], [4, 4]]
m.setObjective(g.quicksum(x[id[0],id[1],k]*k for id in id_obj for k in range(9)), sense=g.GRB.MAXIMIZE)

m.optimize()

f = open(sys.argv[2], "w")
if m.Status != g.GRB.OPTIMAL:
    f.write(str(-1))
else:
    line = str(int(m.objVal)) + '\n'
    for i in range(9):
        for j in range(9):
            for k in range(9):
                if int(x[i,j,k].X) == 1:
                    line = line + str(k)
                    break
        line = line + '\n'
    f.write(line)
f.close()


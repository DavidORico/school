#!/usr/bin/env python3
import sys
import gurobipy as g


f = open(sys.argv[1], "r")
line = f.readline()
f.close()
d = [int(i) for i in line.split(" ")]

m = g.Model()

# vars
n=len(d)
x = m.addVars(n, vtype=g.GRB.INTEGER, name="x", obj=1)
z = m.addVars(n, vtype=g.GRB.INTEGER, name="z")
# constraints
for i in range(n):
    m.addConstr(d[i] - g.quicksum(x[(i-j)%24] for j in range(8)) <= z[i])
    m.addConstr(g.quicksum(x[(i-j)%24] for j in range(8)) - d[i] <= z[i])
    m.addConstr(z[i] >= 0)

#objective
m.setObjective(g.quicksum(z[i] for i in range(24)), sense=g.GRB.MINIMIZE)

#m.write("model.lp")
m.optimize()

res = [x[i].x for i in range(24)]
f = open(sys.argv[2], "w")
f.write(str(int(round(m.objVal))) + '\n' + ' '.join(str(int(e)) for e in res))
f.close()
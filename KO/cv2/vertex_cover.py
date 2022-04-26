import gurobipy as grb

# Example input
n = 5  # number of vertices
edges = [(0, 1), (2, 3), (0, 4), (3, 1), (3, 4)]  # list of edges

model = grb.Model()

# var
x = model.addVars(n, vtype=grb.GRB.BINARY, name = "x")

# constr
for (i,j) in edges:
    model.addConstr(x[i] + x[j] >= 1)

model.setObjective(x.sum(), sense=grb.GRB.MINIMIZE)

model.optimize()

for i in x:
    print(i, x[i].X)
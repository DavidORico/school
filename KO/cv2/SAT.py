import gurobipy as grb

# Example input
# SAT formula: (x0 or ~x1) and (~x0 or x1 or x2) <- encode directly into the model

model = grb.Model()

# variables
x0 = model.addVar(vtype=grb.GRB.BINARY, name="x0")
x1 = model.addVar(vtype=grb.GRB.BINARY, name="x1")
x2 = model.addVar(vtype=grb.GRB.BINARY, name="x2")

# constraints

model.addConstr(x0 + (1 - x1) >= 1)
model.addConstr((1 - x0) + x1 + x2 >= 1)

# objective
# -- neni (protoze chci jen zjistit, jestli to existuje)


model.optimize()

print("x0", x0.X)
print("x1", x1.X)
print("x2", x2.X)
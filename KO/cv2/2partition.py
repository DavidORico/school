import gurobipy as grb



# Example input
S = [100, 50, 50, 50, 20, 20, 5]

model = grb.Model()

# variables
x = model.addVars(len(S), vtype=grb.GRB.BINARY,name="x") # bacha na to treba pri scitani... pro python to jsou ty klice
y = model.addVar(vtype=grb.GRB.CONTINUOUS, name="y") #added

#constrs
S1 = grb.quicksum(x[i] * S[i] for i in x)
S2 = grb.quicksum((1- x[i]) * S[i] for i in x)
# model.addConstr(S1 == S2)
model.addConstr(S1 - S2 <= y)
model.addConstr(S1 - S2 >= y)

# objective
model.setObjective(y, sense=grb.GRB.MINIMIZE) # added

model.optimize()

for i in x:
    print(i, x[i].X)



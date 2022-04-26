#!/usr/bin/env python3
import sys
import gurobipy as g
import numpy as np


def smallest_cycle(res, n):
    sol_mod = np.zeros((n, n))
    visited = np.zeros((n,))
    for k, v in res.items():
        sol_mod[k] = v

    cycles = []
    while np.any(visited == 0):
        curr_node = visited.argmin()
        curr_cycle = []
        while True:
            if visited[curr_node] == 1:
                break

            visited[curr_node] = 1
            next_node = np.where(sol_mod[curr_node, :] == 1)[0][0]
            curr_cycle.append((curr_node, next_node))
            curr_node = next_node
        if curr_cycle:
            cycles.append(curr_cycle)

    return min(cycles, key=len)

def dfs_dummy_print(res, n):
    cycle = []
    next = None
    for i in range(n):
        if res[n-1, i].X == 1:
            cycle.append((n-1, i))
            next = i
            break

    while True:
        if next == n-1:
            break

        for i in range(n):
            if res[next, i].X == 1:
                cycle.append((next, i))
                next = i
                break
    return cycle

def calc_cost(s1, s2, w, h):
    return np.sum(np.absolute(s1[-1] - s2[0]))

def main():
    f = open(sys.argv[1], "r")
    line = f.readline()
    #print(line)
    d = [int(i) for i in line.split(" ")]
    num_stripes = d[0]
    width_stripe = d[1]
    height_stripe = d[2]

    # transform original file and ignore middle of stripes
    stripes = np.loadtxt(f, dtype=int)
    stripes = stripes.reshape((num_stripes, height_stripe, width_stripe, 3))
    f.close()

    # costs of edges
    c = np.zeros([num_stripes+1, num_stripes+1], dtype=int)
    for i in range(num_stripes):
        for j in range(num_stripes):
            if i != j:
                c[i, j] = np.abs(stripes[i, :, -1, :] - stripes[j, :, 0, :]).sum()

    m = g.Model()
    m.Params.lazyConstraints = 1
    # Variables
    x = m.addVars(num_stripes+1, num_stripes+1, vtype=g.GRB.BINARY, name="x")

    # Constraints
    m.addConstrs(x.sum(i, "*") == 1
                 for i in range(num_stripes+1))
    m.addConstrs(x.sum("*", i) == 1
                 for i in range(num_stripes+1))
    m.addConstrs(x[i, i] == 0
                 for i in range(num_stripes+1))

    # Objective
    m.setObjective(g.quicksum([c[i, j]*x[i, j]
                             for i in range(num_stripes+1)
                             for j in range(num_stripes+1)]))

    # lazy constraint
    def my_callback(model, where):
        if where == g.GRB.Callback.MIPSOL:
            res = model.cbGetSolution(x)
            smallest_subtour = smallest_cycle(res, num_stripes+1)
            # Add lazy constraint to model.
            if len(smallest_subtour) != num_stripes+1:
                model.cbLazy(g.quicksum(x[idx[0], idx[1]] for idx in smallest_subtour) <= len(smallest_subtour) - 1)

    # call the solver
    m.optimize(my_callback)

    # get result
    tour = dfs_dummy_print(x, num_stripes+1)
    f = open(sys.argv[2], "w")
    line = ""
    for i in range(len(tour)-1):
        if i != len(tour)-2:
            line += str(tour[i][1]+1) + " "
        else:
            line += str(tour[i][1] + 1)
    f.write(line)
    f.close()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import sys
import numpy as np
import gurobipy as g


def main():
    f = open(sys.argv[1], "r")
    line = f.readline()
    d = [int(i) for i in line.split(" ")]
    num_vertices = d[0]
    num_edges = d[1]
    edge_costs = np.zeros((num_vertices+2, num_vertices+2)) - 1
    b_values = np.zeros((num_vertices))

    for i in range(num_edges):
        line = f.readline()
        d = [int(p) for p in line.split(" ")]
        edge_costs[d[0], d[1]] = d[2]
        edge_costs[d[1], d[0]] = d[2]

    line = f.readline()
    terminal_vert = [int(p) for p in line.split(" ")]
    f.close()

    lower_bounds = np.ones((num_vertices + 2, num_vertices + 2))
    upper_bounds = np.zeros((num_vertices + 2, num_vertices + 2)) + len(terminal_vert) - 1

    # start and sink node edges
    start = num_vertices
    sink = num_vertices + 1
    for i in range(len(terminal_vert)):
        if i == 0:
            # first terminal vertex chosen as connected to start node
            b_values[terminal_vert[i]] = len(terminal_vert) - 1
            lower_bounds[start, terminal_vert[i]] = 0
            upper_bounds[start, terminal_vert[i]] = len(terminal_vert) - 1
            edge_costs[start, terminal_vert[i]] = 0
        else:
            b_values[terminal_vert[i]] = -1
            #lower_bounds[terminal_vert[i], sink] = 0
            upper_bounds[terminal_vert[i], sink] = 1
            edge_costs[terminal_vert[i], sink] = 0

    m = g.Model()

    # vars
    flow = m.addVars(num_vertices+2, num_vertices+2, vtype=g.GRB.INTEGER, name="f")
    binary_bounds = m.addVars(num_vertices + 2, num_vertices + 2, vtype=g.GRB.BINARY, name="b")

    # constraints
    for i in range(num_vertices+2):
        # Kirhoff constraint
        if i < num_vertices:
            m.addConstr(flow.sum(i, "*") == flow.sum("*", i))
        for j in range(num_vertices+2):
            if edge_costs[i, j] == -1:  # don't consider edges that don't exist in the graph
                m.addConstr(flow[i, j] == 0)
                m.addConstr(binary_bounds[i, j] == 0)
            else:  # binary variable helps to replace the signum function for objective by correct bounding
                m.addConstr(flow[i, j] <= int(upper_bounds[i, j]) * (1 - binary_bounds[i, j]))
                m.addConstr(int(lower_bounds[i, j]) * (-binary_bounds[i, j]) <= flow[i, j])
    # all N-1 nodes have to be produced and consumed
    m.addConstr(flow.sum("*", sink) == len(terminal_vert) - 1)
    m.addConstr(flow[start, terminal_vert[0]] == len(terminal_vert) - 1)

    # goal, sum of all edge costs for flows that were used
    m.setObjective(g.quicksum(
        (1 - binary_bounds[i, j]) * int(edge_costs[i, j])
        for i in range(num_vertices)
        for j in range(num_vertices)),
        sense=g.GRB.MINIMIZE)
    m.optimize()

    f = open(sys.argv[2], "w")
    final_val = 0
    line = ""
    for i in range(num_vertices):
        for j in range(num_vertices):
            if flow[i, j].X > 0:
                line = line + str(i) + ' ' + str(j) + '\n'
                final_val += int(edge_costs[i, j])
    line = str(final_val) + '\n' + line
    f.write(line)
    f.close()


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
import sys
import copy

class Node:
    def __init__(self):
        self.successors = []
        self.pred = []
        self.l_bounds = []
        self.u_bounds = []

    def add_succ(self, succ, l_b, u_b):
        self.successors.append(succ)
        self.l_bounds.append(l_b)
        self.u_bounds.append(u_b)

    def add_pred(self, pred):
        self.pred.append(pred)

def labelling(graph, start, sink, flows):
    queue = []
    path = []  # list of tuples (nd, succ, is_forward)
    visited_from = {}
    visited = {}
    delta = float('inf')
    for i in range(len(graph)):
        visited_from[i] = (-1, True)
        visited[i] = False
    visited[start] = True
    queue.append(start)

    #BFS
    while queue:
        nd = queue.pop(0)
        if nd == sink:
            break

        for i in range(len(graph[nd].successors)):
            #forward
            if not visited[graph[nd].successors[i]] and visited[nd] and flows[nd][i] < graph[nd].u_bounds[i]:
                visited[graph[nd].successors[i]] = True
                visited_from[graph[nd].successors[i]] = (nd, True)
                queue.append(graph[nd].successors[i])
                delta = min(delta, graph[nd].u_bounds[i] - flows[nd][i])
        for i in range(len(graph[nd].pred)):
            for j in range(len(graph[graph[nd].pred[i]].successors)):
                if nd == graph[graph[nd].pred[i]].successors[j]:
                    #backward
                    if not visited[graph[nd].pred[i]] and visited[nd] and flows[graph[nd].pred[i]][j] > graph[graph[nd].pred[i]].l_bounds[j]:
                        visited[graph[nd].pred[i]] = True
                        visited_from[graph[nd].pred[i]] = (nd, False)
                        queue.append(graph[nd].pred[i])
                        delta = min(delta, flows[graph[nd].pred[i]][j] - graph[graph[nd].pred[i]].l_bounds[j])

    if visited_from[sink][0] == -1 or delta == float('inf'):
        return 0, []

    # reconstruct path
    nd = sink
    while visited_from[nd][0] != -1:
        path.insert(0, (visited_from[nd][0], nd, visited_from[nd][1]))
        nd = visited_from[nd][0]

    return delta, path

def ford_fulkerson(graph, start, sink, init_flows):
    max_flows = init_flows.copy()
    while True:
        delta, P = labelling(graph, start, sink, max_flows)
        #print(delta)
        #print(P)
        #break

        if delta > 0:
            for i in range(len(P)):
                #forward arc
                if P[i][2] == True:
                    for j in range(len(graph[P[i][0]].successors)):
                        if graph[P[i][0]].successors[j] == P[i][1]:
                            max_flows[P[i][0]][j] += delta
                            break
                else:
                    for j in range(len(graph[P[i][1]].successors)):
                        if graph[P[i][1]].successors[j] == P[i][0]:
                            max_flows[P[i][1]][j] -= delta
                            break
        else:
            break

    return max_flows

def check_saturation(graph, flows, start_node):
    #print(graph[start_node].u_bounds)
    for i in range(len(flows[start_node])):
        #print(flows[start_node][i])
        if flows[start_node][i] != graph[start_node].u_bounds[i]:
            return False
    return True

def print_graph(graph):
    for i in range(len(graph)):
        print("Node: " + str(i))
        print("Successors")
        print(graph[i].successors)
        print("Lower bounds")
        print(graph[i].l_bounds)
        print("Upper bounds")
        print(graph[i].u_bounds)

def main():
    f = open(sys.argv[1], "r")
    line = f.readline()
    d = [int(i) for i in line.split(" ")]
    num_customers = d[0]
    num_products = d[1]

    #orig graph
    st_nd = num_customers + num_products
    end_nd = num_customers + num_products + 1
    original_graph = []
    for i in range(num_customers + num_products + 2):
        original_graph.append(Node())
    #prepare customer and start nodes
    for i in range(num_customers):
        line = f.readline()
        d = [int(p) for p in line.split(" ")]
        original_graph[st_nd].add_succ(i, d[0], d[1])
        for j in range(2, len(d)):
            original_graph[i].add_succ(d[j]-1+num_customers, 0, 1)
    line = f.readline()
    min_product_reviews = [int(p) for p in line.split(" ")]
    f.close()

    #make connections from products to sink node
    for i in range(num_customers, num_customers + num_products):
        original_graph[i].add_succ(end_nd, min_product_reviews[i-num_customers], 500000)

    # add predecessors
    for i in range(len(original_graph)):
        for j in range(len(original_graph[i].successors)):
            original_graph[original_graph[i].successors[j]].add_pred(i)
    #print("created graph")
    #print_graph(original_graph)

    #modify original graph
    #modified_graph = copy.deepcopy(original_graph)
    modified_graph = []
    for i in range(num_customers + num_products + 2):
        modified_graph.append(Node())
        modified_graph[i].successors = original_graph[i].successors.copy()
        modified_graph[i].l_bounds = original_graph[i].l_bounds.copy()
        modified_graph[i].u_bounds = original_graph[i].u_bounds.copy()
        modified_graph[i].pred = original_graph[i].pred.copy()

    #add two new nodes
    mod_st_nd = num_customers + num_products + 2
    mod_end_nd = num_customers + num_products + 3
    modified_graph.append(Node())
    modified_graph.append(Node())

    #edge from original sink to original start
    modified_graph[end_nd].add_succ(st_nd, 0, float('inf'))
    modified_graph[st_nd].add_pred(end_nd)

    #change lower and upper bounds
    for i in range(num_customers+num_products+1):
        for j in range(len(modified_graph[i].l_bounds)):
            modified_graph[i].u_bounds[j] -= modified_graph[i].l_bounds[j]
            modified_graph[i].l_bounds[j] = 0

    #calc Ls of vertices
    L_values = [0] * (num_customers + num_products + 2)
    for curr_nd in range(num_customers + num_products + 2):
        L_values[curr_nd] -= sum(original_graph[curr_nd].l_bounds)
        if curr_nd < num_customers:
            for i in range(len(original_graph[st_nd].successors)):
                if original_graph[st_nd].successors[i] == curr_nd:
                    L_values[curr_nd] += original_graph[st_nd].l_bounds[i]
                    break
        else:
            for j in range(num_customers):
                for k in range(len(original_graph[j].successors)):
                    if original_graph[j].successors[k] == curr_nd:
                        L_values[curr_nd] += original_graph[j].l_bounds[k]
                        break

    #print(L_values)
    added_to_start = False
    added_to_end = False
    for i in range(num_customers + num_products + 2):
        if L_values[i] > 0:
            added_to_start = True
            modified_graph[mod_st_nd].add_succ(i, 0, L_values[i])
            modified_graph[i].add_pred(mod_st_nd)
        elif L_values[i] < 0:
            added_to_end = True
            modified_graph[i].add_succ(mod_end_nd, 0, -L_values[i])
            modified_graph[mod_end_nd].add_pred(i)
    if not added_to_start or not added_to_end:
        f = open(sys.argv[2], "w")
        f.write("-1")
        f.close()
        return
    #print("created modified graph")
    #print_graph(modified_graph)

    #ford fulkerson on the modified graph
    mod_flows = []
    for i in range(len(modified_graph)):
        mod_flows.append([0] * len(modified_graph[i].successors))
    max_mod_flows = ford_fulkerson(modified_graph, mod_st_nd, mod_end_nd, mod_flows)
    #print(max_mod_flows)
    #print("ran ford fulkerson on the modified graph")

    if not check_saturation(modified_graph, max_mod_flows, mod_st_nd):
        f = open(sys.argv[2], "w")
        f.write("-1")
        f.close()
        return
    #print("checked saturation")

    #modify flows
    init_orig_flows = []
    for i in range(len(original_graph)):
        init_orig_flows.append([0] * len(original_graph[i].successors))
        for j in range(len(original_graph[i].successors)):
            init_orig_flows[i][j] = max_mod_flows[i][j] \
                                           + original_graph[i].l_bounds[j]
    #print("modified flows")

    #ford fulkerson on the original graph
    final_flow = ford_fulkerson(original_graph, st_nd, end_nd, init_orig_flows)
    #print(final_flow)
    #print("ford fulkerson on the original graph")

    f = open(sys.argv[2], "w")
    for i in range(num_customers):
        list_of_chosen_prod = []
        for j in range(len(final_flow[i])):
            if final_flow[i][j] == 1:
                list_of_chosen_prod.append(original_graph[i].successors[j]-num_customers+1)
        if list_of_chosen_prod:
            listToStr = ' '.join(map(str, list_of_chosen_prod))
            f.write(listToStr + '\n')
    f.close()


if __name__ == "__main__":
    main()
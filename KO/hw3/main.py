#!/usr/bin/env python3
import sys


class Graph:
    def __init__(self):
        self.edges = []
        self.nodes = []  # list of edges for node


class Edge:
    def __init__(self, from_n, to_n, l_b, u_b):
        self.from_n = from_n
        self.to_n = to_n
        self.l_b = l_b
        self.u_b = u_b
        self.flow = 0


def reconstruct_path(graph, start, sink, visited_from):
    if visited_from[sink] == -1:
        return 0, []

    delta = float('inf')
    path = []
    curr_nd = sink
    while curr_nd != start:
        for edge_id in graph.nodes[curr_nd]:
            if graph.edges[edge_id].from_n == curr_nd and graph.edges[edge_id].to_n == visited_from[curr_nd]:
                # backward edge
                delta = min(delta, graph.edges[edge_id].flow - graph.edges[edge_id].l_b)
                path.append((edge_id, False))
                break
            elif graph.edges[edge_id].to_n == curr_nd and graph.edges[edge_id].from_n == visited_from[curr_nd]:
                # forward edge
                delta = min(delta, graph.edges[edge_id].u_b - graph.edges[edge_id].flow)
                path.append((edge_id, True))
                break
        curr_nd = visited_from[curr_nd]
    path.reverse()
    return delta, path


def labeling(graph, start, sink):
    # BFS
    queue = []
    visited_from = [-1 for _ in range(len(graph.nodes))]
    visited = [False for _ in range(len(graph.nodes))]
    queue.append(start)
    visited[start] = True

    while queue:
        curr_nd = queue.pop(0)

        if curr_nd == sink:
            break
        for edge_id in graph.nodes[curr_nd]:
            if graph.edges[edge_id].from_n == curr_nd:  # forward
                if not visited[graph.edges[edge_id].to_n] and graph.edges[edge_id].flow < graph.edges[edge_id].u_b:
                    queue.append(graph.edges[edge_id].to_n)
                    visited[graph.edges[edge_id].to_n] = True
                    visited_from[graph.edges[edge_id].to_n] = curr_nd
                    #if graph.edges[edge_id].to_nd == sink:
                    #    break
            else:  # backward
                if not visited[graph.edges[edge_id].from_n] and graph.edges[edge_id].flow > graph.edges[edge_id].u_b:
                    queue.append(graph.edges[edge_id].from_n)
                    visited[graph.edges[edge_id].to_n] = True
                    visited_from[graph.edges[edge_id].to_n] = curr_nd
                    #if graph.edges[edge_id].from_nd == sink:
                    #    break

    delta, P = reconstruct_path(graph, start, sink, visited_from)
    return delta, P


def ford_fulkerson(graph, start, sink):
    while True:
        delta, P = labeling(graph, start, sink)
        if delta > 0:
            for p in P:
                if p[1] == True:
                    graph.edges[p[0]].flow += delta
                else:
                    graph.edges[p[0]].flow -= delta
        else:
            break
    return


def saturated(graph, st_nd):
    for edge_id in graph.nodes[st_nd]:
        if graph.edges[edge_id].from_n == st_nd and graph.edges[edge_id].flow != graph.edges[edge_id].u_b:
            return False
    return True


def main():
    f = open(sys.argv[1], "r")
    line = f.readline()
    d = [int(i) for i in line.split(" ")]
    num_customers = d[0]
    num_products = d[1]
    st_nd = num_customers + num_products
    end_nd = num_customers + num_products + 1

    original_graph = Graph()
    for i in range(num_customers):
        line = f.readline()
        d = [int(p) for p in line.split(" ")]
        original_graph.edges.append(Edge(st_nd, i, d[0], d[1]))
        for j in range(2, len(d)):
            original_graph.edges.append(Edge(i, d[j]-1+num_customers, 0, 1))
    line = f.readline()
    min_product_reviews = [int(p) for p in line.split(" ")]
    f.close()

    # make connections from products to sink node
    for i in range(num_customers, num_customers + num_products):
        original_graph.edges.append(Edge(i, end_nd, min_product_reviews[i - num_customers], 50000000))

    # assign edges to node
    original_graph.nodes = [[] for _ in range(num_customers + num_products + 2)]
    for i in range(len(original_graph.edges)):
        original_graph.nodes[original_graph.edges[i].from_n].append(i)
        original_graph.nodes[original_graph.edges[i].to_n].append(i)

    # original graph created, creating modified graph
    # copy everything from original graph
    modified_graph = Graph()
    for edge in original_graph.edges:
        modified_graph.edges.append(Edge(edge.from_n, edge.to_n, edge.l_b, edge.u_b))
    for lst_edges in original_graph.nodes:
        modified_graph.nodes.append(lst_edges.copy())

    # edge from original sink to original start
    modified_graph.edges.append(Edge(end_nd, st_nd, 0, float('inf')))
    modified_graph.nodes[end_nd].append(len(modified_graph.edges) - 1)
    modified_graph.nodes[st_nd].append(len(modified_graph.edges) - 1)

    # change lower and upper bounds, note inf - some value is still inf
    for edge in modified_graph.edges:
        edge.u_b = edge.u_b - edge.l_b
        edge.l_b = 0

    # calc Ls of nodes
    L_values = [0 for _ in range(num_customers + num_products + 2)]
    for i in range(len(original_graph.nodes)):
        for j in range(len(original_graph.nodes[i])):
            if original_graph.edges[original_graph.nodes[i][j]].from_n == i:
                L_values[i] = L_values[i] - original_graph.edges[original_graph.nodes[i][j]].l_b
            elif original_graph.edges[original_graph.nodes[i][j]].to_n == i:
                L_values[i] = L_values[i] + original_graph.edges[original_graph.nodes[i][j]].l_b

    # add new start and sink node and their edges
    mod_st_nd = num_customers + num_products + 2
    mod_end_nd = num_customers + num_products + 3
    modified_graph.nodes.append([])
    modified_graph.nodes.append([])
    for i in range(num_customers + num_products + 2):
        if L_values[i] > 0:
            modified_graph.edges.append(Edge(mod_st_nd, i, 0, L_values[i]))

            edge_id = len(modified_graph.edges) - 1
            modified_graph.nodes[mod_st_nd].append(edge_id)
            modified_graph.nodes[i].append(edge_id)
        elif L_values[i] < 0:
            modified_graph.edges.append(Edge(i, mod_end_nd, 0, -L_values[i]))

            edge_id = len(modified_graph.edges) - 1
            modified_graph.nodes[mod_end_nd].append(edge_id)
            modified_graph.nodes[i].append(edge_id)

    # run ford fulkerson on modified graph
    ford_fulkerson(modified_graph, mod_st_nd, mod_end_nd)

    if not saturated(modified_graph, mod_st_nd):
        f = open(sys.argv[2], "w")
        f.write("-1")
        f.close()
        return

    # modify flows of original graph
    for i in range(len(original_graph.edges)):
        original_graph.edges[i].flow = modified_graph.edges[i].flow + original_graph.edges[i].l_b

    ford_fulkerson(original_graph, st_nd, end_nd)

    f = open(sys.argv[2], "w")
    for i in range(num_customers):
        list_of_chosen_prod = []
        for edge_id in original_graph.nodes[i]:
            if original_graph.edges[edge_id].from_n == i and original_graph.edges[edge_id].flow == 1:
                list_of_chosen_prod.append(original_graph.edges[edge_id].to_n - num_customers + 1)
        if list_of_chosen_prod:
            listToStr = ' '.join(map(str, list_of_chosen_prod))
            f.write(listToStr + '\n')
    f.close()


if __name__ == "__main__":
    main()
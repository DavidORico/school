#!/usr/bin/env python3

import numpy as np
import sys


def print_infeasible(arg):
    with open(arg[2], "w") as fl:
        fl.write("-1")
    exit()


def back_track(g, lb, ub, f, s, t, visited_from):
    delta = np.max(ub)
    path = [t]
    while True:
        path.append(visited_from[int(path[-1])])
        u, v = int(path[-1]), int(path[-2])
        if g[u, v] == 1:
            delta = min(delta, ub[u, v] - f[u, v])
        else:
            delta = min(delta, f[v, u] - lb[v, u])
        if u == s:
            break
    path.reverse()
    return delta, path


def bfs(g, lb, ub, f, actual, t, n, visited_from):
    new_actual = []
    for a in actual:
        for idx in range(n - 1, -1, -1):
            if visited_from[idx] < 0:
                if (g[a, idx] == 1 and ub[a, idx] - f[a, idx] > 0) \
                        or (g[a, idx] == -1 and f[idx, a] - lb[idx, a] > 0):
                    visited_from[idx] = a
                    new_actual.append(idx)
                    if idx == t:
                        return visited_from
    if len(new_actual) > 0:
        visited_from = bfs(g, lb, ub, f, new_actual, t, n, visited_from)
    return visited_from


def labeling(g, lb, ub, f, s, t, n):
    visited_from = bfs(g, lb, ub, f, [s], t, n, -1 * np.ones(n))
    if visited_from[t] < 0:
        return 0, []
    return back_track(g, lb, ub, f, s, t, visited_from)


def ford_fulkerson(g, lb, ub, f, s, t, n):
    while True:
        delta, path = labeling(g, lb, ub, f, s, t, n)
        if delta > 0:
            for idx in range(1, len(path)):
                if g[int(path[idx - 1]), int(path[idx])] == 1:
                    f[int(path[idx - 1]), int(path[idx])] += delta
                else:
                    f[int(path[idx]), int(path[idx - 1])] -= delta
        else:
            break
    return f


def find_init_flow(g, lb, ub, s, t, n):
    new_g = np.zeros((n + 2, n + 2))
    new_lb = np.zeros_like(new_g)
    new_ub = np.zeros_like(new_g)
    new_f = np.zeros_like(new_g)
    new_g[0:n, 0:n] = g
    # add edge from t to s
    new_g[t, s] = 1
    new_g[s, t] = -1
    # new upper bounds
    new_ub[0:n, 0:n] = ub - lb
    new_ub[t, s] = np.inf
    new_s = n
    new_t = n + 1
    for idx in range(n):
        b = np.sum(lb[idx, :]) - np.sum(lb[:, idx])
        if b > 0:
            new_g[idx, new_t] = 1
            new_g[new_t, idx] = -1
            new_ub[idx, new_t] = b
        elif b < 0:
            new_g[new_s, idx] = 1
            new_g[idx, new_s] = -1
            new_ub[new_s, idx] = -b
    new_f = ford_fulkerson(new_g, new_lb, new_ub, new_f, new_s, new_t, n + 2)

    if np.all(new_f[new_s, :] == new_ub[new_s, :]):
        new_f[t, s] = 0
        f = lb + new_f[0:n, 0:n]
        return True, f
    else:
        return False, new_f


if __name__ == "__main__":

    with open(sys.argv[1], 'r') as file:
        C, P = [int(x) for x in next(file).split()]
        C_start = 1
        P_start = 1 + C
        T_start = 1 + C + P
        N = C + P + 2
        G = np.zeros((N, N))
        G[0, C_start:C_start + C] = 1
        G[C_start:C_start + C, 0] = -1
        G[P_start: P_start + P, T_start] = 1
        G[T_start, P_start: P_start + P] = -1
        LB = np.zeros((N, N))
        UB = np.zeros((N, N))
        for i in range(C):
            inp = [int(x) for x in next(file).split()]
            LB[0, C_start + i] = inp[0]
            UB[0, C_start + i] = inp[1]
            for j in range(2, len(inp)):
                G[i + C_start, inp[j] + P_start - 1] = 1
                G[inp[j] + P_start - 1, i + C_start] = -1
                UB[i + C_start, inp[j] + P_start - 1] = 1

        LB[P_start: P_start + P, T_start] = [int(x) for x in next(file).split()]
        UB[P_start: P_start + P, T_start] = 10  # np.sum(UB[0, :])
        if np.sum(LB[P_start: P_start + P, T_start]) > np.sum(UB[0, :]):
            # print_infeasible(sys.argv)
            a = 1

    feasible, F = find_init_flow(G, LB, UB, 0, T_start, N)
    if not feasible:
        print_infeasible(sys.argv)
    F = ford_fulkerson(G, LB, UB, F, 0, T_start, N)

    with open(sys.argv[2], "w") as file:
        for i in range(C_start, C_start + C):
            output = np.where(F[i, :] > 0)[0] - P_start + 1
            out_str = ""
            for ch in output:
                out_str += str(ch) + " "
            out_str += "\n"
            file.write(out_str)

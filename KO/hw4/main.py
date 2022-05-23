#!/usr/bin/env python3
import sys
import numpy as np


def dfs(c, non_scheduled_tasks, processing_times, release_times, deadlines, UB):
    if non_scheduled_tasks.size == 0:
        return True, False, [], c

    # rule one
    for id in non_scheduled_tasks:
        if max(release_times[id], c) + processing_times[id] > deadlines[id]:
            # prune
            return False, None, None, None

    # rule two
    LB = max(c, np.min(release_times[non_scheduled_tasks])) + np.sum(processing_times[non_scheduled_tasks])
    new_UB = min(np.max(deadlines[non_scheduled_tasks]), UB)
    if LB > new_UB:
        # prune
        return False, None, None, None

    # rule three
    optimal = False
    if c <= np.min(release_times[non_scheduled_tasks]):
        # don't backtrack
        optimal = True

    found_feasible = False
    min_UB = new_UB
    new_schedule = []
    for i in range(len(non_scheduled_tasks)):
        mod_tasks = np.delete(non_scheduled_tasks, i)
        mod_c = max(release_times[non_scheduled_tasks[i]] + processing_times[non_scheduled_tasks[i]],
                c + processing_times[non_scheduled_tasks[i]])
        feasible, n_optimal, schedule, new_UB = dfs(mod_c, mod_tasks,  processing_times, release_times, deadlines, min_UB)
        if feasible:
            found_feasible = True
            if new_UB <= min_UB:
                min_UB = new_UB
                new_schedule = schedule.copy()
                new_schedule.append(non_scheduled_tasks[i])
            #if n_optimal:
            return feasible, n_optimal, new_schedule, min_UB

    if found_feasible:
        return True, optimal, new_schedule, min_UB
    else:
        return False, None, None, None


def reconstruct_path(order_proc, release_times, processing_times):
    res = np.zeros((release_times.size))
    c = 0
    for id in order_proc:
        res[id] = max(c, release_times[id])
        c = max(c, release_times[id]) + processing_times[id]
    return res


def main():
    f = open(sys.argv[1], "r")
    line = f.readline()
    d = [int(i) for i in line.split(" ")]
    num_processes = d[0]
    processing_times = np.zeros((num_processes))
    release_times = np.zeros((num_processes))
    deadlines = np.zeros((num_processes))


    for i in range(num_processes):
        line = f.readline()
        d = [int(i) for i in line.split(" ")]
        processing_times[i] = d[0]
        release_times[i] = d[1]
        deadlines[i] = d[2]
    f.close()

    non_scheduled_tasks = np.arange(num_processes)
    min_UB = np.max(deadlines[non_scheduled_tasks])
    feasible, optimal, res, UB = dfs(0, non_scheduled_tasks, processing_times, release_times, deadlines, min_UB)

    if not feasible:
        f = open(sys.argv[2], "w")
        f.write(str(-1))
        f.close()
    else:
        res.reverse()
        optimal_release_times = reconstruct_path(res, release_times, processing_times)
        f = open(sys.argv[2], "w")
        line = ""
        for rs in optimal_release_times:
            line = line + str(int(rs)) + '\n'
        f.write(line)
        f.close()


if __name__ == "__main__":
    main()
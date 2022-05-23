import matplotlib.pyplot as plt
import numpy as np

strategies = ["FF-replan", "follow VI policy", "MCTS", "obtaining VI policy"]
files = ["7-A1.txt", "7-A2.txt", "7-B.txt",
          "7-C.txt", "7-E.txt", "15-A1.txt",
          "15-A2.txt", "15-B.txt", "15-C.txt",
          "15-E.txt", "25-A1.txt", "25-A2.txt",
          "25-B.txt", "25-C.txt", "25-E.txt",
          "51-A1.txt", "51-A2.txt", "51-B.txt",
          "51-C.txt", "51-E.txt"]
ff_replan_averages = np.zeros((20))
vi_averages = np.zeros((20))
mcts_averages = np.zeros((20))
policy_times = np.zeros((20))
for i in range(len(files)):
    # FF replan
    f = open("../output/FF_REPLAN/time_microsec_maze-" + files[i], "r")
    line = f.readline()
    d = [int(i) for i in line[1:].split(" ")]
    ff_replan_averages[i] = np.sum(d)/len(d)
    f.close()
    # VI async
    f = open("../output/VI/time_microsec_maze-" + files[i], "r")
    line = f.readline()
    d = [int(i) for i in line[1:].split(" ")]
    vi_averages[i] = np.sum(d)/len(d)
    f.close()
    # policy
    f = open("../output/VI/policy_time_microsec_maze-" + files[i], "r")
    line = f.readline()
    policy_times[i] = int(line[1:])
    f.close()
    # MCTS
    f = open("../output/MCTS/time_microsec_maze-" + files[i], "r")
    line = f.readline()
    d = [int(i) for i in line[1:].split(" ")]
    mcts_averages[i] = np.sum(d)/len(d)
    f.close()

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.barh(strategies, [ff_replan_averages[i], vi_averages[i], mcts_averages[i], policy_times[i]], align='center')
    ax.set_xlabel('microseconds')
    ax.set_title("Average runtime comparisons for " + files[i] + " on 1000 runs")

    fig.savefig("runtimes/" + files[i] + "runtime.png")
    # plt.show()

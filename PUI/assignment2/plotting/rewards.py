import plotly.graph_objects as go

x = []
files = ["7-E.txt", "15-E.txt", "25-E.txt", "51-E.txt"]

ff_replan_rewards = []
vi_rewards = []
mcts_rewards = []
for i in range(len(files)):
    # FF replan
    f = open("../output/FF_REPLAN/rewards_maze" + files[i], "r")
    line = f.readline()
    d = [int(i) for i in line[1:].split(" ")]
    x.extend([files[i]] * len(d))
    ff_replan_rewards.extend(d)
    f.close()
    # VI async
    f = open("../output/VI/rewards_maze" + files[i], "r")
    line = f.readline()
    d = [int(i) for i in line[1:].split(" ")]
    vi_rewards.extend(d)
    f.close()
    # MCTS
    f = open("../output/MCTS/rewards_maze" + files[i], "r")
    line = f.readline()
    d = [int(i) for i in line[1:].split(" ")]
    mcts_rewards.extend(d)
    f.close()

fig = go.Figure()

fig.add_trace(go.Box(
    y=ff_replan_rewards,
    x=x,
    name='FF-replan',
    marker_color='#3D9970'
))
fig.add_trace(go.Box(
    y=vi_rewards,
    x=x,
    name='VI async',
    marker_color='#FF4136'
))
fig.add_trace(go.Box(
    y=mcts_rewards,
    x=x,
    name='MCTS',
    marker_color='#FF851B'
))

fig.update_layout(
    yaxis_title='rewards',
    boxmode='group' # group together boxes of the different traces for each value of x
)
fig.show()

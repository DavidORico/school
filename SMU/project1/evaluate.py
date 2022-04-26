import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import List

import numpy as np


def evaluate(rewards1: List[float], rewards2: List[float], rewards3: List[float]):
    # TODO implement your own code here if you want to
    # or alternatively you can modify the existing code
    # if you reuse the averaging, you should probably change the parameters

    np.set_printoptions(precision=5)

    #print("Rewards:")
    #print(rewards)
    #print("Simple moving average:")
    # if you reuse this code, you should change the parameters
    #print(simple_moving_average(rewards, 40))
    #print("Exponential moving average")
    #print(exponential_moving_average(rewards, 0.2))
    #print("Average")
    #print(np.sum(rewards) / len(rewards))
    #print("Average from the last 10000 games")
    #print(np.sum(rewards[-10000:]) / 10000)

    plot_averages(rewards1, rewards2, rewards3)
    plot_averages_last(rewards1, rewards2, rewards3)
    plot_sma_series(simple_moving_average(rewards1, 5000), simple_moving_average(rewards2, 5000), simple_moving_average(rewards3, 5000))
    plot_ema_series(exponential_moving_average(rewards1, 0.5), "random")
    plot_ema_series(exponential_moving_average(rewards2, 0.5), "dealer")
    plot_ema_series(exponential_moving_average(rewards3, 0.5), "agent")

# check Wikipedia: https://en.wikipedia.org/wiki/Moving_average
def simple_moving_average(x: List[float], n: int) -> float:
    mean = np.zeros(len(x) - n + 1)
    tmp_sum = np.sum(x[0:n])
    for i in range(len(mean) - 1):
        mean[i] = tmp_sum
        tmp_sum -= x[i]
        tmp_sum += x[i + n]
    mean[len(mean)-1] = tmp_sum
    return mean / n


# check Wikipedia: https://en.wikipedia.org/wiki/Moving_average
def exponential_moving_average(x: List[float], alpha: float) -> float:
    mean = np.zeros(len(x))
    mean[0] = x[0]
    for i in range(1, len(x)):
        mean[i] = alpha * x[i] + (1.0 - alpha) * mean[i - 1]
    return mean

def plot_averages(arr1, arr2, arr3):
    fig, ax = plt.subplots()
    ax.bar(['random', 'dealer', 'SARSA'], [np.sum(arr1) / len(arr1), np.sum(arr2) / len(arr2), np.sum(arr3) / len(arr3)])
    ax.set_title("Average over all 300000 episodes for different agents")
    fig.savefig('averages.pdf')

def plot_averages_last(arr1, arr2, arr3):
    fig, ax = plt.subplots()
    ax.bar(['random', 'dealer', 'SARSA'], [np.sum(arr1[-10000:]) / 10000, np.sum(arr2[-10000:]) / 10000, np.sum(arr3[-10000:]) / 10000])
    ax.set_title("Average from the last 10000 episodes out of 300000 for different agents")
    fig.savefig('averages_last.pdf')

def plot_sma_series(arr1, arr2, arr3):
    fig, ax = plt.subplots()
    ax.plot(arr1, label="random", linestyle="-")
    ax.plot(arr2, label="dealer", linestyle="--")
    ax.plot(arr3, label="SARSA", linestyle="-.")
    ax.legend()
    ax.set_xlabel('episodes where param n = 5000')
    ax.set_ylabel('average')
    ax.set_title("Simple moving average for different agents")
    fig.savefig('sma_values.pdf')

def plot_ema_series(arr1, name):
    fig, ax = plt.subplots()
    ax.plot(arr1, label=name, linestyle="-")
    ax.legend()
    ax.set_xlabel('episodes where param alpha = 0.5')
    ax.set_ylabel('average')
    ax.set_title("Exponential moving average for " + name)
    fig.savefig("ema_values" + name + ".pdf")

def plot_learned_values(learned_Us, learned_Qs_hit, learned_Qs_stick):
    fig, ax = plt.subplots()
    ax.plot(learned_Us, label="Us of observed state", linestyle="-")
    ax.plot(learned_Qs_hit, label="Q hit of observed state", linestyle="--")
    ax.plot(learned_Qs_stick, label="Q stick of observed state", linestyle="-.")
    ax.legend()
    ax.set_xlabel('episodes')
    ax.set_ylabel('values')
    ax.set_title("Learned values for chosen observed state")
    fig.savefig('learned_values.pdf')

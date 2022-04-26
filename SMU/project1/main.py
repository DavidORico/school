from gym.wrappers import Monitor

from abstractagent import AbstractAgent
from dealeragent import DealerAgent
from evaluate import *
import gym
from gym import wrappers
from gym.envs.registration import register
from randomagent import RandomAgent
from sarsaagent import SarsaAgent
from tdagent import TDAgent
#from advancedagent import AdvancedAgent


def get_env() -> Monitor:
    """
    Creates the environment. Check the OpenAI Gym documentation.

    :rtype: Environment of the blackjack game that follows the OpenAI Gym API.
    """
    environment = gym.make('smu-blackjack-v0')
    return wrappers.Monitor(environment, 'smuproject4', force=True, video_callable=False)


if __name__ == "__main__":
    # Registers the environment so that it can be used
    register(
        id='smu-blackjack-v0',
        entry_point='blackjack:BlackjackEnv'
    )
    # ######################################################
    # IMPORTANT: do not modify the code above this line! ###
    # ######################################################

    # here you can play with the code yourself
    # for example you may want to split the code to two phases - training and testing
    # or you may want to compare two agents
    # feel free to modify the number of games played (highly recommended!)
    # ... or whatever

    env0 = get_env()
    env1 = get_env()
    env2 = get_env()
    env3 = get_env()

    number_of_episodes = 300000

    random_agent: AbstractAgent = RandomAgent(env0, number_of_episodes)
    dealer_agent: AbstractAgent = DealerAgent(env1, number_of_episodes)
    td_agent: AbstractAgent = TDAgent(env2, number_of_episodes)
    sarsa_agent: AbstractAgent = SarsaAgent(env3, number_of_episodes)
    # agent: AbstractAgent = AdvancedAgent(env, number_of_episodes)
    random_agent.train()
    dealer_agent.train()
    td_agent.train()
    sarsa_agent.train()

    Us_observed_state = td_agent.get_observed_states()
    Qs_hit, Qs_stick = sarsa_agent.get_observed_states()
    # in evaluate.py are some ideas that you might want to use to evaluate the agent
    # feel free to modify the code as you want to
    evaluate(env0.get_episode_rewards(), env1.get_episode_rewards(), env3.get_episode_rewards())
    plot_learned_values(Us_observed_state, Qs_hit, Qs_stick)

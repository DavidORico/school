from abstractagent import AbstractAgent
from blackjack import *
from carddeck import *
from state import *
import torch
import numpy as np

class SarsaAgent(AbstractAgent):
    """
    Here you will provide your implementation of SARSA method.
    You are supposed to implement train() method. If you want
    to, you can split the code in two phases - training and
    testing, but it is not a requirement.

    For SARSA explanation check AIMA book or Sutton and Burton
    book. You can choose any strategy and/or step-size function
    (learning rate) as long as you fulfil convergence criteria.
    """
    def __init__(self, env: BlackjackEnv, number_of_episodes: int):
        super(SarsaAgent, self).__init__(env, number_of_episodes)
        self.states_Qs = np.zeros((20, 5, 9, 10, 2, 2), dtype=int)

        # observe state
        self.hand_val = 21 - 2
        self.num_aces = 0
        self.num_cards = 3
        self.dealers_card_val = 4 - 1
        self.observable_state_values_hit = []
        self.observable_state_values_stick = []

    def train(self):
        discount_factor = 0.9
        for i in range(self.number_of_episodes):
            observation = self.env.reset()
            terminal = False
            reward = 0
            epsilon = 1 / (i + 1)
            while not terminal:
                action = self.eps_greedy(observation, epsilon)
                next_observation, reward, terminal, _ = self.env.step(action)
                hand_val, num_aces, num_cards, dealers_card_val = get_indexes(observation)

                self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][action][1] += 1  # increment the number of visits

                tdTarget = reward
                if not terminal:
                    tdTarget += discount_factor * self.greedy_q_value(next_observation)

                # calculate alpha based on the number of visits
                c = 5
                alpha = c / (c - 1 + self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][action][1])

                #update Q
                self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][action][0] += alpha*(tdTarget - self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][action][0])

                self.check_and_store_state(hand_val, num_aces, num_cards, dealers_card_val, action)

                observation = next_observation

    def check_and_store_state(self, hand_val, num_aces, num_cards, dealers_card_val, action):
        if hand_val == self.hand_val and num_aces == self.num_aces and num_cards == self.num_cards and dealers_card_val == self.dealers_card_val:
            if action == BlackjackAction.HIT.value:
                self.observable_state_values_hit.append(
                    self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][action][0])
            else:
                self.observable_state_values_hit.append(
                    self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][action][0])

    def get_observed_states(self):
        return self.observable_state_values_hit, self.observable_state_values_stick

    def eps_greedy(self, observation, epsilon):
        hand_val, num_aces, num_cards, dealers_card_val = get_indexes(observation)

        q_stick = self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][BlackjackAction.STAND.value][0]
        q_hit = self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][BlackjackAction.HIT.value][0]
        prob_a_max = 1 - epsilon * (1 - 1 / 2)
        if q_stick >= q_hit:
            return np.random.choice([BlackjackAction.STAND.value, BlackjackAction.HIT.value], p=[prob_a_max, 1 - prob_a_max])
        else:
            return np.random.choice([BlackjackAction.STAND.value, BlackjackAction.HIT.value], p=[1 - prob_a_max, prob_a_max])

    def greedy_q_value(self, observation):
        hand_val, num_aces, num_cards, dealers_card_val = get_indexes(observation)

        q_stick = self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][BlackjackAction.STAND.value][0]
        q_hit = self.states_Qs[hand_val][num_aces][num_cards][dealers_card_val][BlackjackAction.HIT.value][0]
        if q_stick >= q_hit:
            return q_stick
        else:
            return q_hit

    def get_hypothesis(self, observation: BlackjackObservation, terminal: bool, action: int) -> float:
        """
        Implement this method so that I can test your code. This method is supposed to return your learned Q value for
        particular observation and action.

        :param observation: The observation as in the game. Contains information about what the player sees - player's
        hand and dealer's hand.
        :param terminal: Whether the hands were seen after the end of the game, i.e. whether the state is terminal.
        :param action: Action for Q-value.
        :return: The learned Q-value for the given observation and action.
        """
        hand_val, num_aces, num_cards, dealers_card_val = get_indexes(observation)
        return self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][action][0]
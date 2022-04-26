from abstractagent import AbstractAgent
from blackjack import BlackjackObservation, BlackjackEnv, BlackjackAction
from carddeck import *
from state import *
import numpy as np


class TDAgent(AbstractAgent):
    """
    Implementation of an agent that plays the same strategy as the dealer.
    This means that the agent draws a card when sum of cards in his hand
    is less than 17.

    Your goal is to modify train() method to learn the state utility function
    and the get_hypothesis() method that returns the state utility function.
    I.e. you need to change this agent to a passive reinforcement learning
    agent that learns utility estimates using temporal difference method.
    """
    def __init__(self, env: BlackjackEnv, number_of_episodes: int):
        super(TDAgent, self).__init__(env, number_of_episodes)
        self.states_Us = np.zeros((20, 5, 9, 10, 2), dtype=int)

        #observe state
        self.hand_val = 21 - 2
        self.num_aces = 0
        self.num_cards = 3
        self.dealers_card_val = 4 - 1
        self.observable_state_values = []

    def train(self):
        discount_factor = 0.9
        for i in range(self.number_of_episodes):
            observation = self.env.reset()
            #state = observation2state(observation)

            terminal = False
            reward = 0
            while not terminal:
                # render method will print you the situation in the terminal
                # self.env.render()
                epsilon = 1/(i+1) #choose randomly with prob. epsilon
                action = np.random.choice([self.random_action(), self.receive_observation_and_get_action(observation, terminal)], p=[epsilon, 1 - epsilon])
                new_observation, reward, terminal, _ = self.env.step(action)
                # TODO your code will be very likely here
                hand_val_n, num_aces_n, num_cards_n, dealers_card_val_n = get_indexes(new_observation)
                hand_val, num_aces, num_cards, dealers_card_val = get_indexes(observation)
                self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][1] += 1  # increment the number of visits

                tdTarget = reward
                if not terminal:
                    tdTarget += discount_factor * self.states_Us[hand_val_n][num_aces_n][num_cards_n][dealers_card_val_n][0]

                #calculate alpha based on the number of visits
                c = 5
                alpha = (c)/(c - 1 + self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][1])

                update = alpha * (tdTarget - self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][0])
                self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][0] += update

                self.check_and_store_state(hand_val, num_aces, num_cards, dealers_card_val)

                observation = new_observation

            # self.env.render()

    def random_action(self):
        return np.random.choice([BlackjackAction.HIT.value, BlackjackAction.STAND.value])

    def get_observed_states(self):
        return self.observable_state_values

    def check_and_store_state(self, hand_val, num_aces, num_cards, dealers_card_val):
        if hand_val == self.hand_val and num_aces == self.num_aces and num_cards == self.num_cards and dealers_card_val == self.dealers_card_val:
            self.observable_state_values.append(self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][0])

    def receive_observation_and_get_action(self, observation: BlackjackObservation, terminal: bool) -> int:
        return BlackjackAction.HIT.value if observation.player_hand.value() < 17 else BlackjackAction.STAND.value

    def get_hypothesis(self, observation: BlackjackObservation, terminal: bool) -> float:
        """
        Implement this method so that I can test your code. This method is supposed to return your learned U value for
        particular observation.

        :param observation: The observation as in the game. Contains information about what the player sees - player's
        hand and dealer's hand.
        :param terminal: Whether the hands were seen after the end of the game, i.e. whether the state is terminal.
        :return: The learned U-value for the given observation.
        """
        hand_val, num_aces, num_cards, dealers_card_val = get_indexes(observation)
        return self.states_Us[hand_val][num_aces][num_cards][dealers_card_val][0]

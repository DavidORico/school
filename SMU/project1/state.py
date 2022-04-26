import torch
from carddeck import *
from blackjack import *

#state1
def get_card_id(card):
    index = 0
    if card.suit == Suit.CLUB:
        index = 0
    elif card.suit == Suit.DIAMOND:
        index = 13
    elif card.suit == Suit.HEART:
        index = 26
    elif card.suit == Suit.SPADES:
        index = 39

    index = index + card.rank.value - 1
    return index


def observation2state(observation):
    state = torch.zeros(55)
    for card in observation.player_hand.cards:
        state[get_card_id(card)] = 1
    state[52] = observation.player_hand.value()
    state[53] = get_card_id(observation.dealer_hand.cards[0])
    state[54] = observation.dealer_hand.cards[0].value()
    return state

#state3
def get_indexes(observation):
    num_aces = 0
    num_cards = len(observation.player_hand.cards) - 2  # player always has at least two cards
    hand_val = observation.player_hand.value() - 2  # value of hand is at least two
    dealers_card_val = observation.dealer_hand.cards[0].value() - 1  # the card has value of at least one
    for card in observation.player_hand.cards:
        if card.rank == Rank.ACE:
            num_aces = num_aces + 1
    return hand_val, num_aces, num_cards, dealers_card_val

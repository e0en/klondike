#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum
import random

from card import Card, Symbol, Rank


class CardStackName(Enum):
    TALON = 1
    FOUNDATION = 2
    TABLEAU = 3

    def __repr__(self):
        return self.name

    __str__ = __repr__


class CardStack:
    name: CardStackName

    def __init__(self):
        self.open_cards: list[Card] = []
        self.closed_cards: list[Card] = []


class Talon(CardStack):
    name = CardStackName.TALON

    def __init__(self):
        CardStack.__init__(self)

    def draw(self):
        if self.closed_cards:
            c = self.closed_cards.pop()
            self.open_cards += [c]
        elif self.open_cards:
            self.closed_cards = [x for x in self.open_cards]
            self.open_cards = []

    def __repr__(self):
        result = 'Talon('
        if self.closed_cards:
            result += '[CLOSED]*?, '
        if self.open_cards:
            result += str(self.open_cards[-1])
        else:
            result += '_'
        result += ')'
        return result

    __str__ = __repr__


class Foundation(CardStack):
    name = CardStackName.FOUNDATION

    def __init__(self):
        CardStack.__init__(self)

    def empty(self):
        return not bool(self.open_cards)

    def __repr__(self):
        result = 'Foundation('
        if self.open_cards:
            result += str(self.open_cards[-1])
        result += ')'
        return result

    __str__ = __repr__


class Tableau(CardStack):
    name = CardStackName.TABLEAU

    def __init__(self):
        CardStack.__init__(self)

    def empty(self):
        return not bool(self.open_cards + self.closed_cards)

    def __repr__(self):
        result = 'Tableau('
        if self.closed_cards:
            result += f'[CLOSED]*{len(self.closed_cards)}, '
        result += ', '.join([str(c) for c in self.open_cards])
        result += ')'
        return result

    __str__ = __repr__


class Board:
    def __init__(self):
        self.talon = Talon()
        self.foundation = [Foundation() for _ in range(4)]
        self.tableau = [Tableau() for _ in range(7)]

        deck = [Card(s, r) for s in Symbol for r in Rank
                if s != Symbol.UNKNOWN and r != Rank.UNKNOWN]
        random.shuffle(deck)
        for i, t in enumerate(self.tableau):
            for _ in range(i):
                t.closed_cards += [deck.pop()]
            t.open_cards += [deck.pop()]

        while deck:
            self.talon.closed_cards += [deck.pop()]

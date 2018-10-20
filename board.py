#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from card import Card, Symbol, Rank


class CardStack:
    def __init__(self):
        self.open_cards: list[Card] = []
        self.closed_cards: list[Card]  = []


class Talon(CardStack):
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
    def __init__(self):
        CardStack.__init__(self)

    def __repr__(self):
        result = 'Foundation('
        if self.open_cards:
            result += str(self.open_cards[-1])
        result += ')'
        return result

    __str__ = __repr__


class Tableau(CardStack):
    def __init__(self):
        CardStack.__init__(self)

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

        deck = [Card(s, r) for s in Symbol for r in Rank]
        random.shuffle(deck)
        for i, t in enumerate(self.tableau):
            for _ in range(i):
                t.closed_cards += [deck.pop()]
            t.open_cards += [deck.pop()]

        while deck:
            self.talon.closed_cards += [deck.pop()]

    def display(self):
        print('-' * 20)
        print(self.talon)
        print('')
        for f in self.foundation:
            print(f)
        print('')
        for t in self.tableau:
            print(t)
        print('-' * 20)


if __name__ == '__main__':
    board = Board()

    board.display()
    board.talon.draw()
    board.display()

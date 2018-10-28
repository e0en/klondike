#!/usr/bin/env python
# -*- coding: utf-8 -*-
from enum import Enum


class Symbol(Enum):
    UNKNOWN = -1
    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

    def __repr__(self):
        if self == Symbol.UNKNOWN:
            return '?'
        if self == Symbol.SPADES:
            return '\u2660'
        if self == Symbol.HEARTS:
            return '\u2661'
        if self == Symbol.DIAMONDS:
            return '\u2662'
        if self == Symbol.CLUBS:
            return '\u2663'

    __str__ = __repr__


class Color(Enum):
    UNKNOWN = -1
    RED = 1
    BLACK = 2


class Rank(Enum):
    UNKNOWN = -1
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    def __repr__(self):
        if self == Rank.UNKNOWN:
            return '?'
        elif 2 <= self.value <= 10:
            return str(self.value)
        else:
            return self.name[0]

    __str__ = __repr__


class Card:
    def __init__(self, symbol: Symbol, rank: Rank):
        self.symbol = symbol
        self.rank = rank
        if symbol in {Symbol.SPADES, Symbol.CLUBS}:
            self.color = Color.BLACK
        elif symbol in {Symbol.HEARTS, Symbol.DIAMONDS}:
            self.color = Color.RED
        else:
            self.color = Color.UNKNOWN

    def __repr__(self):
        return f'Card({self.symbol}{self.rank: >2})'

    @staticmethod
    def unknown():
        return Card(Symbol.UNKNOWN, Rank.UNKNOWN)

    __str__ = __repr__


if __name__ == '__main__':
    all_cards = [Card(s, r) for s in Symbol for r in Rank
                 if s != Symbol.UNKNOWN and r != Rank.UNKNOWN]
    for c in all_cards:
        print(c)

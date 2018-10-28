#!/usr/bin/env python
# -*- coding: utf-8 -*-
from board import Board
from board import CardStackName as csn
from card import Rank


def possible_from_locations(board: Board):
    result = []
    if board.talon.open_cards:
        result += [(csn.TALON, )]

    for i, f in enumerate(board.foundation):
        # no need to move a king card from foundation
        if not f.empty() and f.open_cards[-1].rank != Rank.KING:
            result += [(csn.FOUNDATION, i)]

    for i, t in enumerate(board.tableau):
        if not t.empty():
            for j in range(len(t.open_cards)):
                result += [(csn.TABLEAU, i, j)]

    return result


def possible_to_locations(from_location, board: Board):
    result = []

    if from_location[0] == csn.TALON:
        moving_cards = [board.talon.open_cards[-1]]

    elif from_location[0] == csn.FOUNDATION:
        foundation = board.foundation[from_location[1]]
        moving_cards = [foundation.open_cards[-1]]

    elif from_location[0] == csn.TABLEAU:
        tableau = board.tableau[from_location[1]]
        moving_cards = tableau.open_cards[from_location[2]:]

    if len(moving_cards) == 1 and from_location[0] != csn.FOUNDATION:
        card = moving_cards[0]
        for i, f in enumerate(board.foundation):
            if f.empty():
                if card.rank == Rank.ACE:
                    result += [(csn.FOUNDATION, i)]
                    break
                continue

            f_card = f.open_cards[-1]
            if (f_card.symbol == card.symbol and
                card.rank.value == f_card.rank.value + 1):
                result += [(csn.FOUNDATION, i)]
                break

    for i, t in enumerate(board.tableau):
        if from_location[0] == csn.TABLEAU and from_location[1] == i:
            continue

        card = moving_cards[0]

        if t.empty():
            if card.rank == Rank.KING:
                if (from_location[0] == csn.TABLEAU and
                    not board.tableau[from_location[1]].closed_cards):
                    continue
                result += [(csn.TABLEAU, i)]
            continue

        t_card = t.open_cards[-1]
        if t_card.rank == Rank.ACE:
            continue
        if (card.color != t_card.color and
            card.rank.value == (t_card.rank.value - 1)):
            result += [(csn.TABLEAU, i)]

    return result


def possible_moves(board: Board):
    result = ['draw']
    all_from = possible_from_locations(board)
    for f in all_from:
        result += [(f, t) for t in possible_to_locations(f, board)]
    return result


def is_finished(board: Board):
    for f in board.foundation:
        if f.empty():
            return False
        if f.open_cards[-1].rank != Rank.KING:
            return False
    return True


if __name__ == '__main__':
    board = Board()

    board.display()
    moves = possible_moves(board)
    print(moves)

    board.talon.draw()

    board.display()
    moves = possible_moves(board)
    print(moves)

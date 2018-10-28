#!/usr/bin/env python
# -*- coding: utf-8 -*-
from card import Card, Symbol, Rank
from board import Board, CardStack, CardStackName


def card_to_dict(card: Card):
    return {'symbol': card.symbol.name, 'rank': card.rank.name}


def dict_to_card(d):
    return Card(Symbol[d['symbol']], Rank[d['rank']])


def stack_to_dict(stack: CardStack):
    return {
        'closed_cards': len(stack.closed_cards),
        'open_cards': [card_to_dict(c) for c in stack.open_cards],
    }


def board_to_dict(board: Board):
    result = dict()
    result['talon'] = stack_to_dict(board.talon)
    result['foundation'] = [stack_to_dict(f) for f in board.foundation]
    result['tableau'] = [stack_to_dict(t) for t in board.tableau]

    return result


def dict_to_board(d):
    board = Board()

    talon = d['talon']
    board.talon.open_cards = [dict_to_card(c) for c in talon['open_cards']]
    board.talon.closed_cards = [Card.unknown()
                                for _ in range(talon['closed_cards'])]

    foundation = d['foundation']
    for i, f in enumerate(foundation):
        board.foundation[i].open_cards =\
            [dict_to_card(c) for c in f['open_cards']]
        board.foundation[i].closed_cards = \
            [Card.unknown() for _ in range(f['closed_cards'])]

    tableau = d['tableau']
    for i, t in enumerate(tableau):
        board.tableau[i].open_cards =\
            [dict_to_card(c) for c in t['open_cards']]
        board.tableau[i].closed_cards = \
            [Card.unknown() for _ in range(t['closed_cards'])]

    return board


def move_to_dict(move):
    if move == 'draw':
        return {'type': 'draw'}
    from_pos, to_pos = move
    result = {'type': 'move'}
    result['from'] = {'stack_type': from_pos[0].name}
    if len(from_pos) >= 2:
        result['from']['stack_index'] = from_pos[1]
    if len(from_pos) >= 3:
        result['from']['card_index'] = from_pos[2]

    result['to'] = {'stack_type': to_pos[0].name}
    if len(to_pos) >= 2:
        result['to']['stack_index'] = to_pos[1]

    return result


def dict_to_move(d):
    if d['type'] == 'draw':
        return 'draw'

    from_pos = [CardStackName[d['from']['stack_type']]]
    if 'stack_index' in d['from']:
        from_pos += [d['from']['stack_index']]
    if 'card_index' in d['from']:
        from_pos += [d['from']['card_index']]
    from_pos = tuple(from_pos)

    to_pos = [CardStackName[d['to']['stack_type']]]
    if 'stack_index' in d['to']:
        to_pos += [d['to']['stack_index']]
    to_pos = tuple(to_pos)

    return from_pos, to_pos

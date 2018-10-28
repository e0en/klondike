#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import rule
from board import Board
from board import CardStackName as csn
from serialize import board_to_dict, dict_to_move


def apply_move(move, board: Board):
    if move == 'draw':
        if board.talon.closed_cards:
            card = board.talon.closed_cards.pop()
            board.talon.open_cards += [card]
        else:
            board.talon.closed_cards = board.talon.open_cards[::-1]
            board.talon.open_cards = []
        return

    from_pos, to_pos = move

    if from_pos[0] == csn.TALON:
        card = board.talon.open_cards.pop()
        moving_cards = [card]
    elif from_pos[0] == csn.FOUNDATION:
        f = board.foundation[from_pos[1]]
        card = f.open_cards.pop()
        moving_cards = [card]
    elif from_pos[0] == csn.TABLEAU:
        t = board.tableau[from_pos[1]]
        moving_cards = t.open_cards[from_pos[2]:]
        t.open_cards = t.open_cards[:from_pos[2]]
        if not t.open_cards and t.closed_cards:
            new_open_card = t.closed_cards.pop()
            t.open_cards = [new_open_card]

    if to_pos[0] == csn.TALON:
        board.talon.open_cards += moving_cards
    elif to_pos[0] == csn.FOUNDATION:
        board.foundation[to_pos[1]].open_cards += moving_cards
    elif to_pos[0] == csn.TABLEAU:
        board.tableau[to_pos[1]].open_cards += moving_cards


class Server:
    def __init__(self):
        self.board: Board = Board()

    def send_board(self):
        return json.dumps(board_to_dict(self.board))

    def recv_move(self, move_json):
        move = dict_to_move(json.loads(move_json))
        if move not in rule.possible_moves(self.board):
            return {'status': 'fail'}

        apply_move(move, self.board)

        if rule.is_finished(self.board):
            return {'status': 'win'}
        else:
            return {'status': 'ok'}

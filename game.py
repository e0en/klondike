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


if __name__ == '__main__':
    from serialize import move_to_dict, dict_to_board

    server = Server()
    is_finished = False

    while not is_finished:
        board_json = server.send_board()
        board = dict_to_board(json.loads(board_json))

        print('talon: ' + str(board.talon.open_cards))
        for i, f in enumerate(board.foundation):
            print(f'foundation {i+1}: ' + str(f.open_cards))
        for i, t in enumerate(board.tableau):
            print(f'tableau {i+1}: ' + str(t.open_cards))

        moves = rule.possible_moves(board)

        for i, m in enumerate(moves):
            print(f'{i + 1}: {m}')

        user_input = input(f'choose (1~{len(moves)}) : ')
        if user_input == 'q':
            print('bye!')
            break
        try:
            move_idx = int(user_input) - 1
        except ValueError:
            print('wrong input.')
            continue
        if not (0 <= move_idx < len(moves)):
            print('wrong input.')
            continue

        move = moves[move_idx]
        move_json = json.dumps(move_to_dict(move))
        print(move_json)

        msg = server.recv_move(move_json)
        print(msg)

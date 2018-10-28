#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

import rule
from board import Board
from serialize import move_to_dict, dict_to_board
from server import Server


class Client:
    def __init__(self, server: Server):
        self.server = server
        self.board: Board = None

    def send_move(self, move):
        resp = self.server.recv_move(json.dumps(move))
        return resp

    def update(self):
        board_json = self.server.send_board()
        self.board = dict_to_board(json.loads(board_json))

    def choose_move(self):
        moves = rule.possible_moves(self.board)
        for i, m in enumerate(moves):
            print(f'{i + 1}: {m}')

        user_input = input(f'choose (1~{len(moves)}) : ')
        if user_input == 'q':
            print('bye!')
            return
        try:
            move_idx = int(user_input) - 1
        except ValueError:
            print('wrong input.')
            return
        if not (0 <= move_idx < len(moves)):
            print('wrong input.')
            return

        self.send_move(move_to_dict(moves[move_idx]))

    def draw(self):
        n_closed = len(self.board.talon.closed_cards)
        print(f'talon: {n_closed} ', end='')
        if self.board.talon.open_cards:
            print(self.board.talon.open_cards[-1])
        else:
            print('')

        for i, f in enumerate(self.board.foundation):
            print(f'foundation {i+1}: ', end='')
            if f.open_cards:
                print(f.open_cards[-1])
            else:
                print('')

        for i, t in enumerate(self.board.tableau):
            print(f'tableau {i+1}: {len(t.closed_cards)} {t.open_cards}')


if __name__ == '__main__':
    server = Server()

    client = Client(server)
    is_finished = False

    while not is_finished:
        client.update()
        client.draw()
        client.choose_move()

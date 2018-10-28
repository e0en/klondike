#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rule
from board import Board
from board import CardStackName as csn


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


if __name__ == '__main__':
    board = Board()
    while not rule.is_finished(board):
        moves = rule.possible_moves(board)
        if not moves:
            print('game over')
            break

        board.display()

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
        apply_move(move, board)

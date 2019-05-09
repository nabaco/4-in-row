#!/usr/bin/env python3
try:
    from ..envs import *
except (ImportError, ValueError):
    import os
    import sys
    parentdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    sys.path.insert(0, parentdir)
    from envs import *

import pytest


class TestEnv4InRow(object):
    def test_game(self):
        player1 = "d"
        player2 = "n"
        width = 4
        height = 2
        game = create_env('4-in-row', player1, player2, board_size=(height, width))
        assert game is not None, 'Failed to initialize environment'
        game.render()  # Manual check
        assert game.available_moves(player1) != []
        assert game.available_moves(player2) != []
        assert game.player_status(player1) == 0
        assert game.player_status(player2) == 0
        assert game.is_terminal_state() is False
        game.apply_action(player1, 1)
        game.apply_action(player2, 1)
        game.render()  # Manual check
        assert game.reset is not None
        game.render()  # Manual check

    def test_horizontal_win(self):
        player1 = "d"
        player2 = "n"
        width = 4
        height = 2
        game = create_env('4-in-row', player1, player2, board_size=(height, width))

        print(game.available_moves(player1))  # Test available moves in the beginning
        game.apply_action(player1, 0)
        game.apply_action(player2, 0)
        game.apply_action(player1, 1)
        game.apply_action(player2, 1)
        game.apply_action(player1, 2)
        game.apply_action(player2, 2)
        game.apply_action(player1, 3)

        assert game.available_moves(player1) == []
        assert game.available_moves(player2) == []
        assert game.player_status(player1) == 1
        assert game.player_status(player2) == -1
        assert game.is_terminal_state() is True
        assert game.apply_action(player2, 4) is None

    def test_vertical_win(self):
        player1 = "d"
        player2 = "n"
        width = 2
        height = 4
        game = create_env('4-in-row', player1, player2, board_size=(height, width))
        for h in range(3):
            game.apply_action(player1, 0)
            game.apply_action(player2, 1)
        game.apply_action(player1, 0)

        assert game.available_moves(player1) == []
        assert game.available_moves(player2) == []
        assert game.player_status(player1) == 1
        assert game.player_status(player2) == -1
        assert game.is_terminal_state() is True
        assert game.apply_action(player2, 4) is None

    def test_diagonal_win(self):
        player1 = "d"
        player2 = "n"
        width = 4
        height = 4
        game = create_env('4-in-row', player1, player2, board_size=(height, width))

        game.apply_action(player1, 0)
        game.apply_action(player2, 1)
        game.apply_action(player1, 1)
        game.apply_action(player2, 2)
        game.apply_action(player1, 1)
        game.apply_action(player2, 2)
        game.apply_action(player1, 2)
        game.apply_action(player2, 3)
        game.apply_action(player1, 3)
        game.apply_action(player2, 3)
        game.apply_action(player1, 3)

        assert game.available_moves(player1) == []
        assert game.available_moves(player2) == []
        assert game.player_status(player1) == 1
        assert game.player_status(player2) == -1
        assert game.is_terminal_state() is True
        assert game.apply_action(player2, 4) is None

    def test_reverse_diagonal_win(self):
        player1 = "d"
        player2 = "n"
        width = 4
        height = 4
        game = create_env('4-in-row', player1, player2, board_size=(height, width))

        game.apply_action(player1, 3)
        game.apply_action(player2, 2)
        game.apply_action(player1, 2)
        game.apply_action(player2, 1)
        game.apply_action(player1, 2)
        game.apply_action(player2, 1)
        game.apply_action(player1, 1)
        game.apply_action(player2, 0)
        game.apply_action(player1, 0)
        game.apply_action(player2, 0)
        game.apply_action(player1, 0)

        assert game.available_moves(player1) == []
        assert game.available_moves(player2) == []
        assert game.player_status(player1) == 1
        assert game.player_status(player2) == -1
        assert game.is_terminal_state() is True
        assert game.apply_action(player2, 4) is None

    def test_is_terminal_state(self):
        player1 = "d"
        player2 = "n"
        width = 2
        height = 2
        game = create_env('4-in-row', player1, player2, board_size=(height, width))

        game.apply_action(player1, 0)
        game.apply_action(player2, 0)
        game.apply_action(player1, 1)
        game.apply_action(player1, 1)

        assert game.available_moves(player1) == []
        assert game.available_moves(player2) == []
        assert game.player_status(player1) == 0
        assert game.player_status(player2) == 0
        assert game.is_terminal_state() is True
        assert game.apply_action(player2, 4) is None


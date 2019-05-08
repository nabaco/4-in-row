#!/usr/bin/env python3
try:
    from ..envs import *
except ImportError:
    import os
    import sys
    sys.path.insert(0, os.path.abspath('..'))
    from envs import *

import pytest


class TestEnv4InRow(object):
    def play(self, player, action):
        if not self.game.apply_action(player, action):
            print("Wrong action!")
        status = self.game.player_status(self.player1)
        assert status is not None
        if status == 1:
            print("self.player1 won!")
        elif status == -1:
            print("self.player1 lost!")
        if self.game.is_terminal_state():
            print("self.game over(c)! Board is full!")

    def test_horizontal_win(self):
        self.player1 = "d"
        self.player2 = "n"
        self.width = 7
        self.height = 6
        self.game = create_env('4-in-row', self.player1, self.player2, board_size=(self.height, self.width))
        assert self.game is not None, 'Failed to initialize environment'
        self.game.render()  # Test initial rendering
        print(self.game.available_moves(self.player1))  # Test available moves in the beginning
        for h in range(self.height):  # Test a horizontal winning situation
            c = 0
            while self.game.player_status(self.player1) != 1 and c < self.width-1:
                self.play(self.player1, c)
                self.play(self.player2, c)
                c += 1
        self.game.render()  # Test final rendering

    def test_vertical_win(self):
        self.player1 = "d"
        self.player2 = "n"
        self.width = 7
        self.height = 6
        self.game = create_env('4-in-row', self.player1, self.player2, board_size=(self.height, self.width))
        assert self.game is not None, 'Failed to initialize environment'
        self.game.reset()
        for h in range(self.height):  # Test a vertical winning situation
            c = 0
            while self.game.player_status(self.player1) != 1 and c < self.width-1:
                self.play(self.player1, c)
                self.play(self.player2, c+1)
        self.game.render()

    def test_diagonal_win(self):
        self.player1 = "d"
        self.player2 = "n"
        self.width = 7
        self.height = 6
        self.game = create_env('4-in-row', self.player1, self.player2, board_size=(self.height, self.width))
        assert self.game is not None, 'Failed to initialize environment'
        self.game.reset()
        for h in range(self.height):  # Test a diagonal winning situation
            c = 0
            while self.game.player_status(self.player1) != 1 and c < self.width-1:
                self.play(self.player1, c)
                for o in range(c):
                    self.play(self.player2, c+1)
                c += 1
        self.game.render()

    def test_reverse_diagonal_win(self):
        self.player1 = "d"
        self.player2 = "n"
        self.width = 7
        self.height = 6
        self.game = create_env('4-in-row', self.player1, self.player2, board_size=(self.height, self.width))
        assert self.game is not None, 'Failed to initialize environment'
        self.game.reset()
        for h in range(self.height):  # Test a reverse diagonal winning situation
            c = self.width
            while self.game.player_status(self.player1) != 1 and c > 1:
                self.play(self.player1, c)
                for o in range(self.width-c):
                    self.play(self.player2, c-1)
                c -= 1
        self.game.render()

    def test_is_terminal_state(self):
        # TODO: add a test for a full board - self.game.is_terminal_state()
        pass


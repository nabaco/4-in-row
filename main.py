#!/usr/bin/env python3

from envs import create_env
from agents import Agent


class DummyAgent(Agent):

    def choose_action(self, env):
        pass


player1 = DummyAgent('p1')
player2 = DummyAgent('p2')
width = 8
height = 6
game = create_env('4-in-row', player1, player2, board_size=(height, width))


def play(player, action):
    if not game.apply_action(player, action):
        print("Wrong action!")
    status = game.player_status(player1)
    if status == 1:
        print("Player1 won!")
    if status == -1:
        print("Player1 lost!")
    if game.is_terminal_state():
        print("Game over(c)! Board is full!")


game.render()  # Test initial rendering
print(game.available_moves(player1))  # Test available moves in the beginning
for h in range(height):  # Test a horizontal winning situation
    c = 0
    while game.player_status(player1) != 1 and c < width-1:
        play(player1, c)
        play(player2, c)
        c += 1
game.render()  # Test final rendering

game.reset()
for h in range(height):  # Test a vertical winning situation
    c = 0
    while game.player_status(player1) != 1 and c < width-1:
        play(player1, c)
        play(player2, c+1)
game.render()

game.reset()
# THIS `for h in range(height)` IS REDUNDANT!!!
for h in range(height):  # Test a diagonal winning situation
    c = 0
    while game.player_status(player1) != 1 and c < width-1:
        play(player1, c)
        for o in range(c-1):
            play(player2, c+1)
            play(player1, 'pass')
        play(player2, 'pass')
        c += 1
game.render()

game.reset()
# THIS `for h in range(height)` IS REDUNDANT!!!
for h in range(height):  # Test a reverse diagonal winning situation
    c = width-1
    while game.player_status(player1) != 1 and c > 1:
        play(player1, c)
        for o in range(width-c):
            play(player2, c-1)
            play(player1, 'pass')
        play(player2, 'pass')
        c -= 1
game.render()

# TODO: add a test for a full board - game.is_terminal_state()
import sys

try:
    from engine import GameEngine
    from objects import *
    import pygame
    import gamestate as g
except ImportError as e:
    print("Could not load: {}".format(e))
    sys.exit(2)

if __name__ == "__main__":
    game = GameEngine()
    game.run()

import sys

try:
    from engine import GameEngine
    from objects import *
    import pygame
    import gamestate as g
except ImportError, e:
    print "Could not load: {}".format(e)
    sys.exit(2)

"""
    #TODO:
    * Need: add delta time updating for FPS smoothing
    * Need: Ability to restart at game end
    * Bonus: make ball a circle instead of rectangle
    * Bonus: Add some music
    * Bonus: Add some sound fx
    * Bonus: Add Start screen
"""

if __name__ == "__main__":
    game = GameEngine()
    game.run()

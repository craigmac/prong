""" Game state globals and variable globals that most if not all modules
    will use.
"""

import os.path


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
SIZE = WIDTH, HEIGHT = 640, 480
GAME_DIR = os.path.split(os.path.abspath(__file__))[0]
BALL_SIZE = (8, 8)
TITLE = "Prong!"
PLAYER1_START = (20, 215)
PLAYER2_START = (610, 215)
p1scrx, p1scry = 200, 25
p2scrx, p2scry = 400, 25

# Init global objects that will be modified by GameEngine.__init__()
# initially, and then by other modules/functions as game runs
done = False
screen = None
screen_rect = None
paddle_sprite_list = None
player1 = None
player2 = None
ball = None
# ball_grp = None
font = None
clock = None
vector = [0, 0]  # Movement of ball, e.g. [2, 2]
game_score = [0, 0]  # player1, player2 score
win_score = 10  # Number to reach to win
paddle_sound = None

# Font surfaces and Rects to display user scores
p1score_surf = None
p2score_surf = None
p1score_rect = None
p2score_rect = None

# Other drawings
centerline = None
centerline_rect = None

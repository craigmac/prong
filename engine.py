"""engine.py Engine of the game resides here."""

import os

import pygame

import prong.gamestate as g
from .objects import Ball, Paddle


class GameEngine(object):
    """ Base class to inherit from for a Game class. """

    def __init__(self):
        """ Setup game and record initial global game states. """

        # Pygame setup and initial states
        pygame.mixer.pre_init()  # Some platforms require this first to work
        pygame.init()
        pygame.mixer.init()
        g.screen = pygame.display.set_mode(g.SIZE)
        g.screen_rect = g.screen.get_rect()
        pygame.display.set_caption(g.TITLE)
        g.clock = pygame.time.Clock()
        g.done = False

        # Centerline -- using Surface to blit easy rather than redraw it
        # each cycle in game loop with pygame.draw function
        g.centerline = pygame.Surface((2, g.screen_rect.height))
        g.centerline.fill(g.WHITE)
        g.centerline_rect = g.centerline.get_rect()
        g.centerline_rect.x = g.screen_rect.width / 2

        # Load font and draw initial score (0 - 0)
        g.font = pygame.font.SysFont("terminal", 144)
        self.draw_score()

        g.p1score_surf = g.font.render(str(g.game_score[0]), False, g.WHITE)
        g.p1score_rect = g.p1score_surf.get_rect()

        g.p2score_surf = g.font.render(str(g.game_score[1]), False, g.WHITE)
        g.p2score_rect = g.p2score_surf.get_rect()

        # Load sounds
        g.paddle_sound = self.load_sound(os.path.join(os.curdir, 'assets',
                                                      'music', 'ping.wav'))

        # Create game objects we need in globals.py for import other places
        g.paddle_sprite_list = pygame.sprite.Group()
        g.player1 = Paddle(g.WHITE, g.PLAYER1_START)
        g.player2 = Paddle(g.WHITE, g.PLAYER2_START)
        g.paddle_sprite_list.add(g.player1)
        g.paddle_sprite_list.add(g.player2)
        g.ball = Ball(g.WHITE, g.BALL_SIZE)

        print("GameEngine.__init__(): Complete.")

    def load_sound(self, sound_file):
        """Return a pygame.mixer.Sound object or raise error."""

        try:
            sound = pygame.mixer.Sound(sound_file)
            return sound
        except pygame.error:
            print("Warning, unable to load, {}".format(sound_file))

    def draw_score(self):
        """Draw current score to the screen"""

        # We need to grab current int from game_score each time, because
        # it is frozen to surf once updated
        g.p1score_surf = g.font.render(str(g.game_score[0]), False, g.WHITE)
        g.p1score_rect = g.p1score_surf.get_rect()

        g.p2score_surf = g.font.render(str(g.game_score[1]), False, g.WHITE)
        g.p2score_rect = g.p2score_surf.get_rect()

        # Blit to screen
        g.screen.blit(g.p1score_surf, (g.p1scrx, g.p1scry))
        g.screen.blit(g.p2score_surf, (g.p2scrx, g.p2scry))

    def load_image(self, src):
        """Load an image from disk, convert it and return image its Rect."""

        pass

    def run(self):
        """Main game loop. Call to run instance of game."""

        while not g.done:
            # new movement
            # dt = g.clock.tick(60) / 1000.0
            g.clock.tick(60)
            g.screen.fill(g.BLACK)
            g.screen.blit(g.centerline, g.centerline_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    g.done = True

                # Key pressed down
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        g.player2.change[1] = -5
                    elif event.key == pygame.K_DOWN:
                        g.player2.change[1] = 5
                    elif event.key == pygame.K_w:
                        g.player1.change[1] = -5
                    elif event.key == pygame.K_s:
                        g.player1.change[1] = 5
                # Key un-pressed, reset change values
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        g.player2.change = [0, 0]
                    elif event.key == pygame.K_DOWN:
                        g.player2.change = [0, 0]
                    elif event.key == pygame.K_w:
                        g.player1.change = [0, 0]
                    elif event.key == pygame.K_s:
                        g.player1.change = [0, 0]
            # Logic updates
            # new movement
            # g.ball.update(dt)
            g.ball.update()
            g.screen.blit(g.ball.image, g.ball.rect)
            # new movement
            # g.paddle_sprite_list.update(dt)
            g.paddle_sprite_list.update()

            # Drawing
            g.paddle_sprite_list.draw(g.screen)
            self.draw_score()
            pygame.display.update()

        # Loop broken, done = True
        pygame.quit()

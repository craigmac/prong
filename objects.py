import pygame
import random
import gamestate as g
import sys
import time


class Paddle(pygame.sprite.Sprite):
    """ Returns Paddle object for player control. """

    def __init__(self, colors, position):
        """ 3-tuple of RGB colors for a Paddle and a 2-tuple x,y position. """

        pygame.sprite.Sprite.__init__(self)

        # No initial movement, paddle is still
        self.change_y = 0

        # Set size and color
        self.image = pygame.Surface((10, 50))
        self.image.fill(colors)
        self.rect = self.image.get_rect()

        # Position and vectors
        self.rect.x = position[0]
        self.rect.y = position[1]

        self.change = [0, 0]  # Initial x,y

    # New movement
    # def update(self, dt):
    def update(self):
        """ Move the paddle details with change array of x,y.

        We check here if there is a collision with the ball first before
        moving, because if we don't there are situations where the pad can
        move over top of the ball position before the next frame and the ball
        behaves bizarrely, even getting stuck 'inside' the paddle because it
        keeps registering collisions and reversing position.
        """

        # Move up/down by checking change_y value
        # when user lets up on key, this is changed back to 0 to stop movement
        #self.rect.y += self.change[1]

        # Collision with top/bottom border of screen
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > g.screen_rect.bottom:
            self.rect.bottom = g.screen_rect.bottom

        if not self.rect.colliderect(g.ball.rect):
            # We can move freely this frame, so move
            #TODO: new movement
            # self.rect.y += self.change[1] * dt
            self.rect.y += self.change[1]
        else:  # Colliding with ball, check if is top or bottom of ball
            if g.ball.vector[1] > 0:  # Ball moving down
                # Don't allow paddle to overlap
                self.rect.top = g.ball.rect.bottom
            elif g.ball.vector[1] < 0:  # Ball moving up
                self.rect.bottom = g.ball.rect.top


class Ball(pygame.sprite.Sprite):
    """ Returns Ball object that bounces around play area. """

    def __init__(self, colors, size):
        """ Create a ball object with using color tuple and position tuple. """

        pygame.sprite.Sprite.__init__(self)  # Pygame required

        # Set size, color, vector
        self.image = pygame.Surface(size)
        self.image.fill(colors)

        self.rect = self.image.get_rect()
        self.rect.center = g.screen_rect.center

        # Initial movement
        self.vector = self.get_rand_vector()  # e.g., (-2, 2) down-left
        self.hit = False

    #TODO: new movement
    # def update(self, dt):
    def update(self):
        """ Move the ball. Called by pygame.sprite.Group.update()

        Calls move_axis method with an x-axis value first, then calls it again
        with the y-axis vector. This is a strategy to prevent some glitches
        where multiple axis are colliding at once, leading to some weird bugs.
        """

        # Move x-axis first
        #TODO: new movement
        # self.move_axis(self.vector[0], 0) * dt
        self.move_axis(self.vector[0], 0)
        # Now move y-axis
        #TODO: new movement
        # self.move_axis(self.vector[1]) * dt
        self.move_axis(0, self.vector[1])

    def move_axis(self, xchange, ychange):
        """Move ball object in a direction and test for collisions.
        Used to move one axis at a time. Call this method twice, once with
        x-axis vector, and then call this method again with y-axis vector. This
        also speeds up the ball by 1 each time it is hit by a paddle, by
        incrementing the vectors.

        E.g., To move 3 px to right: self.move_axis(self.vector[0], 0)

        Ball object's hit attribute is set to False when initialized, and this
        is what is checked on each movement to determine whether to check for
        collisions along either axis.

        In the game loop code the Ball.update() is called first and then
        the Paddle.update() is called next. The Paddle.update() methods check
        if colliding with Ball before moving, to avoid moving the paddle
        'over' the ball and causing bugs in the next frame when Ball.update()
        runs again.
        """

        # X-axis value given
        if xchange:
            self.rect.x += xchange

            if not self.hit:
                # First check if scored
                if self.rect.right >= g.screen_rect.right:
                    self.hit = True
                    self.vector = [0, 0]
                    self.update_score(0)
                elif self.rect.left <= g.screen_rect.left:
                    self.hit = True
                    self.vector = [0, 0]
                    self.update_score(1)
                # Check paddle collisions
                elif self.rect.colliderect(g.player1.rect):
                    if g.paddle_sound:
                        g.paddle_sound.play()
                    self.hit = True
                    self.rect.left = g.player1.rect.right
                    self.vector[0] = -(self.vector[0] - 1)
                    if self.vector[1] < 0:
                        self.vector[1] -= 1
                    else:
                        self.vector[1] += 1
                elif self.rect.colliderect(g.player2.rect):
                    if g.paddle_sound:
                        g.paddle_sound.play()
                    self.hit = True
                    self.rect.right = g.player2.rect.left
                    self.vector[0] = -(self.vector[0] + 1)
                    if self.vector[1] < 0:
                        self.vector[1] -= 1
                    else:
                        self.vector[1] += 1
            else:  # Currently hit, see if we can change it to False yet
                if not self.rect.colliderect(g.player1.rect) or \
                        not self.rect.colliderect(g.player2.rect):
                    self.hit = False

        # Y-axis value given
        elif ychange:
            self.rect.y += ychange

            if not self.hit:
                # First check top/bottom screen collisions
                if self.rect.top <= g.screen_rect.top:
                    self.rect.top = g.screen_rect.top
                    self.vector[1] = -(self.vector[1])
                elif self.rect.bottom >= g.screen_rect.bottom:
                    self.rect.bottom = g.screen_rect.bottom
                    self.vector[1] = -(self.vector[1])
                # Check paddle collisions
                elif ychange > 0:  # Moving down
                    if self.rect.colliderect(g.player1.rect):
                        if g.paddle_sound:
                            g.paddle_sound.play()
                        self.hit = True
                        self.rect.bottom = g.player1.rect.top
                        self.vector[1] = -(self.vector[1] - 1)
                        self.vector[0] -= 1
                    elif self.rect.colliderect(g.player2.rect):
                        if g.paddle_sound:
                            g.paddle_sound.play()
                        self.hit = True
                        self.rect.bottom = g.player2.rect.top
                        self.vector[1] = -(self.vector[1] - 1)
                        self.vector[0] += 1
                elif ychange < 0:  # Moving up
                    if self.rect.colliderect(g.player1.rect):
                        if g.paddle_sound:
                            g.paddle_sound.play()
                        self.hit = True
                        self.rect.top = g.player1.rect.bottom
                        self.vector[1] = -(self.vector[1] - 1)
                        self.vector[0] -= 1
                    elif self.rect.colliderect(g.player2.rect):
                        if g.paddle_sound:
                            g.paddle_sound.play()
                        self.hit = True
                        self.rect.top = g.player2.rect.bottom
                        self.vector[1] -= 1
                        self.vector[0] += 1
            else:  # Current hit = True, see if we set to False yet
                if not self.rect.colliderect(g.player1.rect) or \
                        not self.rect.colliderect(g.player2.rect):
                    self.hit = False

    def get_rand_vector(self):
        """Return a random direction for both x and y starting direction. """

        left_right = random.choice([-2, 2])  # -2 is left
        up_down = random.choice([-2, 2])  # -2 is up
        return [left_right, up_down]

    def reset(self):
        """Resets ball to middle of screen and starts ball moving again."""

        self.rect.center = g.screen_rect.center
        g.screen.blit(self.image, g.screen_rect.center)
        g.screen.blit(g.p1score_surf, (g.p1scrx, g.p1scry))
        g.screen.blit(g.p2score_surf, (g.p2scrx, g.p2scry))
        g.paddle_sprite_list.draw(g.screen)
        pygame.display.flip()
        # Pause ball
        self.hit = False
        time.sleep(1)
        self.vector = self.get_rand_vector()

    def update_score(self, player_to_update=None):
        """Check current scores and update them."""

        # Update score
        if player_to_update == 0:
            g.game_score[0] += 1
            print("Player 1 scored. Current Score : {}-{}".format(
                g.game_score[0], g.game_score[1]))
        elif player_to_update == 1:
            g.game_score[1] += 1
            print("Player 2 scored. Current Score : {}-{}".format(
                g.game_score[0], g.game_score[1]))

        # Check if game won
        if g.game_score[0] >= g.win_score:
            print("Player 1 won the game.")
            g.done = True
        elif g.game_score[1] >= g.win_score:
            print("Player 2 won the game.")
            g.done = True
        else:
            self.reset()

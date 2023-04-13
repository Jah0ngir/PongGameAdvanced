import pygame
from sys import exit
import random


# Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_position, y_position):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_position, y_position))


class Player(Block):
    def __init__(self, path, x_position, y_position, speed):
        super().__init__(path, x_position, y_position)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()


def ball_animation():
    # assigning global variable
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, pong_sound, score_sound
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= height:
        pygame.mixer.Sound.play(pong_sound)
        ball_speed_y *= -1

    # Player score
    if ball.left <= 0:
        pygame.mixer.Sound.play(score_sound)
        player_score += 1
        score_time = pygame.time.get_ticks()

    # Opponent score
    if ball.right >= width:
        pygame.mixer.Sound.play(score_sound)
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        pygame.mixer.Sound.play(pong_sound)
        if abs(ball.left - opponent.right) < 10:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height


def opponent_animation():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height:
        opponent.bottom = height


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (width / 2, height / 2)

    if current_time - score_time < 700:
        number_three = game_font.render('3', False, light_grey)
        screen.blit(number_three,
                    (width / 2 - 10, height / 2 + 20))  # 10 from center to left and 20 from center to bottom

    if 700 < current_time - score_time < 1400:
        number_two = game_font.render('2', False, light_grey)
        screen.blit(number_two, (width / 2 - 10, height / 2 + 20))

    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render('1', False, light_grey)
        screen.blit(number_one, (width / 2 - 10, height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


# Initial setup
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
clock = pygame.time.Clock()

# Set up main screen window
width = 1100
height = 770
screen = pygame.display.set_mode((width, height))
# Setting name 
pygame.display.set_caption('Pong For Final')

# Game Rectangles
ball = pygame.Rect(width / 2 - 15, height / 2 - 15, 30, 30)
player = pygame.Rect(width - 20, height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, height / 2 - 70, 10, 140)

# Colors
background_color = pygame.Color('blue')
light_grey = (200, 200, 200)

# Game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# Sound
pong_sound = pygame.mixer.Sound('sounds\pong.ogg')
score_sound = pygame.mixer.Sound('sounds\score.ogg')

# Score timer
score_time = True

while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # checking if user press x button
            pygame.quit()  # unitialize the pygame
            exit()  # terminate the game

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 7
            if event.key == pygame.K_UP:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            if event.key == pygame.K_UP:
                player_speed += 7

    ball_animation()
    player_animation()
    opponent_animation()

    # Components
    screen.fill(background_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.rect(screen, light_grey, opponent)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.aaline(screen, light_grey, (width / 2, 0), (width / 2, height))

    if score_time:
        ball_restart()

    player_text = game_font.render(f'{player_score}', False, light_grey)
    screen.blit(player_text, (580, 385))

    opponent_text = game_font.render(f'{opponent_score}', False, light_grey)
    screen.blit(opponent_text, (500, 385))

    # Updating the window
    pygame.display.flip()
    clock.tick(60)

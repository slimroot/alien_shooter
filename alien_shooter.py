import sys
import pygame
import random
import math
from pygame import mixer

pygame.init()
mixer.init()
screen = pygame.display.set_mode((700, 450))
bg_colour = (230, 230, 230)
pygame.display.set_caption(" Project I")
icon = pygame.image.load("logo.png")
pygame.display.set_icon(icon)
player = pygame.image.load("spaceship.png")
player = pygame.transform.scale(player, (42, 42))
playerX = 335
playerY = 400
player_change = 0

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (700, 450))

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Setting up an enemy
# monster = pygame.image.load("monster.png")
# monster = pygame.transform.scale(monster, (35, 35))
# enemy_x_position = random.randint(0, 700)
# enemy_y_position = random.randint(0, 30)
# enemyX_change = 0.2
# enemyY_change = 40

# Adding bullets to the ship
bullet = pygame.image.load("bullet.png")
bullet = pygame.transform.scale(bullet, (30, 30))
bullet_x_position = 0
bullet_y_position = 380
bulletY_change = 0.5
bullet_state = "ready"

# Multiple enemies
monster = []
enemy_x_position = []
enemy_y_position = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 5

for enemy in range(number_of_enemies):
    monster = pygame.transform.scale(pygame.image.load("monster.png"), (35, 35))
    enemy_x_position.append(random.randint(0, 700))
    enemy_y_position.append(random.randint(0, 30))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
score_x = 10
score_y = 10


def get_score():
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (score_x, score_y))


# Displays enemy on the screen
def get_spaceship(x, y):
    screen.blit(player, (x, y))


# Displays enemy on the screen
def get_enemy(x, y):
    screen.blit(monster, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 5, y))


def enemy_bullet_collision_detection(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(bullet_x - enemy_x, 2) + math.pow(bullet_y - enemy_y, 2))
    if distance <= 30:
        return True
    else:
        return False


def enemy_player_collision_detection(enemy_x, enemy_y, player_x, player_y):
    distance = math.sqrt(math.pow(player_x - enemy_x, 2) + math.pow(player_y - enemy_y, 2))
    if distance <= 30:
        return True
    else:
        return False


def get_failed_msg():
    over_font = pygame.font.Font("freesansbold.ttf", 35)
    failed_text = over_font.render("You Failed! Try Again.", True, (255, 255, 255))
    screen.blit(failed_text, (300, 180))


while True:
    # Setting up background color
    screen.fill(bg_colour)

    screen.blit(background, (0, 0))
    get_score()

    # Looping through the event during the session
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_change = -0.3
            elif event.key == pygame.K_RIGHT:
                player_change = +0.3
            elif event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x_position = playerX
                    fire_bullet(bullet_x_position, bullet_y_position)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_change = 0

    # Checks if the spaceship is out of boundary or not
    if playerX <= 0:
        playerX = 0
    elif playerX >= 658:
        playerX = 658

    playerX += player_change
    get_spaceship(playerX, playerY)

    for i in range(number_of_enemies):
        if enemy_y_position[i] > 250:
            get_failed_msg()
            break
        if enemy_x_position[i] <= 0:
            enemyX_change[i] = +0.2
            enemy_y_position[i] += enemyY_change[i]
        elif enemy_x_position[i] >= 658:
            enemyX_change[i] = -0.2
            enemy_y_position[i] += enemyY_change[i]

        enemy_x_position[i] += enemyX_change[i]
        get_enemy(enemy_x_position[i], enemy_y_position[i])

        if bullet_state == "fire":
            fire_bullet(bullet_x_position, bullet_y_position)
            bullet_y_position -= bulletY_change

        if bullet_y_position <= 0:
            bullet_y_position = 380
            bullet_state = "ready"

        enemy_bullet_collision = enemy_bullet_collision_detection(enemy_x_position[i], enemy_y_position[i],
                                                                  bullet_x_position, bullet_y_position)

        if enemy_bullet_collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_y_position = 380
            enemy_x_position[i] = random.randint(0, 700)
            enemy_y_position[i] = random.randint(0, 30)
            bullet_state = "ready"
            score_value += 1

    pygame.display.flip()

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
from random import randint
from os import listdir

pygame.init()
FPS = pygame.time.Clock()
screen = wigth, heigth = 800, 600
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
font = pygame.font.SysFont('Helvetica', 20)

main_surface = pygame.display.set_mode(screen)
pygame.display.set_caption("SUPER BALL")
# ball = pygame.Surface((20, 20))
# ball.fill(WHITE)
IMGS_PATH = 'images/goose'
ball_imgs = [pygame.image.load(
    IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = ball_imgs[0]
ball_rect = pygame.Rect(ball.get_rect())
ball_speed = 4

bg = pygame.transform.scale(pygame.image.load(
    'images/background.png').convert(), screen)
bgx = 0
bgx2 = bg.get_width()
bg_speed = 2


def create_enemy():
    enemy = pygame.image.load('images/enemy.png').convert_alpha()
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    enemy_rect = pygame.Rect(wigth, randint(0, heigth), *enemy.get_size())
    enemy_speed = randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(GREEN)
    bonus = pygame.image.load('images/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(randint(100, wigth-100), 0, *bonus.get_size())
    bonus_speed = randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

enemies = []
bonuses = []
scores = 0
img_index = 0

is_working = True
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            # if len(bonuses) == 0:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(ball_imgs):
                img_index = 0
            ball = ball_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    # main_surface.fill(BLACK)
    # main_surface.blit(bg, (0, 0))
    bgx -= bg_speed
    bgx2 -= bg_speed

    if bgx < - bg.get_width():
        bgx = bg.get_width()
    if bgx2 < - bg.get_width():
        bgx2 = bg.get_width()

    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))

    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render(str(scores), True, RED), (wigth - 30, 5))

    for enemy in enemies:
        main_surface.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(-enemy[2], 0)
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            is_working = False
    for bonus in bonuses:
        main_surface.blit(bonus[0], bonus[1])
        bonus[1] = bonus[1].move(0, bonus[2])
        if bonus[1].bottom > heigth:
            bonuses.pop(bonuses.index(bonus))
        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= heigth:
        ball_rect = ball_rect.move(0, ball_speed)
    if pressed_keys[K_UP] and not ball_rect.top <= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    if pressed_keys[K_RIGHT] and not ball_rect.right >= wigth:
        ball_rect = ball_rect.move(ball_speed, 0)
    if pressed_keys[K_LEFT] and not ball_rect.left <= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    pygame.display.flip()

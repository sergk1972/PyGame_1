import sqlite3
from sqlite3 import Error
import pygame
import pygame_textinput
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, KEYDOWN, K_RETURN
from random import randint
from os import listdir
import sys
# from sqlitefunc import SqliteActions


pygame.init()
FPS = pygame.time.Clock()
screen = wigth, heigth = 800, 600
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
font = pygame.font.SysFont('Helvetica', 20, True)
font_big = pygame.font.SysFont('Helvetica', 25, True)

main_surface = pygame.display.set_mode(screen)
pygame.display.set_caption("SUPER GOOSE (Супер гусь)")
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


def sql_connection():  # db_file  creating and establishing connection
    try:
        db = sqlite3.connect('database.db')
        return db
    except Error as ex:
        print(ex)


def sql_table_create(db):  # database table creating
    try:
        cursor_sql = db.cursor()
        cursor_sql.execute(f"CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                           f"name TEXT DEFAULT 'empty_space', score INTEGER DEFAULT 'empty_space') ")
        db.commit()
    except Error as ex:
        print(ex)


def sql_table_delete(db):  # database table creating
    try:
        cursor_sql = db.cursor()
        cursor_sql.execute(f"DROP table if exists players")
        db.commit()
    except Error as ex:
        print(ex)


def sql_insert_one(db, name, score):
    try:
        cursor_sql = db.cursor()
        cursor_sql.execute(
            f'INSERT INTO players(name, score) VALUES(?, ?)', (name, score))
        db.commit()
    except Error as ex:
        print(ex)


def sql_fetch(db):  # show data
    try:
        cursor_sql = db.cursor()
        cursor_sql.execute(
            f'SELECT name, score FROM players ORDER BY score DESC LIMIT 8')
        data = cursor_sql.fetchall()
        return data
    except Error as ex:
        print(ex)


def create_enemy():
    enemy = pygame.image.load('images/enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(wigth, randint(
        50, heigth - 50), *enemy.get_size())
    enemy_speed = randint(3, 5)
    return [enemy, enemy_rect, enemy_speed]


def create_bonus():
    bonus = pygame.image.load('images/bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(
        randint(100, wigth-100), -150, *bonus.get_size())
    bonus_speed = randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]


db = sql_connection()
sql_table_create(db)


def start_game():
    name: str = None
    textinput = pygame_textinput.TextInputVisualizer()

    pygame.key.set_repeat(200, 25)
    while name == None:
        FPS.tick(60)
        # main_surface = pygame.display.set_mode((800, 600))
        s_game = pygame.image.load('images/SUPER GOOSE.png').convert_alpha()
        s_game_rect = s_game.get_rect()  # pygame.Rect(150, 250, *g_over.get_size())
        main_surface_rect = main_surface.get_rect()
        s_game_rect.centerx = main_surface_rect.centerx
        s_game_rect.centery = main_surface_rect.centery
        main_surface.fill(GREEN)
        pygame.draw.rect(main_surface, BLUE, (5, 5,
                         main_surface_rect.right-10, main_surface_rect.bottom-10), 2)
        main_surface.blit(s_game, s_game_rect)
        main_surface.blit(font.render(
            ' ENTER YOUR NAME: ', True, RED), (220, 200))
        events = pygame.event.get()
        # Feed it with events every frame
        textinput.update(events)
        # Blit its surface onto the screen
        main_surface.blit(textinput.surface, (400, 200))

        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN:
                return textinput.value[:6]
            if event.type == QUIT:
                # db.close()
                sys.exit()
        pygame.display.update()


def game_over():
    sql_insert_one(db, name, scores)
    score_table = sql_fetch(db)
    step = 400
    fl = True
    while True:
        FPS.tick(60)
        # main_surface = pygame.display.set_mode((800, 600))
        g_over = pygame.image.load('images/GAME OVER.png').convert_alpha()
        g_over_rect = g_over.get_rect()  # pygame.Rect(150, 250, *g_over.get_size())
        main_surface_rect = main_surface.get_rect()
        g_over_rect.centerx = main_surface_rect.centerx
        g_over_rect.centery = main_surface_rect.centery
        # main_surface.fill(GREEN)
        pygame.draw.rect(main_surface, BLUE, (1, 1,
                         main_surface_rect.right-2, main_surface_rect.bottom-2), 5)
        main_surface.blit(font.render('PLAYER : SCORE',
                          True, RED), (350, 380))
        if fl == True:
            main_surface.blit(font_big.render(
                'HALL    OF    FAME', True, BLACK), (320, 360))
            for n, m in score_table:
                main_surface.blit(font.render(
                    n.upper(), True, RED), (350, step))
                main_surface.blit(font.render(
                    ': ' + str(m), True, RED), (430, step))
                step += 20
        fl = False
        main_surface.blit(g_over, g_over_rect)
        for event in pygame.event.get():
            if event.type == QUIT:
                db.close()
                sys.exit()

        pygame.display.update()


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
name = start_game()
is_working = True
while is_working:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(ball_imgs):
                img_index = 0
            ball = ball_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    bgx -= bg_speed
    bgx2 -= bg_speed

    if bgx < - bg.get_width():
        bgx = bg.get_width()
    if bgx2 < - bg.get_width():
        bgx2 = bg.get_width()

    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))

    main_surface.blit(ball, ball_rect)
    main_surface.blit(font.render('RLAYER: ' + name.upper() +
                      '  SCORES:' + str(scores), True, RED), (wigth - 250, 5))

    for enemy in enemies:
        main_surface.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(-enemy[2], 0)
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        if ball_rect.colliderect(enemy[1]):
            game_over()

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

    pygame.display.update()

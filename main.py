import pygame
from pygame.constants import QUIT
from random import randint

pygame.init()
screen = wigth, heigth = 801, 600
main_surface = pygame.display.set_mode(screen)
pygame.display.set_caption("SUPER BALL")
# ball = pygame.Surface((20, 20))
ball = pygame.image.load('images/ball.png')
ball_color = [(0, 0, 0), (255, 255, 255), (0, 0, 255),
              (0, 255, 0), (255, 25, 25), (255, 255, 51)]
# ball.fill((255, 255, 255))
ball_rect = ball.get_rect()
ball_speed = [1, 1]
is_working = True
while is_working:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
    ball_rect = ball_rect.move(ball_speed)
    if ball_rect.bottom >= heigth or ball_rect.top <= 0:  # отскок от края поля
        ball_speed[1] = - ball_speed[1]
        # ball.fill(ball_color[randint(0, 5)])  # изменение цвета объекта
    elif ball_rect.right >= wigth or ball_rect.left <= 0:
        ball_speed[0] = - ball_speed[0]
        # ball.fill(ball_color[randint(0, 5)])
    main_surface.fill((100, 100, 100))
    main_surface.blit(ball, ball_rect)
    pygame.display.flip()

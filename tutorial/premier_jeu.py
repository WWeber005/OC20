import pygame
from pygame.locals import *

size = 640, 320
width, height = size
GREEN = (150, 255, 150)
RED = (255, 0, 0)




pygame.init()
screen = pygame.display.set_mode(size)
running = True
speed = [1, 1]
ball = pygame.image.load('ball.gif')
rect = ball.get_rect()


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
           
    rect = rect.move(speed)
    if rect.left < 0 or rect.right > width:
        speed[0] = -speed[0]
    elif rect.top < 0 or rect.bottom > height:
        speed[1] = -speed[1]
        
    screen.fill(GREEN)
    pygame.draw.rect(screen, GREEN, rect, 1)
    screen.blit(ball, rect)
    pygame.display.update()

pygame.quit()
import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

#rect(screen, (255, 0, 255), (100, 100, 200, 200))
#rect(screen, (0, 0, 255), (100, 100, 200, 200), 5)
#polygon(screen, (255, 255, 0), [(100,100), (200,50),
#                               (300,100), (100,100)])
#polygon(screen, (0, 0, 255), [(100,100), (200,50),
#                               (300,100), (100,100)], 5)

#circle(screen, (0, 255, 0), (200, 175), 50)
color = (190, 190, 190)
screen.fill(color)


circle(screen, (255, 255, 0), (200, 175), 150) 	#голова

circle(screen, (255, 0, 0), (140, 135), 30)		#левый глаз
circle(screen, (255, 0, 0), (260, 135), 30)		#правый глаз

circle(screen, (0, 0, 0), (140, 135), 10)		#левый зрачок
circle(screen, (0, 0, 0), (260, 135), 10)		#правый зрачок


polygon(screen, (0, 0, 0), [(120, 70), (130, 60),
                 (177, 130), (156, 140), (120, 70)])

polygon(screen, (0, 0, 0), [(260, 70), (250, 60),
                 (207, 130), (226, 140), (260, 70)])

rect(screen, (0, 0, 0), (130, 200, 100, 10))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()
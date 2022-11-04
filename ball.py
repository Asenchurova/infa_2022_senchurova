mport pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 25
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():

    # _____РИСУЕТ НОВЫЙ ШАРИК_____
    '''
    здесь x, y, r - координаты и радиус, 
    velocity_0, 1 - скорости по горизонтали и вертикали
    '''

    finished = False
    global x, y, r, velocity_0, velocity_1
    
    x = randint(100, 1100)
    y = randint(100, 900)
    r = randint(10, 100)

    velocity_0 = randint(0, 5)
    velocity_1 = randint(0, 5)

    while not finished:

        x = randint(100, 1100)
        y = randint(100, 900)
        r = randint(10, 100)
        
    color = COLORS[randint(0, 5)]
       
    circle(screen, color, (x, y), r)

    return [x, y, r, color, velocity_0, velocity_1]


def click(event):
    print(x, y, r)

    global points
    if (event.y - y)**2 + (event.x - x)**2 <= r**2:
        points += 1



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
    new_ball()
    pygame.display.update()
    screen.fill(BLACK)



pygame.quit()
import pygame               #очевидно, зачем
from pygame.draw import *   #для рисования фигурок
from random import randint  #для задания случайных хар-к шаров
import pandas as pd         #для таблицы результатов

print('enter your name')
person = str(input())   #это понадобится для таблицы результатов
result = 0              #баллы текущего игрока пока 0

pygame.init()

FPS = 25
s_x = 1200  # размер экрана по горизонтали
s_y = 900   # размер экрана по вертикали
screen = pygame.display.set_mode((s_x, s_y))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

def new_ball():

    # ___РИСУЕТ НОВЫЙ ШАРИК___
    '''
    здесь x, y, r - координаты и радиус, 
    velocity_x, y - скорости по горизонтали и вертикали

    Возвращает характеристику шарика (тип - массив)
    '''

    global x, y, r, velocity_x, velocity_y, color


    x           = randint(10, s_x - 50)
    y           = randint(100, s_y - 20)
    r           = randint(10, 100)
    velocity_x  = randint(-5, 5)
    velocity_y  = randint(-5, 5)
    color       = COLORS[randint(0, 5)]  

    circle(screen, color, (x, y), r)

    return [x, y, r, color, velocity_x, velocity_y]

def several_balls(number):
    # ___РИСУЕТ НЕСКОЛЬКО ШАРИКОВ___
    '''
    Функция от числа шариков number. 
    Возвращает характеристики всех созданных шаров several_char
    (тип - массив)

    '''
    several_char = []

    for i in range(number):
        new_ball()
        several_char.append((new_ball()))

    return (several_char)

def is_click(several_balls, mouse_x, mouse_y):
    #___ПРОВЕРЯЕТ, ПОПАЛ ЛИ ЩЕЛЧОК ПО ШАРУ___
    '''
    Получает на вход массив характеристик шариков several_balls,
    координаты клика мыши
    Возвращает число попаданий

    Здесь, как и везде ранее, в массиве ball:
    [0] - x, [1] - y, [2] - r, [3] - colour,
    [4] - velocity_x, [5] - velocity_y
    Изначально планировалось перебирать массив иначе, но почему-то не получилось, поэтому такие некрасивые переменные

    '''
    points = 0
    for i in several_balls:
        
        if (mouse_x - i[0])**2 + (mouse_y - i[1])**2 <= i[2]**2:
            points += 1

    return (points)

def change_position(several_balls):
    #___МЕНЯЕТ КООРДИНАТЫ ШАРИКОВ___
    '''
    функция от массива координат набора шариков
    Возвращает массив новых характеристик шариков
    Учитывает отражение от стенок (меняет скорости на противоположные)
    Здесь, как и везде ранее, в массиве ball:
    [0] - x, [1] - y, [2] - r, [3] - colour,
    [4] - velocity_x, [5] - velocity_y

    '''
    several_balls_bytime = []
    x_bytime = 0
    y_bytime = 0

    for ball in several_balls:

        circle(screen, ball[3], (ball[0], ball[1]), ball[2])

        if (ball[0] + ball[2] > s_x) or (ball[0] - ball[2] <= 0):
            ball[4] *= (-1)

        if (ball[1] + ball[2] > s_y) or (ball[1] - ball[2] <= 0):
            ball[5] *= (-1)

        x_bytime = ball[0] + ball[4]
        y_bytime = ball[1] + ball[5]

        circle(screen, ball[5], (x_bytime, y_bytime), ball[2])
        j = [x_bytime, y_bytime, ball[2], ball[3], ball[4], ball[5]]
        several_balls_bytime.append(j)

    return(several_balls_bytime)

def personal_score(name, result):
    #___ЗАПИСЫВАЕТ РЕЗУЛЬТАТ ОДНОГО ИГРОКА___
    '''
   # Принимает имя person и его очки result
   # Если игрока ещё нет, записывает в табличку.
'''
    df = pd.read_csv('results.csv')

    print(list(df))

    if ((name in list(df['users'])) != 1):
        df.loc[len(df.index)] = [name, int(result)]
    else:
        df.at[list(df['users']).index(name), 'result'] = int(result)

    export_csv = df.to_csv(r'results.csv', index = None, header = True)

#функции кончились, функций дальше нет

pygame.display.update()
clock = pygame.time.Clock()
finished = False

TIME = 120  # влияет на то, как часто меняется набор шариков
timer = 0   #таймер
balls = several_balls(5)

while not finished:

    if timer == TIME:
        balls = several_balls(5)
        timer = 0

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if is_click(balls, mouse_x, mouse_y):
                result += 1

            print('Click!')

    balls = change_position(balls)

    pygame.display.update()
    screen.fill(BLACK)

    timer += 1

personal_score(person, result)
print('Your result is', result, '!')
pygame.quit()
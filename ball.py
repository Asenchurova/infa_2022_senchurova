import pygame               #очевидно, зачем
from pygame.draw import *   #для рисования фигурок
from random import randint  #для задания случайных хар-к шаров
import pandas as pd         #для таблицы результатов

person = str(input())   #это понадобится для таблицы результатов
result = 0              #баллы текущего игрока пока 0

pygame.init()


FPS = 25
s_x = 1200  # размер экрана по горизонтали, очень не хотелось называть переменную длиннее
s_y = 900   # размер экрана по вертикали, аналогично
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

    ball_char = [x, y, r, color, velocity_x, velocity_y]
    return (ball_char)

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
    Получает на вход массив характеристик шариков several_char,
    координаты клика мыши
    Возвращает число попаданий

    Здесь, как и везде ранее, в массиве ball:
    [0] - x, [1] - y, [2] - r, 
    [3] - velocity_x, [4] - velocity_y, [5] - colour
    '''
    points = 0
    for ball in several_balls:

        if (mouse_x - ball[0])**2 + (mouse_y - ball[1])**2 <= (ball[2])**2:
            points += 1

    return (points)

def change_position(several_char):
    #___МЕНЯЕТ КООРДИНАТЫ ШАРИКОВ___
    '''
    функция от массива координат набора шариков
    Возвращает массив новых характеристик шариков
    Учитывает отражение от стенок (меняет скорости на противоположные)
    Здесь, как и везде ранее, в массиве ball:
    [0] - x, [1] - y, [2] - r, 
    [3] - velocity_x, [4] - velocity_y, [5] - colour

    '''
    several_char_bytime = []

    for ball in several_balls:

        circle(screen, BLACK, (ball[0], ball[1]), ball[2])
        if ((ball[0] + ball[2] > s_x) or (ball[0] - ball[2] <= 0)):
            ball[3] *= (-1)

        if ((ball[1] + ball[2] > s_y) or (ball[1] - ball[2] <= 0)):
            ball[4] *= (-1)

        x_bytime = ball[0] + ball[3]
        y_bytime = ball[1] + ball[4]

        circle(screen, ball[5], (x_bytime, y_bytime), ball[2])
        several_balls_bytime.append(x_bytime, y_bytime, ball[2], ball[3], ball[4], ball[5])

    return(several_balls_bytime)

def personal_score(person, result):
    #___ЗАПИСЫВАЕТ РЕЗУЛЬТАТ ОДНОГО ИГРОКА___
    '''
    Принимает имя person и его очки result
    Если игрока ещё нет, записывает в табличку.
    '''
    df = pd.read_csv('results.csv')

    print(list(df))

    if not (person in list(df.users)):
        df.loc[len(df.index)] = [person, str(result)]
    else:
        df.at[list(df.users).index(person), 'result'] = result

    export_csv = df.to_csv(r'results.csv')

#функции кончились, функций дальше нет

pygame.display.update()
clock = pygame.time.Clock()
finished = False

ball_counter = 0
TIME = 60
timer = 0

balls = several_balls(5)

while not finished:
    if ball_counter == 21:
        finished = True 

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
                result += int(is_click)

            print('Click!')

    balls = change_position(balls)

    pygame.display.update()
    screen.fill(BLACK)

    timer += 1

personal_score(person, result)

pygame.quit()
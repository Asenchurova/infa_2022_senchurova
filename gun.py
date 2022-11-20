import math
import random as rnd

import pygame

FPS = 45

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
GRAVITY = 5


class GameObject:

    def __init__(self, screen: pygame.Surface, x, y, r, color=rnd.choice(GAME_COLORS)):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = r
        self.color = color

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def is_hit(self, obj):
        if self.distance(obj) <= (self.r + obj.r):
            return True
        return False

    def distance(self, obj):
        return math.sqrt((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2)


class Ball(GameObject):
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        super().__init__(screen, x, y, r=10, color=rnd.choice(GAME_COLORS))
        """ 
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.vx = 0
        self.vy = 0
        self.live = 30
        self.time = 0

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x + self.r >= WIDTH:
            self.vx = -self.vx
        if self.y + self.r >= HEIGHT:
            self.vy = -self.vy / 1.25
            if math.fabs(self.vy) < 5:
                self.vy = 0
                self.vx = 0
        if self.y > HEIGHT:
            self.y = HEIGHT
        if self.x > WIDTH:
            self.x = WIDTH
        if self.vy != 0:
            self.vy -= GRAVITY * self.time
        self.x += self.vx
        self.y -= self.vy
        self.time += 1 / 30

    def draw(self):
        if self.vy != 0:
            super().draw()
        else:
            if self.time < self.live:
                super().draw()
            self.time += 3


class Rocket(GameObject):
    def __init__(self, screen: pygame.Surface, x=0, y=0):
        super().__init__(screen, x, y, r=5, color=GREEN)
        self.vx = 0
        self.vy = 0
        self.live = 1
        self.time = 0

    def draw(self):
        if self.live >= 1:
            super().draw()

    def move(self):
        if (self.x + self.r) >= WIDTH or (self.y + self.r) >= HEIGHT:
            self.live = 0
        self.vy -= GRAVITY * self.time
        self.x += self.vx
        self.y -= self.vy
        self.time += 1 / 30


class Gun(GameObject):
    def __init__(self, screen: pygame.Surface):
        self.f2_power = 10
        self.f2_on = 0
        self.angle = 1
        self.bullet = 0
        self.f2_max_power = 100
        super().__init__(screen, x=0, y=0, r=0, color=GREY)

    def fire2_start(self):
        if event.button == 1:
            self.f2_on = 1
        if event.button == 3:
            self.bullet += 5
            new_rocket = Rocket(self.screen)
            self.angle = math.atan2((event.pos[1] - new_rocket.y), (event.pos[0] - new_rocket.x))
            new_rocket.vx = 50 * math.cos(self.angle)
            new_rocket.vy = -50 * math.sin(self.angle)
            rockets.append(new_rocket)
            self.f2_on = 0

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        if event.button == 1:
            self.bullet += 1
            new_ball = Ball(self.screen)
            new_ball.r += 5
            self.angle = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
            new_ball.vx = self.f2_power * math.cos(self.angle)
            new_ball.vy = - self.f2_power * math.sin(self.angle)
            balls.append(new_ball)
            self.f2_on = 0
            self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan2(event.pos[1] - 450, event.pos[0] - 20)
        if self.f2_on:
            self.color = YELLOW
        else:
            self.color = GREY

    def draw(self):
        if self.f2_on == 0:
            pygame.draw.line(self.screen, self.color, (20, 450),
                             (20 + 35 * math.cos(self.angle), 450 + 35 * math.sin(self.angle)), 7)
        else:
            pygame.draw.line(self.screen, self.color, (20, 450), (
                20 + (35 + self.f2_power) * math.cos(self.angle), 450 + (35 + self.f2_power) * math.sin(self.angle)), 7)

    def power_up(self):
        if self.f2_on:
            if self.f2_power < self.f2_max_power:
                self.f2_power += 1
            self.color = YELLOW
        else:
            self.color = GREY


class Target(GameObject):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen, x=rnd.randint(600, 780), y=rnd.randint(250, 450), r=rnd.randint(20, 50), color=RED)
        self.v = rnd.randint(-15, 15)
        self.points = 0
        self.live = 1

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
        ''' Двигает цели по вертикали со случайной скоростью '''
        if self.v == 0:
            while self.v == 0:
                self.v = rnd.randint(-15, 15)
        if (self.y + self.r) >= HEIGHT or (self.y - self.r) <= 0:
            self.v = -self.v
        self.y += self.v


def init_game():
    pygame.init()
    return pygame.display.set_mode((WIDTH, HEIGHT))


balls = []
rockets = []
targets = []
screen = init_game()
gun = Gun(screen)
finished = False
while not finished:
    screen.fill(BLACK)
    if len(targets) < 2:
        targets.append(Target(screen))
    for t in targets + balls + rockets:
        t.draw()
    gun.draw()
    for t in targets:
        t.move()
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                finished = True
            case pygame.MOUSEBUTTONDOWN:
                gun.fire2_start()
            case pygame.MOUSEBUTTONUP:
                gun.fire2_end(event)
            case pygame.MOUSEMOTION:
                gun.targetting(event)
    for c in balls + rockets:
        c.move()
        for i in range(2):
            if c.is_hit(targets[i]):
                targets[i].hit()
                targets.remove(targets[i])
                targets.append(Target(screen))
    gun.power_up()
    pygame.display.update()
pygame.quit()
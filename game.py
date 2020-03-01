import pygame, sys, time, math, random
from pygame.locals import *
pygame.init()
width = 500
height = 500
frame = pygame.display.set_mode((width, height))
pygame.display.set_caption('Breakout!')
fpsClock = pygame.time.Clock()
fps = 60
last = time.time()
bg = (0, 0, 0)

class Ball:
    def __init__(self):
        self.x = 340
        self.y = 300
        self.vx = 0
        self.vy = 0
        self.r = 10
        self.color = (0, 255, 255)

    def update(self, elapsed):
        if self.x < self.r:
            self.vx = abs(self.vx)
        elif self.x > width - self.r:
            self.vx = -abs(self.vx)
        if self.y < self.r:
            self.vy = abs(self.vy)
        
        self.x += self.vx * elapsed
        self.y += self.vy * elapsed

    def draw(self, frame):
        pygame.draw.circle(frame,self.color, (int(self.x), int(self.y)), self.r, 0)

class Paddle:
    def __init__(self):
        self.width = 90
        self.height = 8
        self.color = (255, 255, 255)
        self.x = width/2 - self.width/2
        self.y = height - 10
        self.vx = 0
        self.speed = 650
        self.buff = 5

    def draw(self, frame):
        pygame.draw.rect(frame, self.color, (self.x, self.y, self.width, self.height))

    def update(self, elapsed):
        l = pygame.key.get_pressed()[pygame.K_LEFT]
        r = pygame.key.get_pressed()[pygame.K_RIGHT]

        if l != r:
            if l:
                self.vx = -self.speed
            if r:
                self.vx = self.speed
        else:
            self.vx = 0
        
        self.x += self.vx * elapsed

        if self.x < self.buff:
            self.x = self.buff
        elif self.x + self.width > width - self.buff:
            self.x = width - self.width - self.buff

class Brick():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, frame):
        pygame.draw.rect(frame, self.color, (self.x, self.y, self.width, self.height))

    def update(self, elapsed):
        pass

def coll(ball, obj):
    # top segment
    px = ball.x
    py = obj.y
    if px < obj.x: # if ball is left of box, closest point is edge
        px = obj.x
    elif px > obj.x + obj.width:
        px = obj.x + obj.width

    if math.sqrt((ball.x - px)**2 + (ball.y - py)**2) <= ball.r:
        dy = ball.y - py
        dx = ball.x - px
        if dx != 0:
            theta = math.atan(dy/dx)
            vel = math.sqrt(ball.vx**2 + ball.vy**2)
            if dx > 0:
                ball.vx = abs(math.cos(theta) * vel)
            else:
                ball.vx = -abs(math.cos(theta) * vel)
            ball.vy = -abs(math.sin(theta) * vel)
        if dx == 0:
            ball.vy = -abs(ball.vy)
        return True

    # bottom segment
    px = ball.x
    py = obj.y + obj.height
    if px < obj.x: # if ball is left of box, closest point is edge
        px = obj.x
    elif px > obj.x + obj.width:
        px = obj.x + obj.width

    if math.sqrt((ball.x - px)**2 + (ball.y - py)**2) <= ball.r:
        dy = ball.y - py
        dx = ball.x - px
        if dx != 0:
            theta = math.atan(dy/dx)
            vel = math.sqrt(ball.vx**2 + ball.vy**2)
            if dx > 0:
                ball.vx = abs(math.cos(theta) * vel)
            else:
                ball.vx = -abs(math.cos(theta) * vel)
            ball.vy = abs(math.sin(theta) * vel)
        if dx == 0:
            ball.vy = abs(ball.vy)
        return True

    # left segment
    px = obj.x
    py = ball.y
    if py < obj.y: # if ball is left of box, closest point is edge
        py = obj.y
    elif py > obj.y + obj.height:
        py = obj.y + obj.height

    if math.sqrt((ball.x - px)**2 + (ball.y - py)**2) <= ball.r:
        dy = ball.y - py
        dx = ball.x - px
        if dy != 0:
            theta = math.atan(dy/dx)
            vel = math.sqrt(ball.vx**2 + ball.vy**2)
            if dy > 0:
                ball.vy = abs(math.sin(theta) * vel)
            else:
                ball.vy = -abs(math.sin(theta) * vel)
            ball.vx = -abs(math.cos(theta) * vel)
        if dy == 0:
            ball.vx = -abs(ball.vx)
        return True

    # right segment
    px = obj.x + obj.width
    py = ball.y
    if py < obj.y: # if ball is left of box, closest point is edge
        py = obj.y
    elif py > obj.y + obj.height:
        py = obj.y + obj.height

    if math.sqrt((ball.x - px)**2 + (ball.y - py)**2) <= ball.r:
        dy = ball.y - py
        dx = ball.x - px
        if dy != 0:
            theta = math.atan(dy/dx)
            vel = math.sqrt(ball.vx**2 + ball.vy**2)
            if dy > 0:
                ball.vy = abs(math.sin(theta) * vel)
            else:
                ball.vy = -abs(math.sin(theta) * vel)
            ball.vx = abs(math.cos(theta)*vel)
        if dy == 0:
            ball.vx = abs(ball.vx)
        return True

def update(elapsed):
    ball.update(elapsed)
    paddle.update(elapsed)
    coll(ball,paddle)
    i = 0
    while i < len(bricks):
        if coll(ball, bricks[i]):
            del bricks[i]
        else:
            i += 1
    if ball.y >= height:
        global lose
        lose = True
    if len(bricks) == 0:
        global win
        win = True

def draw(frame):
    ball.draw(frame)
    paddle.draw(frame)
    for brick in bricks:
        brick.draw(frame)
    if lose:
        draw_text("YOU LOSE!")
        ball.vx = 0
        ball.vy = 0
    if win:
        draw_text(" YOU WIN!")
        ball.vx = 0
        ball.vy = 0

def draw_text(text): # writes words to screen
    myfont = pygame.font.SysFont("monospace", 100)
    labelWhite = myfont.render(text, 1000, (255, 255, 255))
    labelRed = myfont.render(text, 1000, (255, 0, 0))
    frame.blit(labelWhite, (60, 200))
    frame.blit(labelRed, (62, 202))

ball = Ball()
paddle = Paddle()
colors = [(0, 255, 0), (0, 255, 255), (255, 255, 0), (255, 128, 0), (255, 0, 191)]
bricks = [Brick(2 + 50 * (i % 10), 40 + 25 * (i // 10), 40, 20, colors[i // 10]) for i in range(50)]
lose = False
win = False
ball.x = width/2
ball.y = height - 30
random_angles = [20, 40, 80, 90, 145, 170, 180, 300, 310, 360]
theta = random.choice(random_angles)
vel = 400
ball.vx = math.cos(theta) * vel
ball.vy = math.sin(theta) * vel

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    curr = time.time()
    update(curr - last)
    frame.fill(bg)
    draw(frame)
    pygame.display.update()
    fpsClock.tick(fps)
    last = curr
    vel += 20
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

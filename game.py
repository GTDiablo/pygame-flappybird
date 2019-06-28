# -*- coding:utf-8 -*-
import pygame
import math
import random

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.size = 15
        self.lift = 12
        self.alive = True

    def draw(self):
        pygame.draw.circle(WINDOW, COLORS['bird'], (self.x, self.y), self.size)

    def update(self):
        self.vel += GRAVITY
        self.y += int(self.vel)

        if self.y > HEIGHT or self.y < 0:
            self.alive = False

    def up(self):
        self.vel -= self.lift


class Pipe:
    def __init__(self):
        self.y = 0
        self.x = WIDTH
        self.w = 60
        self.speed = 4
        self.gap = 150
        self.top = random.randint(10, HEIGHT//2)
        self.bottom = self.top + self.gap

    def draw(self):
        pygame.draw.rect(WINDOW, COLORS['pipe'], (self.x, self.y, self.w, self.top))
        pygame.draw.rect(WINDOW, COLORS['pipe'], (self.x, self.bottom, self.w, HEIGHT - self.bottom))
        
    def update(self):
        self.x -= self.speed

    def offscreen(self):
        return self.x + self.w < 0

    def hits(self, bird):
        if bird.y - bird.size < self.top or bird.y + bird.size > self.bottom:
            if bird.x + bird.size >= self.x and bird.x - bird.size <= self.x + self.w:
                return True
        
# Ablak ifnformáció és beállítások
TITLE = 'Flappybird'
WIDTH = 9 * 50
HEIGHT = 14 * 50
SIZE = (WIDTH, HEIGHT)
WINDOW = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)

# Játékbeli konstatnsok és változók
COLORS = dict(
    white = (255,255,255),
    black = (0,0,0),
    sky = (140,184,255),
    pipe = (70, 160, 54),
    bird = (252, 218, 83)
    )
GRAVITY = .5
CLOCK = pygame.time.Clock()
BIRD = Bird(50, HEIGHT//2)
PIPES = []
FRAMERATE = 0
SCORE = 0
RUNNING = True

while RUNNING:
    
    while BIRD.alive:

        WINDOW.fill(COLORS['sky'])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                BIRD.alive = False
                RUNNING = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                BIRD.alive = False
                RUNNING = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                BIRD.up()
                
        BIRD.draw()
        BIRD.update()

        if FRAMERATE % 90 == 0:
            PIPES.append(Pipe())
            FRAMERATE = 0

        for i in range(len(PIPES)-1, 0, -1):
            PIPES[i].draw()
            PIPES[i].update()

            if PIPES[i].hits(BIRD):
                BIRD.alive = False                  
            
            if PIPES[i].offscreen():
                PIPES.pop(i)
                SCORE += 1

        pygame.display.update()
        CLOCK.tick(60)
        FRAMERATE += 1

    print("Game Over")
    print("Your score: %d" % SCORE)
    BIRD = Bird(50, HEIGHT//2)
    PIPES = []
    SCORE = 0
    
pygame.quit()

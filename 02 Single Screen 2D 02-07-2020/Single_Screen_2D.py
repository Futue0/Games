# Robin Vize 02-07-2020.
# 2D platformer with everything on a single screen.
# The most basic 2D platformer possible and first game with PyGame.
# Adapted from here: https://www.youtube.com/watch?v=Q-__8Xw9KTM.
# Note we are using a lot of OOP now.

import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game 02")

# Load all images.
PLAYER_IMAGE = pygame.image.load(os.path.join("assets", "player.png"))
PLATFORM_IMAGE = pygame.image.load(os.path.join("assets", "platform.png"))
FINISH_IMAGE = pygame.image.load(os.path.join("assets", "finish.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))

class Platform:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)


class Player:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_image = PLAYER_IMAGE

        self.mask = pygame.mask.from_surface(self.player_image)

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    
    player = Player(300, 630)

    def redraw_window():
        WIN.blit(BG, (0,0))

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        # check if player and finish are colliding and set win condition

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel

# Run main game loop.
while True:
    main()

pygame.quit()


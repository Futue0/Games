# Robin Vize 02-07-2020.
# 2D platformer with everything on a single screen.
# The most basic 2D platformer possible and first game with PyGame.
# Main menu, win condition, single screen.
# No collision detection, no platforming, jumping is poor.
# Adapted from here: https://www.youtube.com/watch?v=Q-__8Xw9KTM.
# Note: we are using more OOP now.

import pygame
import os

# Setup.
pygame.font.init()
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Single Screen Platformer")

# Load all images.
PLAYER_IMAGE = pygame.image.load(os.path.join("assets", "player.png"))
PLATFORM_IMAGE = pygame.image.load(os.path.join("assets", "platform.png"))
FINISH_IMAGE = pygame.image.load(os.path.join("assets", "finish.png"))
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))

# Player object.
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_image = PLAYER_IMAGE
        self.mask = pygame.mask.from_surface(self.player_image)

    def draw(self, window):
        window.blit(self.player_image, (self.x, self.y))

    def get_width(self):
        return self.player_image.get_width()

    def get_height(self):
        return self.player_image.get_height()


# Finish object.
class Finish:
    def __init__(self):
        self.x = WIDTH - 100
        self.y = HEIGHT - 180
        self.finish_image = FINISH_IMAGE
        self.mask = pygame.mask.from_surface(self.finish_image)

    def draw(self, window):
        window.blit(self.finish_image, (self.x, self.y))


# Main game loop.
def main():
    # initialise
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    aim_font = pygame.font.SysFont("comicsans", 30)
    win_font = pygame.font.SysFont("comicsans", 60)

    # finish
    finish = Finish()
    win = False
    
    # player controls
    player_floor = HEIGHT - 100
    player = Player(0, player_floor)
    player_move_speed = 5
    player_jump_height = 60
    player_jump_cooldown = FPS
    time_since_jump = player_jump_cooldown
    player_fall_speed = 2  
    
    # continual redraw from within loop below
    def redraw_window():
        WIN.blit(BG, (0, 0))

        aim_label = aim_font.render("<-a d-> SPACE jump", 1, (0, 0, 0))
        aim_label2 = aim_font.render("touch the heart to win", 1, (0, 0, 0))
        WIN.blit(aim_label, (500, 30))
        WIN.blit(aim_label2, (500, 50))
        
        player.draw(WIN)
        finish.draw(WIN)
        
        if win:
            win_label = win_font.render("woohoo. touch de organ", 1, (0, 0, 0))
            WIN.blit(win_label, (120, 350))

        pygame.display.update()

    # looping run
    while run:
        clock.tick(FPS)
        redraw_window()

        # quit the game/window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # player left-right movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_move_speed > 0:
            player.x -= player_move_speed
        if keys[pygame.K_d] and player.x + player_move_speed + player.get_width() < WIDTH:
            player.x += player_move_speed

        # player jumping
        time_since_jump += FPS / 30           
        if keys[pygame.K_SPACE]:
            if time_since_jump > player_jump_cooldown:
                player.y -= player_jump_height
                time_since_jump = 0
        if player.y < player_floor:
            player.y += player_fall_speed

        # check for win condition
        if player.x >= finish.x - 10 and player.y <= finish.y + 50:
            print("win")
            win = True
        
            
# Run main game loop.
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (50, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()


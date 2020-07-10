# Robin Vize 03-07-2020.
# 2D platformer with everything on a single screen.
# The most basic 2D platformer possible and first game with pyglet.
# Platforms with collision, win condition, single screen.


import pyglet
from pyglet.window import key
import load


# GLOBALS.
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800


# IMAGES.
load.load_path('../assets')

background_image = pyglet.resource.image('background.png')
platform_image = pyglet.resource.image('platform.png')
finish_image = pyglet.resource.image('finish.png')
player_image = pyglet.resource.image('player.png')

# Sprites.
batch = pyglet.graphics.Batch()
player = pyglet.sprite.Sprite(player_image, batch=batch)
finish = pyglet.sprite.Sprite(finish_image, x=700, y=700, batch=batch)

platform1 = pyglet.sprite.Sprite(platform_image, x=150, y=30, batch=batch)
platform2 = pyglet.sprite.Sprite(platform_image, x=200, y=200, batch=batch)
platform3 = pyglet.sprite.Sprite(platform_image, x=400, y=400, batch=batch)


# PLAYER.
player_vel = WINDOW_WIDTH // 2
player_jump = 4000
player_fall = 20


# WINDOW.
window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption='Single Screen Platformer')
window.set_icon(pyglet.resource.image('16x16.png'), pyglet.resource.image('32x32.png'))
keyboard = key.KeyStateHandler()
window.push_handlers(keyboard)
window.push_handlers(player)

@window.event
def on_key_press(symbol, modifiers):
    # key presses here are only single activation so not good for player controls
    pass

@window.event
def on_draw():
    window.clear()
    background_image.blit(0, 0, width=window.width, height=window.height)
    batch.draw()


# TEXT.
quest_label = pyglet.text.Label(
    'Reach the heart to win',
    font_name='Times New Roman',
    font_size=24,
    bold=True,
    batch=batch,
    color=(0, 0, 0, 255),
    x=window.width//2, y=window.height-50,
    anchor_x='center', anchor_y='center'
)


# COLLISIONS.
# because the platforms are long and thin and the player is a square
# the collisions check if vertices are inside a bounding box but do so
# with the opposite objects in the cases of left-right and top-bottom
def is_collide(player, platform):
    # top-bottom (1, or both, bottom (or top) player corners inside platform area)
    # player vertices (bottom-left-x to top-right-y)
    blx, bly = player.x, player.y
    brx, bry = player.x + player.width, player.y
    tlx, tly = player.x, player.y + player.height
    trx, tryy = player.x + player.width, player.y + player.height # ofc 'try' unfortunately spells python reserved word...

    # platform bounding box (area)
    plat_min_x, plat_min_y = platform.x, platform.y
    plat_max_x, plat_max_y = platform.x + platform.width, platform.y + platform.height

    # one or both of player's bottom corners have collided with platform - i.e. player has landed on platform
    if (plat_min_x < blx < plat_max_x and plat_min_y < bly < plat_max_y) or (plat_min_x < brx < plat_max_x and plat_min_y < bry < plat_max_y):
        return "player_landed"
    # one or both of player's top corners have collided with platform - i.e. player is jumping up into platform from below
    elif (plat_min_x < tlx < plat_max_x and plat_min_y < tly < plat_max_y) or (plat_min_x < trx < plat_max_x and plat_min_y < tryy < plat_max_y):
        return "player_bonk"

    # left-right (1, or both, left side (or right rise) platform corners inside player area)
    # platform vertices (bottom-left-x to top-right-y)
    blx, bly = platform.x, platform.y
    brx, bry = platform.x + platform.width, platform.y
    tlx, tly = platform.x, platform.y + platform.height
    trx, tryy = platform.x + platform.width, platform.y + platform.height # ofc 'try' unfortunately spells python reserved word...

    # player bounding box (area)
    play_min_x, play_min_y = player.x, player.y
    play_max_x, play_max_y = player.x + player.width, player.y + player.height

    # one or both of platforms left side corners have collided with player - i.e. player moved right, into platform side
    if (play_min_x < blx < play_max_x and play_min_y < bly < play_max_y) or (play_min_x < tlx < play_max_x and play_min_y < tly < play_max_y):
        return "player_stop_right"
    # one or both of platform's right side corners have collided with player - i.e. player moved left, into platform side
    elif (play_min_x < brx < play_max_x and play_min_y < bry < play_max_y) or (play_min_x < trx < play_max_x and play_min_y < tryy < play_max_y):
        return "player_stop_left"

# UPDATER.
state = { # sort of state machine dict
    'idle': True,
    'moving_left': False,
    'moving_right': False,
    'idle_jumping': False,
    'jumping_left': False,
    'jumping_right': False
}

limited_movement = False
limiting_factor = 3

def polling_updater(dt):
    # keep player in bounds
    left_bound = True if player.x <= 0 else False
    right_bound = True if player.x + 50 >= WINDOW_WIDTH else False
    # top_bound not used because finish heart is top corner
    # and think it would be annoying if player hit ceiling
    ground_bound = True if player.y <= 0 else False
    
    # player controls
    if keyboard[key.D] and not right_bound and not state['jumping_left']:
        state['idle'] = False
        state['moving_left'] = False
        state['moving_right'] = True
        if limited_movement:
            player.x += (player_vel / limiting_factor) * dt
        else:
            player.x += player_vel * dt
    elif keyboard[key.A] and not left_bound and not state['jumping_right']:
        state['idle'] = False
        state['moving_left'] = True
        state['moving_right'] = False
        if limited_movement:
            player.x -= (player_vel / limiting_factor) * dt
        else:
            player.x -= player_vel * dt
    else:
        state['idle'] = True

    if keyboard[key.SPACE] and ground_bound:
        if state['idle']:
            state['idle_jumping'] = True
        elif state['moving_left']:
            state['jumping_left'] = True
        elif state['moving_right']:
            state['jumping_right'] = True
        ground_bound = False
        player.y += player_jump * dt

    # gravity
    if not ground_bound: # player falls
        player.y -= (player_jump / player_fall) * dt
    else: # player is now on ground
        state['idle_jumping'] = False
        state['jumping_left'] = False
        state['jumping_right'] = False

# This sets the background clock to run polling_updater at 120 FPS.
pyglet.clock.schedule_interval(polling_updater, 1 / 120)


# RUN!
pyglet.app.run()


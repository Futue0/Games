# Robin Vize 03-07-2020.
# 2D platformer with everything on a single screen.
# The most basic 2D platformer possible and first game with pyglet.
# Platforms with collision, win condition, single screen.


import pyglet
from pyglet.window import key
import load


# GLOBALS.
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
GAME_WON = False

# IMAGES.
load.load_path('../assets')

background_image = pyglet.resource.image('background.png')
platform_image = pyglet.resource.image('platform.png')
finish_image = pyglet.resource.image('finish.png')
player_image = pyglet.resource.image('player.png')

# Sprites.
batch = pyglet.graphics.Batch()
player = pyglet.sprite.Sprite(player_image, batch=batch)
finish = pyglet.sprite.Sprite(finish_image, x=50, y=700, batch=batch)

x_pos = 0
y_pos = 0
x_step = 110
y_step = 45
platforms = []

for i in range(7):
    x_pos += x_step
    y_pos += y_step
    platform = pyglet.sprite.Sprite(platform_image, x=x_pos, y=y_pos, batch=batch)
    platforms.append(platform)

for i in range(7):
    x_pos -= x_step
    y_pos += y_step
    platform = pyglet.sprite.Sprite(platform_image, x=x_pos, y=y_pos, batch=batch)
    platforms.append(platform)

# PLAYER.
player_vel = WINDOW_WIDTH // 2
player_jump = 6000
player_fall = 30 # higher = slower falling


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

    if GAME_WON:
        win_label.draw()


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

win_label = pyglet.text.Label(
    'YOU GOT HEART. YOU WIN!',
    font_name='Times New Roman',
    font_size=40,
    bold=True,
    color=(50, 50, 50, 255),
    x=window.width//2, y=window.height//2,
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

    # otherwise, no collisions at all
    return None

# UPDATER.
state = { # sort of state machine dict
    'idle': True,
    'moving_left': False,
    'moving_right': False,
    'idle_jumping': False,
    'jumping_left': False,
    'jumping_right': False
}

def polling_updater(dt):
    # using this to allow player to have directional movement whilst falling from an idle (standing) jump
    # but limiting the control so running jumps feel more powerful
    global limited_movement
    limiting_factor = 2

    # keep player in bounds
    left_bound = True if player.x <= 0 else False
    right_bound = True if player.x + 50 >= WINDOW_WIDTH else False
    # top_bound not used because finish heart is top corner
    # and think it would be annoying if player hit the ceiling
    ground_bound = True if player.y <= 0 else False
    
    # check player collisions with all platforms
    collision_check = None
    for platform in platforms:
        if is_collide(player, platform) != None:
            collision_check = is_collide(player, platform)

    # check player-finish condition (game won)
    if is_collide(player, finish) != None:
        GAME_WON = True
    ### NOTE: can't get this to equate to the winning text appearing on window when you actually reach the heart ###

    # player controls
    if keyboard[key.D] and not right_bound and not state['jumping_left']:
        state['idle'] = False
        state['moving_left'] = False
        state['moving_right'] = True
        if collision_check != "player_stop_right":
            if limited_movement:
                player.x += (player_vel / limiting_factor) * dt
            else:
                player.x += player_vel * dt
    elif keyboard[key.A] and not left_bound and not state['jumping_right']:
        state['idle'] = False
        state['moving_left'] = True
        state['moving_right'] = False
        if collision_check != "player_stop_left":
            if limited_movement:
                player.x -= (player_vel / limiting_factor) * dt
            else:
                player.x -= player_vel * dt
    else:
        state['idle'] = True

    if keyboard[key.SPACE] and (ground_bound or collision_check == "player_landed"):
        if state['idle']:
            limited_movement = True
            state['idle_jumping'] = True
        elif state['moving_left']:
            state['jumping_left'] = True
        elif state['moving_right']:
            state['jumping_right'] = True
        ground_bound = False
        player.y += player_jump * dt

    # gravity
    if not ground_bound and collision_check != "player_landed": # player falls
        player.y -= (player_jump / player_fall) * dt
    else: # player is now on ground
        limited_movement = False
        state['idle_jumping'] = False
        state['jumping_left'] = False
        state['jumping_right'] = False


# This sets the background clock to run polling_updater at 120 FPS.
pyglet.clock.schedule_interval(polling_updater, 1 / 120)


# RUN!
pyglet.app.run()


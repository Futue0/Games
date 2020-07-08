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

platform1 = pyglet.sprite.Sprite(platform_image, x=100, y=100, batch=batch)
platform2 = pyglet.sprite.Sprite(platform_image, x=200, y=200, batch=batch)
platform3 = pyglet.sprite.Sprite(platform_image, x=400, y=400, batch=batch)


# PLAYER.
player_vel = WINDOW_WIDTH // 2
player_jump = 4000


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
quest_label = pyglet.text.Label('Reach the heart to win',
                          font_name='Times New Roman',
                          font_size=24,
                          bold=True,
                          batch=batch,
                          color=(0, 0, 0, 255),
                          x=window.width//2, y=window.height-50,
                          anchor_x='center', anchor_y='center')


# COLLISIONS.
def is_collide(obj1, obj2):
    pass


# UPDATER.
state = {
    'idle': True,
    'moving_left': False,
    'moving_right': False,
    'jumping': False,
    'jumping_left': False,
    'jumping_right': False
}

def polling_updater(dt):
    # keep player in bounds
    left_bound = True if player.x <= 0 else False
    right_bound = True if player.x + 50 >= WINDOW_WIDTH else False
    top_bound = True if player.y + 50 >= WINDOW_HEIGHT else False
    ground_bound = True if player.y <= 0 else False
    
    # player controls
    if keyboard[key.D] and not right_bound:
        state['idle'] = False
        state['moving_left'] = False
        state['moving_right'] = True
        player.x += player_vel * dt
    if keyboard[key.A] and not left_bound:
        state['idle'] = False
        state['moving_left'] = True
        state['moving_right'] = False
        player.x -= player_vel * dt
    if keyboard[key.SPACE]:
        state['jumping'] = True
        if ground_bound:
            player.y += player_jump * dt

    # gravity
    if not ground_bound:
        player.y -= (player_jump / 20) * dt

# This sets the background clock to run polling_updater at 120 FPS.
pyglet.clock.schedule_interval(polling_updater, 1 / 120)


# RUN!
pyglet.app.run()


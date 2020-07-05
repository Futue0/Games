# Robin Vize 03-07-2020.
# 2D platformer with everything on a single screen.
# The most basic 2D platformer possible and first game with pyglet.
# Main menu, win condition, single screen.

### Structure from Astraea example:
###
###     imports
###     GLOBAL constants
###
###     global functions (used in objects below so called here)
###     game objects (classes)
###     UI objects (classes)
###
###     global functions (~mostly~ not used in objects)
###     window setup + decorators
###     resources setup
###     global game state variables
###     game update function
###     pyglet.clock -> pyglet.app.run()

import pyglet
from pyglet.window import key


# IMAGES.
# Set path to correct folder.
pyglet.resource.path = ['../assets']
pyglet.resource.reindex()

# Load image files.
icon1 = pyglet.resource.image('16x16.png')
icon2 = pyglet.resource.image('32x32.png')
background_image = pyglet.resource.image('background.png')
platform_image = pyglet.resource.image('platform.png')
finish_image = pyglet.resource.image('finish.png')
player_image = pyglet.resource.image('player.png')


# WINDOW.
# Game (and only) window.
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption='Single Screen Platformer')
window.set_icon(icon1, icon2)

quest_label = pyglet.text.Label('Reach the heart to win',
                          font_name='Times New Roman',
                          font_size=24,
                          bold=True,
                          color=(0, 0, 0, 255),
                          x=window.width//2, y=window.height-50,
                          anchor_x='center', anchor_y='center')

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        pass # move left
    elif symbol == key.D:
        pass # move right
    elif symbol == key.SPACE:
        pass # jump

@window.event
def on_draw():
    window.clear()
    background_image.blit(0, 0, width=window.width, height=window.height)
    quest_label.draw()

pyglet.app.run()

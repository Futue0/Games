import pyglet
from os import listdir

def load_path(path): # set image directory (path)
    pyglet.resource.path = [path]
    pyglet.resource.reindex()

def image_list(path): # image loader helper (path should be same as above)
    return [i for i in listdir(path)]
    

import os
import pygame
import time
from Album import Album
from Item import Item
SCREEN_RESOLUTION = (1000, 600)
pygame.init()

class Root:
    Albums = []
    Location = ""
    Name = ""
    Pointer = 0
    Current_Album = None
    Buffer = []
    ALGS = False

    def __init__(self, location, name):
        self.Name = name
        self.Albums.append([])
        self.Location = location + "\\" + name

    def get_path_name(self):
        return self.Location

    def init(self, directory, current_album, go_deeper):
        for item in os.listdir(directory):
            if os.path.isdir(directory + "/" + item) and go_deeper:
                new_album = Album(item, directory)
                self.Albums[0].append(new_album)
                self.init(directory + "/" + item, new_album, False)
            else:
                try:
                    image = pygame.image.load(directory + "/" + item)
                    current_album.add_item(Item(image, item, directory))
                except Exception:
                    continue

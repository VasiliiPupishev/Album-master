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
    List_Current = None
    Buffer = []
    ALGS = False

    def get_current_album(self, bool):
        if len(self.List_Current) > 0:
            res = self.List_Current[-1]
            if bool:
                self.List_Current.remove(res)
            return res
        else:
            return None

    def add_current_album(self, album):
        self.List_Current.append(album)

    def __init__(self, location, name):
        self.Name = name
        self.List_Current = []
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

    def add_album(self, album):
        self.Albums.append(album)

    def is_album(self, loc, name):
        return

    def update(self, directory):
        return
        #for item in os.listdir(directory):
            #for album1 in self.Albums:
                #for album in album1:
                    #for item in album.get_all_items():
                        #print(item.get_path_name())


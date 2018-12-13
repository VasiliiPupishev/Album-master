import os
import pygame
import time
from Album import Album
from Item import Item
SCREEN_RESOLUTION = (1000, 600)
pygame.init()

class Root:
    Albums = None
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
        self.Albums = []
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
        for list in self.Albums:
            if len(list) < 28:
                list.append(album)
                return
        self.Items.append([album])

    def is_album(self, loc, name):
        return

    def update(self, ddd):
        flag = False
        for fol in self.Albums:
            for album in fol:
                items = os.listdir(os.getcwd() + "/" + album.Location)
                ls = album.get_all_items()
                for item in ls:
                    if items.__contains__(item.Name):
                        items.remove(item.Name)
                    else:
                        self.get_current_album(False).del_item(item)
                        flag = True
                for name in items:
                    try:
                        image = pygame.image.load(album.Location + "/" + name)
                        self.get_current_album(False).add_item(Item(image, name, album.Name))
                        flag = True
                    except Exception:
                        continue
        return flag

import os

SCREEN_RESOLUTION = (1000, 600)
import pygame


class Item:
    X = 0
    Y = 0
    Location = ""
    Name = ""
    # Image = None
    Index = -1

    def get_image(self):
        try:
            return pygame.image.load(self.Location + "/" + self.Name).convert_alpha()
        except Exception:
            del self
            return None

    def del_item(self):
        del self

    def __init__(self, image, name, location):
        self.Name = name
        # self.Image = image
        self.Location = location

    def get_path_name(self):
        return self.Location + "\\" + self.Name

    def set_position(self, x, y):
        self.X = x
        self.Y = y

    def get_position(self):
        return self.X, self.Y

import os

SCREEN_RESOLUTION = (1000, 600)

class Item:
    X = 0
    Y = 0
    Location = ""
    Name = ""
    Image = None

    def __init__(self, image, name, location):
        self.Name = name
        self.Image = image
        self.Location = location

    def get_path_name(self):
        return self.Location + "\\" + self.Name

    def set_position(self, x, y):
        self.X = x
        self.Y = y

    def get_position(self):
        return self.X, self.Y

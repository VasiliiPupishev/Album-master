import os
import pygame
SCREEN_RESOLUTION = (1000, 600)
pygame.init()


class Album:
    X = 0
    Y = 0
    Items = None
    Location = ""
    Name = ""
    Image = None
    Pointer = 0
    MousePointer = None

    def __init__(self, name, location):
        self.Items = [[]]
        self.Image = pygame.image.load("Backgrounds\\album.png").convert_alpha()
        self.Name = name
        self.MousePointer = []
        self.Location = location + "/" + name

    def add_mpointer(self, item):
        from Item import Item
        if type(item) is Item:
            self.MousePointer.append(item)
        
    def get_path_name(self):
        return self.Location + "\\" + self.Name

    def add_item(self, item):
        for list in self.Items:
            if len(list) < 28:
                list.append(item)
                return
        self.Items.append([item])

    def del_item(self, item1):
        for list in self.Items:
            try:
                list.remove(item1)
            except:
                pass

    def get_all_items(self):
        res = []
        for list in self.Items:
            for item in list:
                res.append(item)
        return res

    def try_get_next_list(self):
        if self.Pointer >= len(self.Items) - 1:
            return False
        else:
            self.Pointer += 1
            return True

    def try_get_previous_list(self):
        if self.Pointer == 0:
            return False
        else:
            self.Pointer -= 1
            return True

    def set_position(self, x, y):
        self.X = x
        self.Y = y

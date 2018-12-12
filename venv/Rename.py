from RootClass import Root
from Album import Album
import copy
import pygame
from Item import Item
import os
from random import choice
from string import ascii_uppercase


class Rename:
    Pattern = 0
    Name = None
    Write = False
    EnumerableFlag = False
    RandomFlag = False

    def __init__(self):
        self.Pattern = 0
        self.Name = ""

    def run_rename(self, screen, root):
        self.print_addition_menu(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.search_events(event.pos, screen, root):
                            return True
                if event.type == pygame.KEYDOWN and self.Write:
                    if event.key == pygame.K_BACKSPACE and len(self.Name) > 0:
                        self.Name = self.Name[:len(self.Name) - 1]
                    else:
                        self.Name += chr(event.key)
                    self.print_addition_menu(screen)
            pygame.display.update()

    def print_addition_menu(self, screen):
        background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
        background_image = pygame.transform.scale(background_image, (1000, 600))
        font = pygame.font.SysFont('arial', 20)  # name caption
        loading_caption = font.render("Creating new album", False, (0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(loading_caption, (380, 10))
        font = pygame.font.SysFont('arial', 15)  # name caption
        loading_caption = font.render("Numerate", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (410, 450))
        loading_caption = font.render("Random name", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (377, 430))
        #---------------------------------------------------------------------------------------------------------------
        button = pygame.image.load("Backgrounds/plate.png")
        font = pygame.font.SysFont('arial', 20)
        button = pygame.transform.scale(button, (100, 40))
        loading_caption = font.render("Create", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (520, 510))
        loading_caption = font.render("Cancel", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (370, 510))
        screen.blit(button, (500, 500))
        screen.blit(button, (350, 500))
        button = pygame.transform.scale(button, (600, 70))
        screen.blit(button, (200, 230))
        font = pygame.font.SysFont('arial', 25)
        loading_caption = font.render(self.Name, False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (300, 250))
        button = pygame.image.load("Backgrounds/sq.png")
        button = pygame.transform.scale(button, (19, 19))
        screen.blit(button, (500, 450))
        screen.blit(button, (500, 430))

    def search_events(self, pos, screen, root):
        x, y = pos
        if 500 < x < 520:
            if 450 < y < 470:
                if not self.EnumerableFlag:
                    self.EnumerableFlag = True
                    button = pygame.image.load("Backgrounds/back.png")
                    button = pygame.transform.scale(button, (19, 19))
                    button = pygame.transform.rotate(button, 90)
                    screen.blit(button, (500, 450))
                else:
                    self.EnumerableFlag = False
                    self.print_addition_menu(screen)
            if 430 < y < 450:
                if not self.RandomFlag:
                    self.RandomFlag = True
                    button = pygame.image.load("Backgrounds/back.png")
                    button = pygame.transform.scale(button, (19, 19))
                    button = pygame.transform.rotate(button, 90)
                    screen.blit(button, (500, 430))
                else:
                    self.RandomFlag = False
                    self.print_addition_menu(screen)
        if 200 < x < 800:
            if 230 < y < 300:
                if not self.Write:
                    self.Write = True
        if 500 < y < 540:
            if 500 < x < 600:
                if root.get_current_album(False) is not None:
                    if len(self.Name) == 0:
                        self.Name = ""
                    i = 0
                    j = 1
                    for item in root.get_current_album(False).MousePointer:
                        new_name = self.Name
                        if self.EnumerableFlag:
                            new_name += str(i)
                        if self.RandomFlag:
                            new_name += ''.join(choice(ascii_uppercase) for i in range(5))
                        try:
                            os.rename(os.getcwd() + "/" + item.Location + "/" + item.Name,
                                      os.getcwd() + "/" + item.Location + "/" + new_name + ".jpg")
                        except FileExistsError:
                            new_name += "-copy(" + str(j) + ")"
                            j += 1
                            os.rename(os.getcwd() + "/" + item.Location + "/" + item.Name,
                                      os.getcwd() + "/" + item.Location + "/" + new_name + ".jpg")
                        item.Name = new_name + ".jpg"
                        i += 1
                return True
            if 350 < x < 450:
                return True
        return False

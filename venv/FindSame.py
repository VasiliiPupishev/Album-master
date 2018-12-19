from RootClass import Root
from Album import Album
import copy
import pygame
from Item import Item
from PIL import Image
import os
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pickle


# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/


class Same:
    items = None
    images = None
    res = None
    Album = None
    Flag = False
    Albums = None

    def __init__(self, root):
        self.res = {}
        self.images = []
        self.items = []
        self.Albums = []
        self.Album = Album("name", "location")
        if root.get_current_album(False) is None:
            print(len(root.Albums))
            for line in root.Albums:
                for album in line:
                    for list in album.Items:
                        for item in list:
                            if type(item) is not Album:
                                self.items.append(item)
                            else:
                                continue
        else:
            print(len(root.get_current_album(False).get_all_items()))
            for list in root.get_current_album(False).Items:
                for item in list:
                    if type(item) is not Album:
                        self.items.append(item)
                    else:
                        continue

    def find_copy(self, per, image_bank):
        number = 0
        for image in self.items:
            try:
                if not self.in_res(image) or type(image) is not Item:
                    continue
                self.res[image] = []
                image_origin = cv2.imread(os.getcwd() + "\\" + image.Location + "\\" + image.Name)
                image_origin = cv2.resize(image_origin, (200, 200))
                image_origin = cv2.cvtColor(image_origin, cv2.COLOR_BGR2GRAY)
                temp = Album("set №" + str(number), "set1")
                temp.Index = 0
                number += 1
                for image1 in self.items:
                    image1_origin = cv2.imread(os.getcwd() + "\\" + image1.Location + "\\" + image1.Name)
                    image1_origin = cv2.resize(image1_origin, (200, 200))
                    image1_origin = cv2.cvtColor(image1_origin, cv2.COLOR_BGR2GRAY)
                    res = ssim(image_origin, image1_origin)
                    if res >= 1 - per:
                        self.res[image].append(image1)
                        self.Album.add_item(image1)
                        temp.add_item(image1)
                self.Albums.append(temp)
            except Exception:
                continue

    def in_res(self, item):
        for key in self.res.keys():
            if key == item:
                return False
            for i in self.res[key]:
                if i == item:
                    return False
        return True

    def print_filter(self, screen, root, im_Bank):
        self.screen_draw(screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('data.pickle', 'wb') as f:
                        pickle.dump(root, f)
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        fl = self.search_events(event.pos, screen, root, im_Bank)
                        if type(fl) is not str and fl:
                            if self.Flag:
                                if root.get_current_album(False) is None:
                                    for item in self.Albums:
                                        root.add_album(item)
                                else:
                                    for item in self.Albums:
                                        print(root.get_current_album(False).Name)
                                        root.get_current_album(False).add_item(item)
                                return True
                            return False
                        elif fl == "exit":
                            return "exit"
            pygame.display.update()

    def search_events(self, pos, screen, root, im_bank):
        x, y = pos
        if 170 < x < 190:
            if 400 < y < 420:
                if not self.Flag:
                    self.Flag = True
                    button = pygame.image.load("Backgrounds/back.png")
                    button = pygame.transform.scale(button, (19, 19))
                    button = pygame.transform.rotate(button, 90)
                    screen.blit(button, (170, 400))
                else:
                    self.Flag = False
                    self.screen_draw(screen)
        if 750 < x < 850:
            if 100 < y < 140:
                self.print_loading(screen)
                self.find_copy(0, im_bank)
                return True
            if 200 < y < 240:
                self.print_loading(screen)
                self.find_copy(0.27, im_bank)
                return True
            if 300 < y < 340:
                self.print_loading(screen)
                self.find_copy(0.5, im_bank)
                return True
        if 440 < x < 540:
            if 480 < y < 520:
                return "exit"
        return False

    def print_loading(self, screen):
        background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
        background_image = pygame.transform.scale(background_image, (1000, 600))
        font = pygame.font.SysFont('arial', 30)
        loading_caption = font.render("LOADING...", False, (0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(loading_caption, (400, 290))
        pygame.display.update()

    def screen_draw(self, screen):
        background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
        background_image = pygame.transform.scale(background_image, (1000, 600))
        font = pygame.font.SysFont('arial', 20)  # name caption
        loading_caption = font.render("Set up filter.", False, (0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(loading_caption, (430, 10))
        font = pygame.font.SysFont('arial', 30)  # name caption
        loading_caption = font.render("Find with full similarity", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 100))
        loading_caption = font.render("Find with 75% similarity", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 200))
        loading_caption = font.render("Find with 50% similarity", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 300))
        font = pygame.font.SysFont('arial', 15)  # name caption
        loading_caption = font.render("Group in albums", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 400))
        # ---------------------------------------------------------------------------------------------------------------
        button = pygame.image.load("Backgrounds/plate.png")
        font = pygame.font.SysFont('arial', 20)
        button = pygame.transform.scale(button, (100, 40))
        loading_caption = font.render("Start", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (780, 110))
        screen.blit(button, (750, 100))
        screen.blit(loading_caption, (780, 210))
        screen.blit(button, (750, 200))
        screen.blit(loading_caption, (780, 310))
        screen.blit(button, (750, 300))
        button = pygame.transform.scale(button, (100, 40))
        loading_caption = font.render("Cancel", False, (0, 0, 0))
        screen.blit(button, (440, 480))
        screen.blit(loading_caption, (460, 490))
        button = pygame.image.load("Backgrounds/sq.png")
        button = pygame.transform.scale(button, (19, 19))
        screen.blit(button, (170, 400))

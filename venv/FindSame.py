from RootClass import Root
from Album import Album
import copy
import pygame
from PIL import Image
import os
from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

#https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/


class Same:
    items = None
    images = None
    res = None
    Album = None

    def __init__(self, root):
        self.res = {}
        self.images = []
        self.items = []
        self.Album = Album("name", "location")
        if root.Current_Album is None:
            for line in root.Albums:
                for album in line:
                    for list in album.Items:
                        for item in list:
                            self.items.append(item)
        else:
            for list in root.Current_Album.Items:
                for item in list:
                    self.items.append(item)

    def find_copy(self, per):
        for image in self.items:
            if not self.in_res(image):
                continue
            self.res[image] = []
            image_origin = cv2.imread(os.getcwd() + "\\" + image.Location + "\\" + image.Name)
            image_origin = cv2.resize(image_origin, (200, 200))
            image_origin = cv2.cvtColor(image_origin, cv2.COLOR_BGR2GRAY)
            for image1 in self.items:
                image1_origin = cv2.imread(os.getcwd() + "\\" + image1.Location + "\\" + image1.Name)
                image1_origin = cv2.resize(image1_origin, (200, 200))
                image1_origin = cv2.cvtColor(image1_origin, cv2.COLOR_BGR2GRAY)
                res = ssim(image_origin, image1_origin)
                print(res)
                if res >= 1 - per:
                    self.res[image].append(image1)
                    self.Album.add_item(image1)

    def in_res(self, item):
        for key in self.res.keys():
            if key == item:
                return False
            for i in self.res[key]:
                if i == item:
                    return False
        return True

    @staticmethod
    def print_filter(screen):
        print("helllo")
        background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
        background_image = pygame.transform.scale(background_image, (1000, 600))
        font = pygame.font.SysFont('arial', 20) #name caption
        loading_caption = font.render("Set up filter.", False, (0, 0, 0))
        screen.blit(background_image, (0, 0))
        screen.blit(loading_caption, (500-70, 10))
        font = pygame.font.SysFont('arial', 30)  # name caption
        loading_caption = font.render("Find with full similarity", False, (0, 0, 0)) #grouping in albums
        screen.blit(loading_caption, (40, 100))
        loading_caption = font.render("Find with 75% similarity", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 200))
        loading_caption = font.render("Find with 50% similarity", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 300))
        font = pygame.font.SysFont('arial', 15)  # name caption
        loading_caption = font.render("Group in albums", False, (0, 0, 0))  # grouping in albums
        screen.blit(loading_caption, (40, 400))
        #---------------------------------------------------------------------------------------------------------------





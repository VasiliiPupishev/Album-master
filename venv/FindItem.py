from RootClass import Root
from Album import Album
import copy
import pygame
from Item import Item
import os
from random import choice
from string import ascii_uppercase


class Find:
   Name = None
   Write = False
   Album = None

   def run_find(self, screen, root):
       self.Name = ""
       self.Album = Album("result_search", "")
       self.print_addition_menu(screen)
       while True:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   raise SystemExit
               if event.type == pygame.MOUSEBUTTONDOWN:
                   if event.button == 1:
                       if self.search_events(event.pos, screen, root):
                           return self.Album
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
       button = pygame.image.load("Backgrounds/plate.png")
       font = pygame.font.SysFont('arial', 20)
       button = pygame.transform.scale(button, (100, 40))
       loading_caption = font.render("Find", False, (0, 0, 0))  # grouping in albums
       screen.blit(loading_caption, (537, 510))
       loading_caption = font.render("Cancel", False, (0, 0, 0))  # grouping in albums
       screen.blit(loading_caption, (370, 510))
       screen.blit(button, (500, 500))
       screen.blit(button, (350, 500))
       button = pygame.transform.scale(button, (600, 70))
       screen.blit(button, (200, 230))
       font = pygame.font.SysFont('arial', 25)
       loading_caption = font.render(self.Name, False, (0, 0, 0))  # grouping in albums
       screen.blit(loading_caption, (300, 250))

   def search_events(self, pos, screen, root):
       x, y = pos
       if 200 < x < 800:
           if 230 < y < 300:
               if not self.Write:
                   self.Write = True
       if 500 < y < 540:
           if 500 < x < 600:
               fi = root.get_current_album(False)
               if fi is not None:
                   for item in fi.get_all_items():
                       if item.Name[:len(item.Name) - 4] == self.Name:
                           self.Album.add_item(item)
               else:
                   items = []
                   for al in root.Albums:
                       for al1 in al:
                           for i in al1.get_all_items():
                               items.append(i)
                   for item in items:
                       if item.Name[:len(item.Name) - 4] == self.Name:
                           self.Album.add_item(item)
               return True
           if 350 < x < 450:
               return True
       return False



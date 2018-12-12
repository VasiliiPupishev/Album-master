import pygame
import sys
import time
from RootClass import Root
from Album import Album
from Item import Item
import os

SCREEN_RESOLUTION = (1000, 600)
RETREAT = (50, 40)
image_size = (90, 90)
PLATE_SIZE = (100, 100)
DIR = os.getcwd()

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('arial', 15)
screen = pygame.display.set_mode(SCREEN_RESOLUTION, pygame.RESIZABLE)
pygame.display.set_caption("Your Photos")
logo = pygame.image.load("Backgrounds\\logo.jpg")
pygame.display.set_icon(logo)


def main():
    items = []
    draw_loading()
    background_image = pygame.image.load('Backgrounds\\index.jpg').convert_alpha()
    background_image = pygame.transform.scale(background_image, SCREEN_RESOLUTION)
    font = pygame.font.SysFont('arial', 30)
    root = Root(DIR, "Images")
    root.init("Images", root.Albums[0], True)
    #print(len(root.Albums[0]))
    loading_caption = font.render("LOADING...", False, (0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(loading_caption, (int(SCREEN_RESOLUTION[0] / 2) - 50, int(SCREEN_RESOLUTION[1] / 2) - 10))
    exit = False
    print_albums(root)
    TIMER = 0
    while not exit:
        TIMER += 1
        if TIMER == 5000:
            TIMER = 0
            root.update("Images")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    search_event(root, event.pos)
                if event.button == 3:
                    set_mouse_pointer(root, event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    copy_item(root)
                if event.key == pygame.K_v:
                    paste_item(root)
                if event.key == pygame.K_m:
                    move_item(root)
                if event.key == pygame.K_r:
                    rename_item(root, screen)
                if event.key == pygame.K_F1:
                    root.ALGS = True
                    find_copy(root, screen)
                if event.key == pygame.K_a:
                    fl = root.get_current_album(False)
                    if fl is not None:
                        fl.MousePointer.clear()
                        for item in fl.get_all_items():
                            fl.add_mpointer(item)
                        print_albums(fl)
        pygame.display.update()
    pygame.quit()
    sys.exit()


def find_copy(root, screen):
    from FindSame import Same
    same = Same(root)
    fl = same.print_filter(screen, root)
    if fl:
        if root.get_current_album(False) is not None:
            print_albums(root.get_current_album(False))
        else:
            print_albums(root)
    elif fl == "exit":
        if root.get_current_album(False) is None:
            print_albums(root)
        else:
            print_albums(root.get_current_album(False))
    else:
        print_albums(same.Album)
        root.add_current_album(same.Album)


def get_delta(image_rect):
    delta_x = 0
    delta_y = 0
    if image_rect[2] > image_rect[3]:
        delta_y = image_rect[3] / image_rect[2]
        delta_x = 1
    else:
        delta_y = 1
        delta_x = image_rect[2] / image_rect[3]
    return delta_x, delta_y


def rename_item(root, screen):
    from Rename import Rename
    rename = Rename()
    rename.run_rename(screen, root)
    fl = root.get_current_album(False)
    if fl is None:
        print_albums(root)
    else:
        print_albums(fl)


def move_item(root):
    import shutil
    if len(root.Buffer) == 0:
        return
    for i in root.Buffer:
        item = i[0]
        try:
            shutil.move(DIR + "/" + item.Location + "/" + item.Name, DIR + "/" + root.get_current_album(False).Location)
        except Exception:
            print("oooops")
        root.get_current_album(False).add_item(item)
        i[1].del_item(item)
    root.Buffer.clear()
    print_albums(root.get_current_album(False))


def copy_item(root):
    if len(root.get_current_album(False).MousePointer) > 0:
        root.Buffer.clear()
        for item in root.get_current_album(False).MousePointer:
            root.Buffer.append((item, root.get_current_album(False)))


def paste_item(root):
    if len(root.Buffer) != 0:
        import shutil
        for i in root.Buffer:
            item = i[0]
            try:
                shutil.copy(DIR + "/" + item.Location + "/" + item.Name, DIR + "/" + root.get_current_album(False).Location + "/" + item.Name[:-4] + "copy.jpg", follow_symlinks=True)
            except Exception:
                print("ooooops")
            root.get_current_album(False).add_item(item)
        root.Buffer.clear()
        print_albums(root.get_current_album(False))


def set_mouse_pointer(root, pos):
    if root.get_current_album(False) is None:
        return
    item = get_album(root.get_current_album(False).Items[root.get_current_album(False).Pointer], pos)
    if item is not None:
        if root.get_current_album(False).MousePointer.__contains__(item):
            root.get_current_album(False).MousePointer.remove(item)
            print_albums(root.get_current_album(False))
            return
        root.get_current_album(False).add_mpointer(item)
        print_albums(root.get_current_album(False))


def draw_loading():
    background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
    background_image = pygame.transform.scale(background_image, SCREEN_RESOLUTION)
    font = pygame.font.SysFont('arial', 30)
    loading_caption = font.render("LOADING...", False, (0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(loading_caption, (int(SCREEN_RESOLUTION[0] / 2) - 100, int(SCREEN_RESOLUTION[1] / 2) - 10))
    pygame.display.update()


def search_event(root, pos):
    print(root.List_Current)
    x, y = pos
    #if root.ALGS and y < 33 and x < 33:
        #root.ALGS = False
        #if root.get_current_album(False) is not None:
            #print_albums(root.get_current_album(True))
        #else:
            #print_albums(root)
        #return
    if y < 33 and x < 33 and root.get_current_album(False) is not None:
        print("heyyyyy")
        root.get_current_album(False).MousePointer.clear()
        print(root.get_current_album(True))
        print(root.get_current_album(False))
        if root.get_current_album(False) is not None:
            print_albums(root.get_current_album(False))
        else:
            print_albums(root)
        #print_albums(root.get_current_album(False))
        return
    if x > SCREEN_RESOLUTION[0] - 33 and y > SCREEN_RESOLUTION[1] - 33 and root.get_current_album(False) is not None:
        if root.get_current_album(False).try_get_next_list():
            print_albums(root.get_current_album(False))
        return
    if x < 33 and y > SCREEN_RESOLUTION[1] - 33 and root.get_current_album(False) is not None:
        if root.get_current_album(False).try_get_previous_list():
            print_albums(root.get_current_album(False))
        return
    if root.get_current_album(False) is not None:
        item = get_album(root.get_current_album(False).Items[root.get_current_album(False).Pointer], pos)
        if item is not None:
            if type(item) is Item:
                path = os.path.abspath(item.Location + "/" + item.Name)
                os.startfile(path)
            else:
                root.add_current_album(item)
                print_albums(item)
    else:
        next_album = get_album(root.Albums[0], pos)
        if next_album is not None:
            root.add_current_album(next_album)
            print_albums(next_album)
    if 955 > x > 925:
        if 594 > y > 564:
            #root.ALGS = True
            draw_loading()
            find_copy(root, screen)
    if 914 > x > 892:
        if 594 > y > 564:
            from AddAlbum import AddAlbum
            additor = AddAlbum()
            additor.run_adding(root, screen)
            temp = root.get_current_album(False)
            if temp is None:
                print_albums(root)
            else:
                print_albums(temp)


def print_addition_menu(root):
    background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
    background_image = pygame.transform.scale(background_image, (1000, 600))
    font = pygame.font.SysFont('arial', 20)  # name caption
    loading_caption = font.render("Creating new album", False, (0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(loading_caption, (430, 10))
    font = pygame.font.SysFont('arial', 15)  # name caption
    loading_caption = font.render("Is this folder", False, (0, 0, 0))  # grouping in albums
    screen.blit(loading_caption, (40, 400))
    # ---------------------------------------------------------------------------------------------------------------
    button = pygame.image.load("Backgrounds/plate.png")
    font = pygame.font.SysFont('arial', 20)
    button = pygame.transform.scale(button, (100, 40))
    loading_caption = font.render("Create", False, (0, 0, 0))  # grouping in albums
    screen.blit(loading_caption, (670, 510))
    screen.blit(button, (650, 500))
    button = pygame.image.load("Backgrounds/sq.png")
    button = pygame.transform.scale(button, (19, 19))
    screen.blit(button, (170, 400))



def get_album(albums, event_position):
    (x, y) = event_position
    for album in albums:
        if album.X < x < album.X + PLATE_SIZE[0] and \
                album.Y < y < album.Y + PLATE_SIZE[1]:
                return album
    return None


def draw_menu():
    back_image = pygame.image.load('Backgrounds/back.png')
    back_image = pygame.transform.scale(back_image, (27, 27))
    screen.blit(back_image, (5, 5))
    screen.blit(back_image, (5, SCREEN_RESOLUTION[1] - 35))
    back_image = pygame.transform.rotate(back_image, 180)
    screen.blit(back_image, (SCREEN_RESOLUTION[0]-35, SCREEN_RESOLUTION[1]-35))
    back_image = pygame.image.load('Backgrounds/21.png')
    back_image = pygame.transform.scale(back_image, (30, 30))
    screen.blit(back_image, (925, 564))
    back_image = pygame.image.load('Backgrounds/add.png')
    back_image = pygame.transform.scale(back_image, (22, 22))
    screen.blit(back_image, (890, 569))
    back_image = pygame.image.load('Backgrounds/search.png')
    back_image = pygame.transform.scale(back_image, (27, 27))
    screen.blit(back_image, (855, 569))


def get_coordinate(x, y, rect):
    x = x + int(PLATE_SIZE[0] / 2) - int(rect[2] / 2)
    y = y + int(PLATE_SIZE[1] / 2) - int(rect[3] / 2)
    return x, y


def print_albums(album):
    background_image = pygame.image.load('Backgrounds/index.jpg').convert_alpha()
    background_image = pygame.transform.scale(background_image, SCREEN_RESOLUTION)
    font = pygame.font.SysFont('arial', 20)
    loading_caption = font.render(album.Name, False, (0, 0, 0))
    screen.blit(background_image, (0, 0))
    screen.blit(loading_caption, (int(SCREEN_RESOLUTION[0] / 2) - 60, 5))
    pygame.display.update()
    draw_menu()
    plate = pygame.image.load("Backgrounds/plate.png")
    plate = pygame.transform.scale(plate, PLATE_SIZE)
    #if type(album) is not Root and len(album.MousePointer) > 0:
    #    mousePointer = pygame.image.load('Backgrounds/sq.png').convert_alpha()
    #    mousePointer = pygame.transform.scale(mousePointer, (PLATE_SIZE[0] + 3, PLATE_SIZE[1] + 3))
    #    for mp in album.MousePointer:
    #            pos = mp.get_position()
    #            screen.blit(mousePointer, (pos[0] - 7, pos[1] - 24))
    current_album = None
    if type(album) is Root:
        current_album = album.Albums[album.Pointer]
    else:
        current_album = album.Items[album.Pointer]
    indent_x = RETREAT[0]
    indent_y = RETREAT[1]
    i = 0
    mousePointer = pygame.image.load('Backgrounds/sq.png').convert_alpha()
    mousePointer = pygame.transform.scale(mousePointer, (PLATE_SIZE[0] + 3, PLATE_SIZE[1] + 3))
    for item in current_album:
        #print(type(item))
        album_image = item.Image
        image_rect = album_image.get_rect()  # scaling
        delta_x, delta_y = get_delta(image_rect)
        temp_x = int(image_size[0] * delta_x)
        temp_y = int(image_size[1] * delta_y)
        album_image = pygame.transform.scale(album_image, (temp_x, temp_y))
        (x, y) = get_coordinate(indent_x, indent_y, album_image.get_rect())
        item.set_position(x, y)
        if type(album) is Album and album.MousePointer.__contains__(item):
            pos = item.get_position()
            screen.blit(mousePointer, (pos[0] - 7, pos[1] - 24))
        screen.blit(plate, (indent_x, indent_y))
        screen.blit(album_image, (x, y))  # ending output
        caption = get_caption(item.Name)
        screen.blit(caption[1], (indent_x + caption[0], indent_y + PLATE_SIZE[1]))
        indent_x = indent_x + PLATE_SIZE[0] + 30
        i += 1
        if i > 6:
            i = 0
            indent_x = RETREAT[0]
            indent_y = indent_y + PLATE_SIZE[1] + 25


def get_caption(name):
    dc = 0
    res = ""
    if len(name) > 13:
        res = name[:13] + "..."
    else:
        res = name
        dc = int(int((14 - len(res)) / 2) * 8.5)
    return dc, myfont.render(res, False, (0, 0, 0))


main()


from ssl import ALERT_DESCRIPTION_HANDSHAKE_FAILURE
from textwrap import fill
from numpy import swapaxes
import pygame
import random
import water_physic
import earth_physic
import block_ids as id
import animations as anim
import time
from math import *

class Game:
    def __init__(self, dim):
        self.map = [[0 for _ in range(int(dim[1]/10))]
                    for _ in range(int(dim[0]/10))]
        """
        la map est initée
        Chaque pixel représente un block
        """

        self._pixsize = 10
        self._o_pixsize = 10
        self.screen_size = (dim[0], dim[1])
        self._size = dim
        self._decalX = 0
        self._decalY = 0
        self._zoom = 1
        self._zoom_target = 1

        self._selected = id.EARTH_ID

        self._textures = {
            id.WATER_ID: pygame.image.load("./assets/eau/eau.png")
        }

        self.sized_textures = {
            id.WATER_ID: pygame.image.load("./assets/eau/eau.png")
        }

        self._animations = {
            id.WATER_ID: anim.animation("./assets/eau/")
        }

        self.background = pygame.image.load("./background.png")

        self.sized_background = self.background

        self._first_plan = []
        self._second_plan = []

        self.time = 0

    def get_coor(self, coor):
        return self.map[coor[0]][coor[1]]

    def set_zoom(self, mult):
        self._pixsize = round(self._o_pixsize * mult)
        if self._pixsize < 5:
            self._pixsize = 5
            return

        if self._pixsize > 100:
            self._pixsize = 100
            return
        for ids in self._textures:
            self.sized_textures[ids] = pygame.transform.scale(
                self._textures[ids], (self._pixsize, self._pixsize))
        for ids in self._animations:
            self._animations[ids].rescale(self._pixsize)

        self._size = (
            round(self.screen_size[0]*mult), round(self.screen_size[1]*mult))
        self.sized_background = pygame.transform.scale(
            self.background, self._size)

    def set_zoom_target(self, mult):
        self._zoom_target = mult

    def get_minimap_side(self, minimap, side):
        if side == "N":
            return minimap[0][1]
        if side == "S":
            return minimap[2][1]
        if side == "O":
            return minimap[1][0]
        if side == "E":
            return minimap[1][2]

    def set_point(self, x, y, b_id):
        self.map[x][y] = b_id
        minimap = self.get_square_of_map(x, y)
        if not minimap:
            return
        self.update(x, y)

    def update(self, x, y):
        minimap = self.get_square_of_map(x, y)
        if not minimap:
            return
        if id.is_static(self.get_minimap_side(minimap, "N")):
            self.map[x -
                     1][y] = id.unstatic_block(self.get_minimap_side(minimap, "N"))
        if id.is_static(self.get_minimap_side(minimap, "S")):
            self.map[x +
                     1][y] = id.unstatic_block(self.get_minimap_side(minimap, "S"))
        if id.is_static(self.get_minimap_side(minimap, "E")):
            self.map[x][y +
                        1] = id.unstatic_block(self.get_minimap_side(minimap, "E"))
        if id.is_static(self.get_minimap_side(minimap, "O")):
            self.map[x][y -
                        1] = id.unstatic_block(self.get_minimap_side(minimap, "O"))

    def draw_pix(self, block_id, coor, window):
        p = pygame.Surface((self._pixsize, self._pixsize))
        if block_id == id.WATER_ID or block_id == id.STATIC_WATER_ID:
            t = self._animations[id.WATER_ID].image(self.time)
            p.blit(t, (0, 0))
        elif block_id == id.EARTH_ID or block_id == id.STATIC_EARTH_ID:
            p.fill((105, 76, 43))
        elif block_id == id.SAND_ID or block_id == id.STATIC_SAND_ID:
            p.fill("yellow")
        elif block_id == id.GRASS_ID or block_id == id.STATIC_GRASS_ID:
            p.fill("green")
        else:
            p.fill("grey")
        shadow = pygame.Surface((self._pixsize, self._pixsize))
        self._second_plan.append(
            (shadow, (coor[0]*self._pixsize-int(self._decalX/2), coor[1]*self._pixsize-int(self._decalY/2))))

        self._first_plan.append(
            (p, (coor[0]*self._pixsize-self._decalX, coor[1]*self._pixsize-self._decalY)))

    def get_square_of_map(self, x, y):
        if not (0 < x < len(self.map)-1 and 0 < y < len(self.map[0])-1):
            return False
        bit = []
        bit.append(self.map[x-1][y-1:y+2])
        bit.append(self.map[x][y-1:y+2])
        bit.append(self.map[x+1][y-1:y+2])
        return bit

    def spill_water(self, x, y):
        minimap = self.get_square_of_map(x, y)
        if not minimap:
            return

        if water_physic.is_type_water(minimap[0][1]) and water_physic.is_type_water(minimap[1][0]) and water_physic.is_type_water(minimap[1][2]) and water_physic.is_type_water(minimap[2][1]):
            self.map[x][y] = id.STATIC_WATER_ID

        if minimap[0][1] == id.NOTHING_ID:
            self.set_point(x-1, y, id.WATER_ID)
        if minimap[1][0] == id.NOTHING_ID:
            self.set_point(x, y-1, id.WATER_ID)
        if minimap[1][2] == id.NOTHING_ID:
            self.set_point(x, y+1, id.WATER_ID)
        if minimap[2][1] == id.NOTHING_ID:
            self.set_point(x+1, y, id.WATER_ID)

    def erode(self, x, y):
        minimap = self.get_square_of_map(x, y)
        if not minimap:
            return
        if earth_physic.erosion(minimap):
            self.set_point(x, y, id.SAND_ID)

    def get_view_boundary(self):
        # return (0, 0, 10+self._pixsize, 10+self._pixsize)
        # return (0, 0, len(self.map), len(self.map[0]))
        return (round(self._decalX/self._pixsize), round(self._decalY/self._pixsize), round(self.screen_size[0]/self._pixsize), round(self.screen_size[1]/self._pixsize))

    def draw(self, window: pygame.surface.Surface):
        xmin, ymin, xmax, ymax = self.get_view_boundary()
        if xmin < 0:
            xmin = 0
        if ymin < 0:
            ymin = 0

        for px, x in enumerate(self.map[xmin:xmin+xmax]):
            for py, y in enumerate(x[ymin:ymin+ymax]):
                if y != id.NOTHING_ID:
                    self.draw_pix(y, (xmin+px, ymin+py), window)
                if y == id.WATER_ID:
                    self.spill_water(xmin+px, ymin+py)
                if y == id.EARTH_ID:
                    self.erode(xmin+px, ymin+py)
        for i in self._second_plan:
            window.blit(i[0], i[1])
        self._second_plan.clear()
        for i in self._first_plan:
            window.blit(i[0], i[1])
        self._first_plan.clear()

        return 0

    def actualiser(self, window):
        window.fill("black")
        window.blit(self.sized_background,
                    [-int(self._decalX/2), -int(self._decalY/2)])

        mouse_event = pygame.mouse.get_pressed(3)
        keyboard_event = pygame.key.get_pressed()

        if mouse_event[0]:
            x, y = pygame.mouse.get_pos()
            dx = x % self._pixsize
            dy = y % self._pixsize
            x = int((x-dx+self._decalX)/self._pixsize)
            y = int((y-dy+self._decalY)/self._pixsize)
            if (0 < x < len(self.map)) and (0 < y < len(self.map[0])):
                self.set_point(x, y, self._selected)

        if keyboard_event[pygame.K_w]:
            self._selected = id.WATER_ID
        if keyboard_event[pygame.K_s]:
            self._selected = id.static_block(self._selected)
        if keyboard_event[pygame.K_e]:
            self._selected = id.EARTH_ID
        if keyboard_event[pygame.K_g]:
            self._selected = id.GRASS_ID

        if keyboard_event[pygame.K_EQUALS]:
            qi = 0
            while qi < 50000:
                qi += 1
            self.set_zoom_target(self._zoom+self._zoom/2)
        if keyboard_event[pygame.K_MINUS]:
            qi = 0
            while qi < 50000:
                qi += 1
            self.set_zoom_target(self._zoom-self._zoom/2)

        if keyboard_event[pygame.K_LEFT]:
            self._decalX -= self._pixsize
        if keyboard_event[pygame.K_RIGHT]:
            self._decalX += self._pixsize
        if keyboard_event[pygame.K_UP]:
            self._decalY -= self._pixsize
        if keyboard_event[pygame.K_DOWN]:
            self._decalY += self._pixsize

        if self._zoom != self._zoom_target:
            if self._zoom_target > self._zoom:
                self._zoom += round((self._zoom_target-self._zoom)/4, 2)
                self.set_zoom(self._zoom)
            else:
                self._zoom -= round((self._zoom-self._zoom_target)/4, 2)
                self.set_zoom(self._zoom)

        self.time += 1
        self.draw(window)

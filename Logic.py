import sqlite3

import PIL.ImageQt
import PyQt5.QtGui
import noise
import sys
from PIL import Image
import numpy as np
import math

seed = 256
persistence = 0.5
scale = 100
octaves = 6
flat_arr = []

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

def create_map():
    global seed, octaves, lacunarity, scale
    # region Основыне Переменные карты
    shape = (600, 900)
    persistence = 0.5
    threshold = 50

    lightblue = [0, 191, 255]
    blue = [65, 105, 225]
    green = [34, 139, 34]
    darkgreen = [0, 100, 0]
    sandy = [210, 180, 140]
    beach = [238, 214, 175]
    snow = [255, 250, 250]
    mountain = [139, 137, 137]

    # endregion
    # region Формирование карты шума перлина
    def rgb_norm(world):
        world_min = np.min(world)
        world_max = np.max(world)
        norm = lambda x: (x - world_min / (world_max - world_min)) * 255
        return np.vectorize(norm)

    def prep_world(world):
        norm = rgb_norm(world)
        world = norm(world)
        return world

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i / scale, j / scale, octaves=octaves, persistence=persistence,
                                        lacunarity=lacunarity, repeatx=600, repeaty=900, base=seed)

    # endregion

    # region присваивание цветов
    def add_color(world):
        color_world = np.zeros(world.shape + (3,))
        for i in range(shape[0]):
            for j in range(shape[1]):
                if world[i][j] < -0.05:
                    color_world[i][j] = blue
                elif world[i][j] < 0:
                    color_world[i][j] = beach
                elif world[i][j] < 0.20:
                    color_world[i][j] = green
                elif world[i][j] < 0.35:
                    color_world[i][j] = mountain
                elif world[i][j] < 1.0:
                    color_world[i][j] = snow

        return color_world

    color_world = add_color(world).astype(np.uint8)
    # endregion

    # region добавление кругового шума для ограничения зоны генерирования объектов
    center_x, center_y = shape[1] // 2, shape[0] // 2
    circle_grad = np.zeros_like(world)

    for y in range(world.shape[0]):
        for x in range(world.shape[1]):
            distx = abs(x - center_x)
            disty = abs(y - center_y)
            dist = math.sqrt(distx * distx + disty * disty)
            circle_grad[y][x] = dist

    max_grad = np.max(circle_grad)
    circle_grad = circle_grad / max_grad
    circle_grad -= 0.5
    circle_grad *= 2.0
    circle_grad = -circle_grad
    world_noise = np.zeros_like(world)

    for i in range(shape[0]):
        for j in range(shape[1]):
            if circle_grad[i][j] > 0:
                world_noise[i][j] = (world[i][j] * circle_grad[i][j])

    # endregion

    # region отрисовка цветов
    def add_color2(world):
        color_world = np.zeros(world.shape + (3,))
        for i in range(shape[0]):
            for j in range(shape[1]):
                if world[i][j] < threshold + 100:
                    color_world[i][j] = blue
                elif world[i][j] < threshold + 102:
                    color_world[i][j] = beach
                elif world[i][j] < threshold + 104:
                    color_world[i][j] = sandy
                elif world[i][j] < threshold + 115:
                    color_world[i][j] = green
                elif world[i][j] < threshold + 130:
                    color_world[i][j] = darkgreen
                elif world[i][j] < threshold + 137:
                    color_world[i][j] = mountain
                else:
                    color_world[i][j] = snow
        return color_world

    # endregion

    island_world_grad = add_color2(prep_world(world_noise)).astype(np.uint8)
    return island_world_grad


def save_map(id, sd, os, ly, se):
    global seed, octaves, lacunarity, scale, flat_arr
    seed = sd
    octaves = os
    lacunarity = ly
    scale = se
    im = Image.new(mode="RGB", size=(900, 600))
    pixels = im.load()
    x, y = im.size
    map_array = create_map()

    for i in range(x):
        for j in range(y):
            pixels[i, j] = int(map_array[j][i][0]), int(map_array[j][i][1]), int(map_array[j][i][2])
            flat_arr.append([int(map_array[j][i][0]), int(map_array[j][i][1]), int(map_array[j][i][2])])
    return im

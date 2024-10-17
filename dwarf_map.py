import pygame
from perlin_noise import PerlinNoise
import random as rd

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

pixel_size = 6
ScreenWidth = 800
ScreenHeigth = 800
world_size = [int(ScreenWidth / pixel_size), int(ScreenHeigth / pixel_size)]

sea_level = 0.5
plain_level = 0.505
mountain_level = 0.615
glacier_level = 0.85

octave = 1
step = 0.04

# Génération du Perlin Noise
def getNoise(seed, octave, size, step):
    noise = PerlinNoise(octave, seed)
    values = []
    for i in range(size[0]) :
        values.append([])
        for j in range(size[1]) :
            value = noise([i*step,j*step])
            value = max(min(value+0.5, 1),0)
            values[i].append(value)
    return values

world_data = [] # contiendra pour chaque pixels les infos suivantes : value, region, biome

def modifyNoise(values) :
    for i in range(len(values)):
        world_data.append([]) # Prépare la la liste pour générer les régions et les biomes
        for j in range(len(values[i])):
            if values[i][j] > sea_level:
                values[i][j] = 2*(values[i][j]-0.5)**2+0.5 # Rend les montagnes plus pentues
            world_data[i].append({"value" : values[i][j], "region" : "", "biome" : None})
            setRegionType(values[i][j], i,j)
            setBiome(i,j)
    return values

def setRegionType(value, x_pos, y_pos): # Les régions dépendent de la hauteur : Mer, plages, plaines, montagnes, glaciers
    if value < sea_level:
        world_data[x_pos][y_pos]["region"] = "sea"
    elif value < plain_level:
        world_data[x_pos][y_pos]["region"] = "beach"
    elif value < mountain_level:
        world_data[x_pos][y_pos]["region"] = "plain"
    elif value < glacier_level:
        world_data[x_pos][y_pos]["region"] = "mountain"
    else:
        world_data[x_pos][y_pos]["region"] = "glacier"
        
forest_noise = getNoise(round(rd.random()*1000), 1.5,world_size, 0.04)
# Les biomes dépendent du type de région
# plaines : forêt, prairie, déserts
def setBiome(x_pos, y_pos):
    if world_data[x_pos][y_pos]["biome"] == None and world_data[x_pos][y_pos]["region"] == "plain" and forest_noise[x_pos][y_pos] > 0.5:
        world_data[x_pos][y_pos]["biome"] ="forest"
    if world_data[x_pos][y_pos]["biome"] == None and world_data[x_pos][y_pos]["region"] == "plain" and world_data[x_pos][y_pos]["value"] > mountain_level-0.04:
        world_data[x_pos][y_pos]["biome"] = "taiga"
    
region_colors = {
    "sea": (2, 128, 182), # (0,0,int((255-sea_level*255)+value*255))
    "beach": (255, 251, 206),
    "plain": (105, 241, 118),
    "mountain": ( 126, 126, 126 ), # int(-150*value+(plain_level+mountain_level)*255)
    "glacier": ( 246, 246, 246 ) # int(value**1.5*255)
}
biome_colors = {
    "forest": (31, 176, 44),
    "taiga": (96, 214, 147)
}
def setColors(x_pos, y_pos):
    color = region_colors[world_data[x_pos][y_pos]["region"]]
    if world_data[x_pos][y_pos]["biome"] != None:
        color = biome_colors[world_data[x_pos][y_pos]["biome"]]
    return color

def getScreen(values) :
    colors = []
    for i in range(len(values)) :
        colors.append([])
        for j in range(len(values[i])) :
            color = setColors(i,j)
            colors[i].append(color)
    return colors

def display(colors,size_pixel) :
    for i in range(len(colors)) :
        for j in range(len(colors[i])) :
            color = colors[i][j]
            try :
                pygame.draw.rect(screen, color, pygame.Rect(i*size_pixel,j*size_pixel,size_pixel,size_pixel))
            except :
                print(color)


first_world = getNoise(round(rd.random() * 1000), octave, world_size, step)
second_world = modifyNoise(first_world)
world_map = getScreen(second_world)

run = True
while run:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_ESCAPE]:
        run = False
        
    display(world_map, pixel_size)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
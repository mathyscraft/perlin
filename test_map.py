import pygame
from perlin_noise import PerlinNoise
import random as rd

pygame.init()
pygame.font.init()
# pygame.display.set_icon(pygame.image.load('castle_32x32.png'))
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
# castle_image = pygame.image.load('castle.png').convert_alpha()

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

def modifyNoise(values) :
    for i in range(len(values)):
        for j in range(len(values[i])):
            if values[i][j] > sea_level:
                values[i][j] = 2*(values[i][j]-0.5)**2+0.5
    setForest(values)
    # generateCastles(values)
    return values

forest = []
def setForest(values):
    noise = getNoise(round(rd.random()*1000), 1.5,world_size, 0.04)
    for i in range(len(values)) :
        for j in range(len(values)):
            if values[i][j] > plain_level and values[i][j] < plain_level + plain_interval and noise[i][j] > 0.5:
                forest.append([i,j])

# castles = []
# def generateCastles(values):
#     while len(castles) < rd.randint(min_num_castles, max_num_castles):
#         x_pos= rd.randint(0, int(ScreenWidth / pixel_size)-1)
#         y_pos= rd.randint(0, int(ScreenHeigth / pixel_size)-1)
#         if getBiome(values[x_pos][y_pos], [x_pos, y_pos])=="Plaines":
#             castles.append([x_pos, y_pos])
                
       

def setColors(value, cordonate):
    if cordonate in forest:
        color = ( 31, 176, 44)
    elif value < sea_level:
        color = (0,0,int((255-sea_level*255)+value*255))
    elif value < plain_level :
        color = ( 255, 251, 206)
    elif value < plain_level + plain_interval:
        color = ( 105, 241, 118)
    elif value < glacier_level :
        v = int(-150*value+(plain_level+plain_interval)*255)
        color= (v, v, v)
    else :
        v = int(value**1.5*255)
        color= ( v,v, v)
    return color

def getScreen(values) :
    colors = []
    for i in range(len(values)) :
        colors.append([])
        for j in range(len(values[i])) :
            color = setColors(values[i][j], [i,j])
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
    castles_pos= [[i[0]*pixel_size,i[1]*pixel_size] for i in castles]
    # for pos in castles_pos:
        # screen.blit(castle_image, pos)
                
def getBiome(value, cordonate):
    if cordonate in castles:
        return "Château"
    elif cordonate in forest:
        return "Forêt"
    elif value < sea_level:
        return "Mer"
    elif value < plain_level:
        return "Plage"
    elif value < plain_level + plain_interval:
        return "Plaines"
    elif value < glacier_level:
        return "Montagnes"
    else:
        return "Glacier"

pixel_size = 4
ScreenWidth = 800
ScreenHeigth = 800

#desert, savane, plaine aride, plaine, fôret tempérée, plaine, fôret luxuriante, plaine, toundra

sea_level = 0.5
plain_level = 0.505
plain_interval = 0.1
glacier_level = 0.85
min_num_castles = 5
max_num_castles = 15

octave = 1
step = 0.04


def generateWorld():
    global castles, forest, world_map, world_size, second_world
    castles = []
    forest = []
    world_size = [int(ScreenWidth / pixel_size), int(ScreenHeigth / pixel_size)]
    first_world = getNoise(round(rd.random() * 1000), octave, world_size, step)
    second_world = modifyNoise(first_world)
    world_map = getScreen(second_world)

generateWorld()
reloading = False
run = True
while run:
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    
    
    if keys[pygame.K_ESCAPE]:
        run = False
        
    if keys[pygame.K_SPACE] and not reloading:
        reloading = True
        generateWorld()
        reloading = False
        
    display(world_map, pixel_size)
    
    # Récupérer la position de la souris
    mouse_pos = pygame.mouse.get_pos()
    map_x, map_y = mouse_pos[0] // pixel_size, mouse_pos[1] // pixel_size
    
    if 0 <= map_x < world_size[0] and 0 <= map_y < world_size[1]:
        value = second_world[map_x][map_y]
        biome = getBiome(value, [map_x, map_y])

        # Afficher le biome à l'écran
        pygame.draw.rect(screen, (50,50,50), pygame.Rect(0,10,150,40))
        biome_text = font.render(biome, True, (255, 255, 255))
        screen.blit(biome_text, (10, 20))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
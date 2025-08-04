import pygame as pg
import numpy as np
from math import cos, sin, ceil
from terrain import generate_perlin_noise  # Assuming you have a function for Perlin noise generation

# Initialize parameters
time_interval = 0
time_step = 0.1
shift_x,shift_y = 0,0
# Generate terrain
liste = generate_perlin_noise(200, 200, scale=100.0, octaves=8, persistence=0.5, lacunarity=2.0, seed=8)
maximum = np.max(liste)

# Initialize Pygame
pg.init()
fenetre_size = 800
fenetre = pg.display.set_mode((fenetre_size, fenetre_size))
clock = pg.time.Clock()

# Rotation and visualization variables
distance = 4
angle_x = -0.7
angle_y = 0.65
angle_z = 0

color = [(51, 51, 153), (44, 64, 166), (37, 77, 179), (31, 91, 193), (24, 104, 206), (17, 117, 219), (11, 131, 233),
         (4, 144, 246), (0, 156, 244), (0, 168, 208), (0, 178, 178), (0, 188, 148), (0, 198, 118), (8, 205, 103),
         (29, 209, 107), (49, 213, 111), (69, 217, 115), (93, 222, 120), (113, 226, 124), (133, 230, 128), (153, 234, 132),
         (173, 238, 136), (193, 242, 140), (213, 246, 144), (232, 250, 148), (254, 253, 152), (244, 240, 147),
         (234, 228, 141), (224, 215, 136), (214, 202, 130), (204, 189, 125), (194, 176, 120), (184, 164, 114),
         (174, 151, 109), (162, 135, 102), (152, 123, 97), (142, 110, 91), (131, 97, 86), (133, 98, 91), (143, 111, 104),
         (153, 124, 118), (163, 137, 131), (175, 152, 147), (185, 165, 161), (195, 178, 174), (205, 191, 187),
         (215, 203, 201), (225, 216, 214), (235, 229, 228), (244, 242, 241), (255, 255, 255), (255, 255, 255),
         (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
         (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
         (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]

def rotate_and_project(point, rotation_matrices, scale, window_size):
    point = np.dot(rotation_matrices, point)
    projection_matrix = np.array([[scale, 0, 0], [0, scale, 0], [0, 0, 0]])
    point_2d = np.dot(projection_matrix, point)
    x = (point_2d[0]) + window_size / 2
    y = -(point_2d[1]) + window_size / 2
    return x, y, point[2]

# Precompute rotated and projected points
point_cache = []

# Main loop
running = True
while running:
    clock.tick(30)
    fenetre.fill((0, 0, 0))
    scale = 1 / distance
    #LOD_ratio = ceil(1.4 * distance)
    LOD_ratio = 2

    # Rotation matrices
    cos_x, sin_x = cos(angle_x), sin(angle_x)
    cos_y, sin_y = cos(angle_y), sin(angle_y)
    cos_z, sin_z = cos(angle_z), sin(angle_z)
    
    rotation_x = np.array([[1, 0, 0], [0, cos_x, -sin_x], [0, sin_x, cos_x]])
    rotation_y = np.array([[cos_y, 0, sin_y], [0, 1, 0], [-sin_y, 0, cos_y]])
    rotation_z = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]])
    rotation_matrices = rotation_x @ rotation_y @ rotation_z

    point_cache.clear()

    # Handle keyboard input
    key_input = pg.key.get_pressed()
    angle_y += 0.05 if key_input[pg.K_LEFT] else -0.05 if key_input[pg.K_RIGHT] else 0
    angle_x += 0.05 if key_input[pg.K_UP] else -0.05 if key_input[pg.K_DOWN] else 0
    angle_z += 0.05 if key_input[pg.K_q] else -0.05 if key_input[pg.K_d] else 0
    if key_input[pg.K_f]:
        angle_x = angle_y = angle_z = 0
    mouse_buttons = pg.mouse.get_pressed()
    if mouse_buttons[0]:  # Left mouse button is pressed
        dx, dy = pg.mouse.get_rel()
        shift_x += dx
        shift_y += dy
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEWHEEL:
            distance = max(0.1, distance + 0.1 * event.y)

    # Determine order of iteration based on angle_y
    iterate_order = range(len(liste)) if cos(angle_y) > 0 else reversed(range(len(liste)))

    # Precompute points and colors
    for i in iterate_order:
        for j in range(0, len(liste[i]), LOD_ratio):
            coor = np.array([j * 15, -5 + liste[i][j] * 15, -i * 15])
            x, y, z = rotate_and_project(coor, rotation_matrices, scale, fenetre_size)
            x += shift_x
            y += shift_y
            point_cache.append((x, y, z, liste[i][j]))

    # Create and draw polygons
    polygons = []
    len_liste = len(liste)
    len_liste0 = ceil(len(liste[0]) / LOD_ratio)

    for i in range(len_liste - 1):
        for j in range(len_liste0 - 1):
            n = i * len_liste0 + j
            if cos(angle_y) > 0:
                points = [point_cache[n][0:2], point_cache[n + len_liste0][0:2],
                          point_cache[n + 1 + len_liste0][0:2], point_cache[n + 1][0:2]]
                depths = [point_cache[n][2], point_cache[n + len_liste0][2],
                          point_cache[n + 1 + len_liste0][2], point_cache[n + 1][2]]
            else:
                points = [point_cache[-n - 1][0:2], point_cache[-n - 1 - len_liste0][0:2],
                          point_cache[-n - 2 - len_liste0][0:2], point_cache[-n - 2][0:2]]
                depths = [point_cache[-n - 1][2], point_cache[-n - 1 - len_liste0][2],
                          point_cache[-n - 2 - len_liste0][2], point_cache[-n - 2][2]]
            
            # Check if at least one point is within the screen bounds
            if any(0 <= x <= fenetre_size and 0 <= y <= fenetre_size for x, y in points):
                height_max = max(abs(point_cache[n][3]), abs(point_cache[n + len_liste0][3]),
                                 abs(point_cache[n + 1 + len_liste0][3]), abs(point_cache[n + 1][3]))
                coloration = color[ceil(height_max)]
                avg_depth = sum(depths) / 4
                polygons.append((avg_depth, points, coloration))

    # Sort polygons by depth
    polygons.sort(key=lambda p: p[0], reverse=True)

    # Draw polygons
    for _, points, coloration in polygons:
        pg.draw.polygon(fenetre, coloration, points)
    pg.display.update()

pg.quit()

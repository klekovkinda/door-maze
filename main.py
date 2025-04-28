import pygame
import yaml

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

with open("config/map.yaml", "r") as file:
    map_config = yaml.safe_load(file)

TILE_SIZE = 100
assets = {"flor": pygame.image.load("assets/flor.png"),
          "wall": pygame.image.load("assets/wall.png"), }


def draw_map():
    for row_index, row in enumerate(map_config["rows"]):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            screen.blit(assets[tile], (x, y))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

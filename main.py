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

hero = {"x": 0, "y": 0}
hero_image = pygame.image.load("assets/hero.png")


def draw_map():
    for row_index, row in enumerate(map_config["rows"]):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            tile_type = tile["type"]
            rotation = tile["rotation"]
            rotated_tile = pygame.transform.rotate(assets[tile_type], rotation)
            screen.blit(rotated_tile, (x, y))
    # Draw the hero
    hero_x = hero["x"] * TILE_SIZE
    hero_y = hero["y"] * TILE_SIZE
    screen.blit(hero_image, (hero_x, hero_y))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                hero["y"] -= 1  #
            elif event.key == pygame.K_DOWN:
                hero["y"] += 1
            elif event.key == pygame.K_LEFT:
                hero["x"] -= 1
            elif event.key == pygame.K_RIGHT:
                hero["x"] += 1

    screen.fill((0, 0, 0))
    draw_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import yaml

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

with open("config/map.yaml", "r") as file:
    map_config = yaml.safe_load(file)

TILE_SIZE = 100
assets = {"flor": pygame.image.load("assets/flor.png"), "wall": pygame.image.load("assets/wall.png"), }

hero = {"x": 0, "y": 0, "target_x": 0, "target_y": 0, "moving": False, "rotation": 0}
hero_image = pygame.image.load("assets/hero.png")
HERO_SPEED = 10

pressed_keys = {"up": False, "down": False, "left": False, "right": False}


def draw_map():
    for row_index, row in enumerate(map_config["rows"]):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            tile_type = tile["type"]
            rotation = tile["rotation"]
            rotated_tile = pygame.transform.rotate(assets[tile_type], rotation)
            screen.blit(rotated_tile, (x, y))
    hero_x = hero["x"] * TILE_SIZE
    hero_y = hero["y"] * TILE_SIZE
    rotated_hero = pygame.transform.rotate(hero_image, hero["rotation"])
    screen.blit(rotated_hero, (hero_x, hero_y))


def update_hero_position():
    if hero["moving"]:
        current_x = hero["x"] * TILE_SIZE
        current_y = hero["y"] * TILE_SIZE
        target_x = hero["target_x"] * TILE_SIZE
        target_y = hero["target_y"] * TILE_SIZE

        dx = target_x - current_x
        dy = target_y - current_y

        if abs(dx) > HERO_SPEED:
            hero["x"] += HERO_SPEED / TILE_SIZE if dx > 0 else -HERO_SPEED / TILE_SIZE
        else:
            hero["x"] = hero["target_x"]

        if abs(dy) > HERO_SPEED:
            hero["y"] += HERO_SPEED / TILE_SIZE if dy > 0 else -HERO_SPEED / TILE_SIZE
        else:
            hero["y"] = hero["target_y"]

        if hero["x"] == hero["target_x"] and hero["y"] == hero["target_y"]:
            hero["moving"] = False


def handle_keydown(event):
    if event.key == pygame.K_UP:
        pressed_keys["up"] = True
        hero["rotation"] = 180
    elif event.key == pygame.K_DOWN:
        pressed_keys["down"] = True
        hero["rotation"] = 0
    elif event.key == pygame.K_LEFT:
        pressed_keys["left"] = True
        hero["rotation"] = -90
    elif event.key == pygame.K_RIGHT:
        pressed_keys["right"] = True
        hero["rotation"] = 90


def handle_keyup(event):
    if event.key == pygame.K_UP:
        pressed_keys["up"] = False
    elif event.key == pygame.K_DOWN:
        pressed_keys["down"] = False
    elif event.key == pygame.K_LEFT:
        pressed_keys["left"] = False
    elif event.key == pygame.K_RIGHT:
        pressed_keys["right"] = False


def update_hero_target():
    if not hero["moving"]:
        if pressed_keys["up"]:
            hero["target_y"] -= 1
        elif pressed_keys["down"]:
            hero["target_y"] += 1
        elif pressed_keys["left"]:
            hero["target_x"] -= 1
        elif pressed_keys["right"]:
            hero["target_x"] += 1

        if hero["target_x"] != hero["x"] or hero["target_y"] != hero["y"]:
            hero["moving"] = True


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)
        elif event.type == pygame.KEYUP:
            handle_keyup(event)

    update_hero_target()
    update_hero_position()
    screen.fill((0, 0, 0))
    draw_map()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

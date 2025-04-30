import pygame
import yaml

pygame.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()

with open("config/map.yaml", "r") as file:
    map_config = yaml.safe_load(file)

TILE_SIZE = 100
assets = {"flor": pygame.image.load("assets/flor.png"), "wall": pygame.image.load("assets/wall.png"), }

hero_sprite_sheet = pygame.image.load("assets/hero-go.png").convert_alpha()
HERO_FRAMES = []
FRAME_COUNT = 10 #TODO seems 11 frames even better
FRAME_WIDTH = hero_sprite_sheet.get_width() // FRAME_COUNT
FRAME_HEIGHT = hero_sprite_sheet.get_height()

for i in range(FRAME_COUNT):
    frame = hero_sprite_sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT))
    HERO_FRAMES.append(frame)

hero = {"x": 0, "y": 0, "target_x": 0, "target_y": 0, "moving": False, "rotation": 0, "target_rotation": 0,
        "frame_index": 0, }

HERO_SPEED = 10
HERO_ROTATION_SPEED = 10  # Degrees per frame for smooth rotation

pressed_keys = {"up": False, "down": False, "left": False, "right": False}
current_direction = None
key_queue = []


def draw_map():
    for row_index, row in enumerate(map_config["rows"]):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            tile_type = tile["type"]
            rotation = tile["rotation"]
            rotated_tile = pygame.transform.rotate(assets[tile_type], rotation)
            screen.blit(rotated_tile, (x, y))

    hero_center_x = hero["x"] * TILE_SIZE + TILE_SIZE // 2
    hero_center_y = hero["y"] * TILE_SIZE + TILE_SIZE // 2

    frame = HERO_FRAMES[hero["frame_index"]]
    rotated_hero = pygame.transform.rotate(frame, hero["rotation"])
    hero_rect = rotated_hero.get_rect(center=(hero_center_x, hero_center_y))
    screen.blit(rotated_hero, hero_rect.topleft)


def update_hero_position_and_rotation():
    if hero["moving"]:
        # Smooth rotation
        target_rotation = hero["target_rotation"]
        current_rotation = hero["rotation"]
        rotation_diff = (target_rotation - current_rotation) % 360
        if rotation_diff > 180:
            rotation_diff -= 360
        if abs(rotation_diff) > HERO_ROTATION_SPEED:
            hero["rotation"] += HERO_ROTATION_SPEED if rotation_diff > 0 else -HERO_ROTATION_SPEED
            hero["rotation"] %= 360
        else:
            hero["rotation"] = target_rotation

        # Only move after completing the rotation
        if hero["rotation"] == target_rotation:
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

            frame_index = HERO_SPEED - int(abs(dx / HERO_SPEED) + abs(dy / HERO_SPEED))

            hero["frame_index"] = 0 if frame_index>=FRAME_COUNT else frame_index
            print(hero["frame_index"])


def handle_keydown(event):
    global current_direction
    direction_map = {pygame.K_UP: "up", pygame.K_DOWN: "down", pygame.K_LEFT: "left", pygame.K_RIGHT: "right", }
    rotation_map = {"up": 180, "down": 0, "left": -90, "right": 90, }

    if event.key in direction_map:
        direction = direction_map[event.key]
        if direction not in key_queue:  # Avoid duplicate entries in the queue
            key_queue.append(direction)

        if current_direction is None:  # Start moving if no direction is active
            current_direction = direction
            hero["target_rotation"] = rotation_map[direction]  # Set target rotation
            pressed_keys[direction] = True


def handle_keyup(event):
    global current_direction
    direction_map = {pygame.K_UP: "up", pygame.K_DOWN: "down", pygame.K_LEFT: "left", pygame.K_RIGHT: "right", }

    if event.key in direction_map:
        direction = direction_map[event.key]
        if direction in key_queue:
            key_queue.remove(direction)  # Remove the released key from the queue

        if current_direction == direction:  # If the released key was the active direction
            pressed_keys[direction] = False
            current_direction = None

            # Check the next key in the queue
            if key_queue:
                next_direction = key_queue[-1]  # Get the most recently pressed key
                current_direction = next_direction
                hero["target_rotation"] = {"up": 180, "down": 0, "left": -90, "right": 90, }[next_direction]
                pressed_keys[next_direction] = True


def update_hero_target():
    if not hero["moving"] and current_direction:
        if current_direction == "up":
            hero["target_y"] -= 1
        elif current_direction == "down":
            hero["target_y"] += 1
        elif current_direction == "left":
            hero["target_x"] -= 1
        elif current_direction == "right":
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
    update_hero_position_and_rotation()
    screen.fill((0, 0, 0))
    draw_map()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()

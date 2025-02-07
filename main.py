import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
GRID_SIZE = 10
CELL_SIZE = 60
MAP_HEIGHT = GRID_SIZE * CELL_SIZE
UI_HEIGHT = 80
SCREEN_WIDTH, SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE, MAP_HEIGHT + UI_HEIGHT
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 100, 200)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Push to Success")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load assets
star_image = pygame.transform.scale(pygame.image.load("assets/Star.png"), (CELL_SIZE, CELL_SIZE))
wall_block = pygame.transform.scale(pygame.image.load("assets/Wall_Block_Tall.png"), (CELL_SIZE, CELL_SIZE))
box_image = pygame.transform.scale(pygame.image.load("assets/Box.png"), (CELL_SIZE, CELL_SIZE))

# Function to generate random target position
def generate_target_position():
    while True:
        tx, ty = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (tx, ty) != (5, 5):
            return tx, ty


def generate_obstacles():
    obstacles = set()
    while len(obstacles) < 15:
        ox, oy = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (ox, oy) not in start_positions and (ox, oy) != finish_position:
            obstacles.add((ox, oy))
    return obstacles


def generate_star():
    valid_positions = set((x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE))
    invalid_positions = obstacles | {finish_position, box_position}
    possible_positions = list(valid_positions - invalid_positions)

    if not possible_positions:
        return set()  # No valid position available

    sx, sy = random.choice(possible_positions)
    return {(sx, sy)}

def generate_box_position():
    while True:
        bx, by = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)
        if (bx, by) not in obstacles and (bx, by) != finish_position:
            return bx, by

#
# def reset_game():
#     global excavator, finish_position, obstacles, box_position, level
#     finish_position = generate_target_position()
#     start_positions = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
#     start_position = random.choice(start_positions)
#     obstacles = generate_obstacles()
#     box_position = generate_box_position()  # Ensuring box is placed correctly
#     level = 1
#     excavator = MainCharacter(*start_position)


def reset_game():
    global excavator, finish_position, obstacles, box_position, level, stars_collected, stars
    finish_position = generate_target_position()
    obstacles = generate_obstacles()
    box_position = (random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2))
    stars_collected = 0
    level = 1
    excavator = MainCharacter(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    stars = generate_star()
# Game variables
finish_position = generate_target_position()
start_positions = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
start_position = random.choice(start_positions)
obstacles = generate_obstacles()
box_position = generate_box_position()
stars = generate_star()
level = 1
stars_collected = 0


def start_screen():
    while True:
        screen.fill(BLACK)
        text = font.render("Press ENTER to Start", True, WHITE)
        screen.blit(text, ((SCREEN_WIDTH - text.get_width()) // 2, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return


class MainCharacter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "down"

        # Load images
        self.images = {
            "left": pygame.transform.scale(pygame.image.load("assets/excavator_left.png"), (CELL_SIZE, CELL_SIZE)),
            "right": pygame.transform.scale(pygame.image.load("assets/excavator_right.png"), (CELL_SIZE, CELL_SIZE)),
            "up": pygame.transform.scale(pygame.image.load("assets/excavator_up.png"), (CELL_SIZE, CELL_SIZE)),
            "down": pygame.transform.scale(pygame.image.load("assets/excavator_down.png"), (CELL_SIZE, CELL_SIZE)),
        }

    def draw(self):
        screen.blit(self.images[self.direction], (self.x * CELL_SIZE, self.y * CELL_SIZE))

    def move(self, dx, dy, new_direction):
        global box_position, level, finish_position, obstacles, stars_collected, stars
        self.direction = new_direction

        new_x = self.x + dx
        new_y = self.y + dy

        # Check if moving into obstacles
        if (0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in obstacles):
            # Check if pushing the box
            if (new_x, new_y) == box_position:
                box_new_x, box_new_y = box_position[0] + dx, box_position[1] + dy
                if (0 <= box_new_x < GRID_SIZE and 0 <= box_new_y < GRID_SIZE and
                        (box_new_x, box_new_y) not in obstacles):
                    box_position = (box_new_x, box_new_y)
                    self.x = new_x
                    self.y = new_y
            else:
                self.x = new_x
                self.y = new_y
        # Check if reached a star
        if (self.x, self.y) in stars:
            stars_collected += 1
            stars.remove((self.x, self.y))

        # Check if the box is at the finish position
        if box_position == finish_position:
            level += 1
            stars = generate_star()
            reset_game()

# Create the main character
excavator = MainCharacter(*start_position)

# Draw button
def draw_button(text, x, y, w, h, color, action=None):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + (w - label.get_width()) // 2, y + (h - label.get_height()) // 2))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_x, mouse_y):
        if pygame.mouse.get_pressed()[0]:
            if action:
                action()

# Game loop
def main():
    start_screen()
    global excavator
    while True:
        screen.fill(GRAY)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    excavator.move(0, -1, "up")
                if event.key == pygame.K_DOWN:
                    excavator.move(0, 1, "down")
                if event.key == pygame.K_LEFT:
                    excavator.move(-1, 0, "left")
                if event.key == pygame.K_RIGHT:
                    excavator.move(1, 0, "right")

        # Draw grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Draw obstacles
        for ox, oy in obstacles:
            screen.blit(wall_block, (ox * CELL_SIZE, oy * CELL_SIZE))

        # Draw stars
        for sx, sy in stars:
            screen.blit(star_image, (sx * CELL_SIZE, sy * CELL_SIZE))

        # Draw box
        screen.blit(box_image, (box_position[0] * CELL_SIZE, box_position[1] * CELL_SIZE))

        # Draw finish position
        pygame.draw.rect(screen, GREEN, (finish_position[0] * CELL_SIZE, finish_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw the excavator
        excavator.draw()

        # Draw UI
        pygame.draw.rect(screen, BLACK, (0, MAP_HEIGHT, SCREEN_WIDTH, UI_HEIGHT))  # UI Background

        # Display level (Bottom Left)
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (10, MAP_HEIGHT + 20))

        # Display stars collected (Bottom Right)
        stars_text = font.render(f"Stars: {stars_collected}", True, YELLOW)
        screen.blit(stars_text, (SCREEN_WIDTH - stars_text.get_width() - 10, MAP_HEIGHT + 20))

        # Draw Reset Button (Center)
        draw_button("Reset", SCREEN_WIDTH // 2 - 50, MAP_HEIGHT + 20, 100, 40, BLUE, reset_game)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()


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
button_color = (200, 50, 50)
button_hover_color = (255, 0, 0)
# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Push to Success")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
fontTwo = pygame.font.Font(None, 50)
fontSmall = pygame.font.Font(None, 23)

# Load assets
star_image = pygame.transform.scale(pygame.image.load("assets/Star.png"), (CELL_SIZE, CELL_SIZE))
wall_block = pygame.transform.scale(pygame.image.load("assets/Wall_Block_Tall.png"), (CELL_SIZE, CELL_SIZE))
box_image = pygame.transform.scale(pygame.image.load("assets/Box.png"), (CELL_SIZE, CELL_SIZE))

TIMER_DURATION  = 30  # Start from 60 seconds (1 minute)
start_ticks = None

# Load Music 🎵
pygame.mixer.init()
pygame.mixer.music.load("assets/start_screen_music.mp3")  # Replace with your music file
pygame.mixer.music.play(-1)  # Loop the music indefinitely


car_move_sound = pygame.mixer.Sound("assets/car_move.mp3")  # Car movement sound
collect_star_sound = pygame.mixer.Sound("assets/star_collect.mp3")  # Star collection
turbo_mode = pygame.mixer.Sound("assets/turbo_mode.mp3")  # Star collection
end_game_mode = pygame.mixer.Sound('assets/end_game.mp3')  # Star collection

def generate_end_game_position():
    while True:
        tx, ty = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (tx, ty) != (5, 5):
            return tx, ty


end_game_position = generate_end_game_position()

def generate_target_position():
    while True:
        tx, ty = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (tx, ty) != (5, 5) and (tx, ty) != end_game_position:
            return tx, ty


def generate_obstacles():
    obstacles = set()
    while len(obstacles) < 15:
        ox, oy = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if (ox, oy) not in start_positions and (ox, oy) != finish_position and (ox, oy) != end_game_position:
            obstacles.add((ox, oy))
    return obstacles


def generate_star():
    valid_positions = set((x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE))
    invalid_positions = obstacles | {finish_position, box_position, end_game_position}
    possible_positions = list(valid_positions - invalid_positions)

    if not possible_positions:
        return set()  # No valid position available

    sx, sy = random.choice(possible_positions)
    return {(sx, sy)}


def generate_box_position():
    while True:
        bx, by = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)
        if (bx, by) not in obstacles and (bx, by) != finish_position and (bx, by) != end_game_position:
            adjacent_positions = {
                (bx + 1, by), (bx - 1, by), (bx, by + 1), (bx, by - 1),
                (bx + 1, by + 1), (bx - 1, by - 1), (bx + 1, by - 1), (bx - 1, by + 1)
            }
            if not adjacent_positions & obstacles:
                return bx, by


def start_new_level():
    global excavator, finish_position, obstacles, box_position, level, stars_collected, stars,end_game_position
    finish_position = generate_target_position()
    end_game_position = generate_end_game_position()
    obstacles = generate_obstacles()
    box_position = generate_box_position()
    excavator = MainCharacter(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    stars = generate_star()


def reset_game():
    global excavator, finish_position, obstacles, box_position, level, stars_collected, stars,end_game_position
    finish_position = generate_target_position()
    end_game_position = generate_end_game_position()
    obstacles = generate_obstacles()
    box_position = generate_box_position()
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

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Push to Success")

# Load background image
background_image = pygame.image.load("assets/bg.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


button_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50)

def draw_start_again_button():
    """ Draw restart button """
    pygame.draw.rect(screen, GREEN, button_rect)
    text = font.render("Start Again", True, WHITE)
    screen.blit(text, (button_rect.x + 25, button_rect.y + 10))

def game_over_screen():
    # Load Music 🎵
    pygame.mixer.init()
    pygame.mixer.music.load("assets/end_game.mp3")  # Replace with your music file
    pygame.mixer.music.play(-1)  # Loop the music indefinitely

    """ Displays a game over animation and restart button """
    alpha = 0  # For fading effect
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)

    running = True
    while running:
        screen.fill(WHITE)

        # Animation: Fade-in effect
        if alpha < 255:
            alpha += 5  # Increase transparency
        fade_surface.set_alpha(alpha)  # Apply transparency
        screen.blit(fade_surface, (0, 0))  # Draw fade effect

        # Display Game Over text
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))

        # Draw restart button
        draw_start_again_button()

        pygame.display.flip()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Exit loop

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()  # Stop game over music before restarting
                    return start_new_level()  # Restart game

    return False

def start_screen():
    running = True
    while running:
        screen.blit(background_image, (0, 0))  # Draw background

        # Draw title
        draw_text("Welcome to the Game!", fontTwo, WHITE, SCREEN_WIDTH // 5, SCREEN_HEIGHT // 30)

        # Draw button
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        mouse_pos = pygame.mouse.get_pos()

        # Change button color on hover
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        current_button_color = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color

        pygame.draw.rect(screen, current_button_color, button_rect, border_radius=9)

        # Draw button text
        draw_text("Start Game", fontTwo, WHITE, SCREEN_WIDTH // 2 - 95, SCREEN_HEIGHT // 2 + 10)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False  # Exit the start screen and go to game
                    pygame.mixer.music.stop()

        pygame.display.flip()


start_mode = False
timer_of_mode = False


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
        global box_position, level, finish_position, obstacles, stars_collected, stars, timer_of_mode, end_game_position
        self.direction = new_direction

        new_x = self.x + dx
        new_y = self.y + dy

        if start_mode:
            # Check if pushing the box
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y):
                if (new_x, new_y) == box_position:
                    box_new_x, box_new_y = box_position[0] + dx, box_position[1] + dy
                    if (0 <= box_new_x < GRID_SIZE and 0 <= box_new_y < GRID_SIZE and
                            (box_new_x, box_new_y) not in obstacles):
                        box_position = (box_new_x, box_new_y)
                        self.x = new_x
                        self.y = new_y
                    else:
                        # Edge case: Swap positions instead of pushing
                        self.x, self.y, box_position = box_position[0], box_position[1], (self.x, self.y)
                else:
                    self.x = new_x
                    self.y = new_y

        # Check if moving into obstacles
        elif 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE and (new_x, new_y) not in obstacles:
            # Check if pushing the box
            if (new_x, new_y) == box_position:
                box_new_x, box_new_y = box_position[0] + dx, box_position[1] + dy
                if (0 <= box_new_x < GRID_SIZE and 0 <= box_new_y < GRID_SIZE and
                        (box_new_x, box_new_y) not in obstacles):
                    box_position = (box_new_x, box_new_y)
                    self.x = new_x
                    self.y = new_y
                else:
                    # Edge case: Swap positions instead of pushing
                    self.x, self.y, box_position = box_position[0], box_position[1], (self.x, self.y)
            else:
                self.x = new_x
                self.y = new_y
        # Check if reached a star
        if (self.x, self.y) in stars:
            collect_star_sound.play()
            stars_collected += 1
            stars.remove((self.x, self.y))

        # Check if the box is at the finish position
        if box_position == finish_position:
            level += 1
            stars = generate_star()
            start_new_level()

        # Check if the box is at the end position
        if box_position == end_game_position:
            level = 1
            stars_collected = 0
            game_over_screen()


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
    global excavator, start_mode, stars_collected, start_ticks
    while True:
        screen.fill(GRAY)


            # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    if stars_collected >= 5:
                        start_mode = True
                        turbo_mode.play()
                        start_ticks = pygame.time.get_ticks()
                        stars_collected = stars_collected - 5
                if event.key == pygame.K_UP:
                    car_move_sound.play()
                    excavator.move(0, -1, "up")
                if event.key == pygame.K_DOWN:
                    car_move_sound.play()
                    excavator.move(0, 1, "down")
                if event.key == pygame.K_LEFT:
                    car_move_sound.play()
                    excavator.move(-1, 0, "left")
                if event.key == pygame.K_RIGHT:
                    car_move_sound.play()
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
        pygame.draw.rect(screen, GREEN,
                         (finish_position[0] * CELL_SIZE, finish_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # Draw end game position
        pygame.draw.rect(screen, RED,
                         (end_game_position[0] * CELL_SIZE, end_game_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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

        # Display Active turbo mode
        if stars_collected >= 5:
            stars_text = fontSmall.render("Active turbo mode by pressing T", True, RED)
            screen.blit(stars_text, (SCREEN_WIDTH - stars_text.get_width() - 10, MAP_HEIGHT + 50))

        # Draw Reset Button (Center)
        draw_button("Reset", SCREEN_WIDTH // 2 - 50, MAP_HEIGHT + 20, 100, 40, BLUE, reset_game)

        if start_mode:
            elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
            remaining_time = max(0, TIMER_DURATION - elapsed_seconds)

            minutes = remaining_time // 60
            seconds = remaining_time % 60
            timer_text = f"{minutes}:{seconds:02d} s"

            text_surface = font.render(timer_text, True, RED)
            screen.blit(text_surface, (SCREEN_WIDTH / 2.2, SCREEN_HEIGHT / 2.3))

            if remaining_time == 0:
                start_mode = False

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

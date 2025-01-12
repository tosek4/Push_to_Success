import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Excavator Movement")
clock = pygame.time.Clock()

# Main character class
class MainCharacter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = "down"  # Default direction

        # Load images
        self.images = {
            "left": pygame.transform.scale(pygame.image.load("assets/excavator_left.png"), (CELL_SIZE, CELL_SIZE)),
            "right": pygame.transform.scale(pygame.image.load("assets/excavator_right.png"), (CELL_SIZE, CELL_SIZE)),
            "up": pygame.transform.scale(pygame.image.load("assets/excavator_up.png"), (CELL_SIZE, CELL_SIZE)),
            "down": pygame.transform.scale(pygame.image.load("assets/excavator_down.png"), (CELL_SIZE, CELL_SIZE)),
        }

    def draw(self):
        # Draw the excavator using the current direction's image
        screen.blit(self.images[self.direction], (self.x * CELL_SIZE, self.y * CELL_SIZE))

    def move(self, dx, dy, new_direction):
        # Update the direction
        self.direction = new_direction

        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Prevent moving outside the grid
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            self.x = new_x
            self.y = new_y

# Create the main character
excavator = MainCharacter(5, 5)

# Game loop
def main():
    global excavator
    while True:
        screen.fill(GRAY)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    excavator.move(0, -1, "up")  # Move up
                if event.key == pygame.K_DOWN:
                    excavator.move(0, 1, "down")  # Move down
                if event.key == pygame.K_LEFT:
                    excavator.move(-1, 0, "left")  # Move left
                if event.key == pygame.K_RIGHT:
                    excavator.move(1, 0, "right")  # Move right

        # Draw the grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # Draw the excavator
        excavator.draw()

        # Refresh the display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

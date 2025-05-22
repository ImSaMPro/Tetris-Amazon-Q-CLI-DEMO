import pygame
import sys
import random
import os

# Initialize Pygame and set up display
pygame.init()
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
GRID_WIDTH = WIDTH // BLOCK_SIZE
GRID_HEIGHT = HEIGHT // BLOCK_SIZE
FPS = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

class Snake:
    """Represents the snake in the game"""
    
    def __init__(self):
        # Initial position: center of grid
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (0, -1)  # Start moving up
        
    def move(self, food_position):
        """Update snake's position based on direction"""
        head_x, head_y = self.body[0]
        
        # Calculate new head position
        new_head = (
            head_x + self.direction[0],
            head_y + self.direction[1]
        )
        
        # Check for collision with food
        if new_head == food_position:
            self.body.insert(0, new_head)
            return True  # Food eaten
        
        # Move snake normally
        self.body.insert(0, new_head)
        self.body.pop()  # Remove tail segment
        
        return False
    
    def draw(self):
        """Draw the snake on the screen"""
        for segment in self.body:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            )

class Food:
    """Represents the food in the game"""
    
    def __init__(self):
        # Generate random position not on the snake
        self.position = self.random_position()
        
    def random_position(self):
        """Find a valid position for the food"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # Ensure food isn't on the snake
            if (x, y) not in snake.body:
                return (x, y)
                
    def draw(self):
        """Draw the food on the screen"""
        pygame.draw.rect(
            screen,
            RED,
            (self.position[0] * BLOCK_SIZE, self.position[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        )

class Game:
    """Main game logic and management"""
    
    def __init__(self):
        # Initialize game elements
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        
        # Game states: start, playing, game_over
        self.state = "start"
        
        # Sound effects (optional)
        self.eat_sound = pygame.mixer.Sound("eat.wav")
        self.game_over_sound = pygame.mixer.Sound("gameover.wav")
        
    def handle_events(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
                
            if self.state == "start":
                # Start game on any key press
                if event.type == pygame.KEYDOWN:
                    self.state = "playing"
                    
            elif self.state == "game_over":
                # Restart or quit on space/escape
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        
    def update(self):
        """Update game state"""
        if self.state == "playing":
            # Move snake and check for food
            if self.snake.move(self.food.position):
                self.score += 1
                self.eat_sound.play()
                self.food = Food()
                
            # Check for collisions
            head = self.snake.body[0]
            if (
                head[0] < 0 or head[0] >= GRID_WIDTH or
                head[1] < 0 or head[1] >= GRID_HEIGHT or
                head in self.snake.body[1:]
            ):
                self.state = "game_over"
                self.game_over_sound.play()
                
    def draw(self):
        """Draw all game elements"""
        screen.fill(BLACK)
        
        # Draw snake and food
        self.snake.draw()
        self.food.draw()
        
        # Display score
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(text, (10, 10))
        
        # Draw start screen instructions
        if self.state == "start":
            font = pygame.font.SysFont(None, 48)
            text = font.render("Press any key to start", True, BLUE)
            screen.blit(text, (WIDTH//2 - 200, HEIGHT//2 - 50))
            
            # Display controls
            font = pygame.font.SysFont(None, 24)
            text = font.render("Use arrow keys or WASD to move", True, WHITE)
            screen.blit(text, (10, 50))
            
        # Draw game over screen
        elif self.state == "game_over":
            font = pygame.font.SysFont(None, 64)
            text = font.render("Game Over", True, RED)
            screen.blit(text, (WIDTH//2 - 180, HEIGHT//2 - 100))
            
            font = pygame.font.SysFont(None, 36)
            text = font.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 + 20))
            
            text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(text, (WIDTH//2 - 180, HEIGHT//2 + 70))
            
            text = font.render("Press ESC to quit", True, WHITE)
            screen.blit(text, (WIDTH//2 - 160, HEIGHT//2 + 110))
    
    def reset(self):
        """Reset game state for new game"""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.state = "playing"

def main():
    game = Game()
    running = True
    
    while running:
        clock.tick(FPS)
        
        game.handle_events()
        game.update()
        game.draw()
        
        pygame.display.flip()
        
        # Quit on escape key
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

if __name__ == "__main__":
    main()
    pygame.quit()

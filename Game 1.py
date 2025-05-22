import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
BLOCK_SIZE = 20
BOARD_WIDTH = 10  # Standard Tetris board width
BOARD_HEIGHT = 20
BOARD_X = (SCREEN_WIDTH - BOARD_WIDTH * BLOCK_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_HEIGHT * BLOCK_SIZE) // 2
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes
SHAPES = {
    'I': {
        'shape': [[1, 1, 1, 1]],
        'color': CYAN
    },
    'O': {
        'shape': [[1, 1], [1, 1]],
        'color': YELLOW
    },
    'T': {
        'shape': [[0, 1, 0], [1, 1, 1]],
        'color': MAGENTA
    },
    'L': {
        'shape': [[1, 0], [1, 0], [1, 1]],
        'color': ORANGE
    },
    'J': {
        'shape': [[0, 1], [0, 1], [1, 1]],
        'color': BLUE
    },
    'S': {
        'shape': [[0, 1, 1], [1, 1, 0]],
        'color': GREEN
    },
    'Z': {
        'shape': [[1, 1, 0], [0, 1, 1]],
        'color': RED
    }
}

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)

        self.reset_game()

    def reset_game(self):
        # Initialize game board (0 = empty, other values = filled with a color)
        self.board = [[0 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]

        # Score tracking
        self.current_score = 0
        self.last_game_score = 0
        self.high_score = 0

        # Current falling piece
        self.current_piece = self.new_piece()
        self.game_over = False

        # Game speed (moves down every N frames)
        self.fall_speed = 10
        self.fall_counter = 0

    def new_piece(self):
        # Randomly select a tetromino
        shape_name = random.choice(list(SHAPES.keys()))
        shape_data = SHAPES[shape_name]

        # Create a new piece dictionary
        piece = {
            'shape': shape_data['shape'],
            'color': shape_data['color'],
            'x': BOARD_WIDTH // 2 - len(shape_data['shape'][0]) // 2,
            'y': 0
        }

        # Check if the new piece can be placed (game over condition)
        if not self.is_valid_position(piece):
            self.game_over = True
            if self.current_score > self.high_score:
                self.high_score = self.current_score
            self.last_game_score = self.current_score

        return piece

    def rotate_piece(self, piece):
        # Create a rotated version of the piece (90 degrees clockwise)
        shape = piece['shape']
        rotated = [[shape[y][x] for y in range(len(shape)-1, -1, -1)] for x in range(len(shape[0]))]

        # Create a new piece with the rotated shape
        new_piece = piece.copy()
        new_piece['shape'] = rotated

        # Adjust position if needed to keep within bounds
        if not self.is_valid_position(new_piece):
            # Try adjusting x position if rotation puts piece out of bounds
            if new_piece['x'] + len(rotated[0]) > BOARD_WIDTH:
                new_piece['x'] = BOARD_WIDTH - len(rotated[0])
            elif new_piece['x'] < 0:
                new_piece['x'] = 0

            # If still invalid, don't rotate
            if not self.is_valid_position(new_piece):
                return piece

        return new_piece

    def is_valid_position(self, piece):
        # Check if the piece is within bounds and not colliding with other pieces
        for y, row in enumerate(piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = piece['x'] + x
                    board_y = piece['y'] + y

                    # Check if out of bounds
                    if (board_x < 0 or board_x >= BOARD_WIDTH or
                        board_y >= BOARD_HEIGHT):
                        return False

                    # Check if colliding with existing pieces on the board
                    if board_y >= 0 and self.board[board_y][board_x]:
                        return False
        return True

    def merge_piece_to_board(self):
        # Add the current piece to the board
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    board_x = self.current_piece['x'] + x
                    board_y = self.current_piece['y'] + y
                    if 0 <= board_y < BOARD_HEIGHT and 0 <= board_x < BOARD_WIDTH:
                        self.board[board_y][board_x] = self.current_piece['color']

    def clear_lines(self):
        lines_cleared = 0
        y = BOARD_HEIGHT - 1
        while y >= 0:
            if all(self.board[y]):
                # Move all lines above down
                for y2 in range(y, 0, -1):
                    self.board[y2] = self.board[y2-1][:]
                # Clear the top line
                self.board[0] = [0] * BOARD_WIDTH
                lines_cleared += 1
            else:
                y -= 1

        # Update score based on lines cleared
        if lines_cleared == 1:
            self.current_score += 100
        elif lines_cleared == 2:
            self.current_score += 300
        elif lines_cleared == 3:
            self.current_score += 500
        elif lines_cleared >= 4:
            self.current_score += 800

    def move_piece(self, dx, dy):
        # Create a new piece with the moved position
        new_piece = self.current_piece.copy()
        new_piece['x'] += dx
        new_piece['y'] += dy

        if self.is_valid_position(new_piece):
            self.current_piece = new_piece
            return True
        return False

    def drop_piece(self):
        # Move the piece down until it hits something
        while self.move_piece(0, 1):
            pass

        # Merge the piece to the board and get a new piece
        self.merge_piece_to_board()
        self.clear_lines()
        self.current_piece = self.new_piece()

    def draw_board(self):
        # Draw the game board
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(
                        self.screen,
                        self.board[y][x],
                        (BOARD_X + x * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (BOARD_X + x * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                        1
                    )

    def draw_piece(self):
        # Draw the current falling piece
        if not self.current_piece:
            return

        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        self.screen,
                        self.current_piece['color'],
                        (BOARD_X + (self.current_piece['x'] + x) * BLOCK_SIZE,
                         BOARD_Y + (self.current_piece['y'] + y) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE)
                    )
                    pygame.draw.rect(
                        self.screen,
                        WHITE,
                        (BOARD_X + (self.current_piece['x'] + x) * BLOCK_SIZE,
                         BOARD_Y + (self.current_piece['y'] + y) * BLOCK_SIZE,
                         BLOCK_SIZE, BLOCK_SIZE),
                        1
                    )

    def draw_score(self):
        # Draw the score information
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        last_score_text = self.font.render(f"Last Game Score: {self.last_game_score}", True, WHITE)
        current_score_text = self.font.render(f"This Game Score: {self.current_score}", True, WHITE)

        # Position on the right side
        score_x = SCREEN_WIDTH - max(high_score_text.get_width(),
                                     last_score_text.get_width(),
                                     current_score_text.get_width()) - 20

        self.screen.blit(high_score_text, (score_x, 20))
        self.screen.blit(last_score_text, (score_x, 50))
        self.screen.blit(current_score_text, (score_x, 80))

    def draw_game_over(self):
        # Draw game over message
        game_over_text = self.font.render("GAME OVER - Press R to Restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)

    def draw_grid(self):
        # Draw the grid lines
        for x in range(BOARD_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                WHITE,
                (BOARD_X + x * BLOCK_SIZE, BOARD_Y),
                (BOARD_X + x * BLOCK_SIZE, BOARD_Y + BOARD_HEIGHT * BLOCK_SIZE)
            )
        for y in range(BOARD_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                WHITE,
                (BOARD_X, BOARD_Y + y * BLOCK_SIZE),
                (BOARD_X + BOARD_WIDTH * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE)
            )

    def run(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        if event.key == pygame.K_LEFT:
                            self.move_piece(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            self.move_piece(1, 0)
                        elif event.key == pygame.K_DOWN:
                            self.move_piece(0, 1)
                        elif event.key == pygame.K_UP:
                            self.current_piece = self.rotate_piece(self.current_piece)
                        elif event.key == pygame.K_SPACE:
                            self.drop_piece()

                    if event.key == pygame.K_r:
                        self.reset_game()

            # Game logic
            if not self.game_over:
                self.fall_counter += 1
                if self.fall_counter >= self.fall_speed:
                    self.fall_counter = 0
                    # Move piece down
                    if not self.move_piece(0, 1):
                        # If can't move down, merge to board and get new piece
                        self.merge_piece_to_board()
                        self.clear_lines()
                        self.current_piece = self.new_piece()

            # Drawing
            self.screen.fill(BLACK)

            # Draw board border
            pygame.draw.rect(
                self.screen,
                WHITE,
                (BOARD_X - 2, BOARD_Y - 2, BOARD_WIDTH * BLOCK_SIZE + 4, BOARD_HEIGHT * BLOCK_SIZE + 4),
                2
            )

            self.draw_grid()
            self.draw_board()
            self.draw_piece()
            self.draw_score()

            if self.game_over:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Tetris()
    game.run()
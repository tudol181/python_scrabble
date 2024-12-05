import pygame
import random
from collections import Counter

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrabble Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont("arial", 36)

# Board setup
board_size = 15  # 15x15 board
tile_size = 40  # Size of each square
board_origin = (100, 50)  # Top-left corner of the board

# Scrabble letter values
letter_values = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
}

# Tile bag: A finite pool of Scrabble tiles
tile_bag = list("E"*12 + "A"*9 + "I"*9 + "O"*8 + "N"*6 + "R"*6 + "T"*6 +
                "L"*4 + "S"*4 + "U"*4 + "D"*4 + "G"*3 + "B"*2 + "C"*2 +
                "M"*2 + "P"*2 + "F"*2 + "H"*2 + "V"*2 + "W"*2 + "Y"*2 +
                "K"*1 + "J"*1 + "X"*1 + "Q"*1 + "Z"*1)
random.shuffle(tile_bag)

# Initialize board
board = [[None for _ in range(board_size)] for _ in range(board_size)]

# Player setup
player_tiles = [random.sample(tile_bag, 7), random.sample(tile_bag, 7)]
for tiles in player_tiles:
    for tile in tiles:
        tile_bag.remove(tile)
scores = [0, 0]
current_player = 0

# Game variables
selected_tile = None
running = True


def draw_board():
    """Draw the Scrabble board grid."""
    for row in range(board_size):
        for col in range(board_size):
            x = board_origin[0] + col * tile_size
            y = board_origin[1] + row * tile_size
            rect = pygame.Rect(x, y, tile_size, tile_size)
            pygame.draw.rect(screen, GRAY, rect, 2)
            if board[row][col]:
                text = font.render(board[row][col], True, BLUE)
                screen.blit(text, (x + 10, y + 5))


def draw_player_tiles():
    """Draw the current player's tiles at the bottom of the screen."""
    x_start = board_origin[0]
    y_start = screen_height - 100
    for i, letter in enumerate(player_tiles[current_player]):
        x = x_start + i * (tile_size + 10)
        rect = pygame.Rect(x, y_start, tile_size, tile_size)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, GRAY, rect, 2)
        text = font.render(letter, True, BLACK)
        screen.blit(text, (x + 10, y_start + 5))


def get_board_position(mouse_pos):
    """Convert mouse position to board grid position."""
    x, y = mouse_pos
    x -= board_origin[0]
    y -= board_origin[1]
    if 0 <= x < board_size * tile_size and 0 <= y < board_size * tile_size:
        col = x // tile_size
        row = y // tile_size
        return row, col
    return None


def calculate_score(placed_tiles):
    """Calculate the score for the tiles placed in this turn."""
    return sum(letter_values[tile] for tile in placed_tiles)


def refill_tiles():
    """Refill the player's tiles from the tile bag."""
    while len(player_tiles[current_player]) < 7 and tile_bag:
        new_tile = tile_bag.pop()
        player_tiles[current_player].append(new_tile)


# Game loop
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            board_pos = get_board_position(mouse_pos)

            # If a tile is selected and clicked on the board
            if board_pos and selected_tile:
                row, col = board_pos
                if not board[row][col]:  # Check if the spot is empty
                    board[row][col] = selected_tile
                    player_tiles[current_player].remove(selected_tile)
                    scores[current_player] += calculate_score([selected_tile])
                    selected_tile = None
                    refill_tiles()
                    current_player = (current_player + 1) % 2  # Alternate turn

            # Check if clicking on player's tiles
            x_start = board_origin[0]
            y_start = screen_height - 100
            for i, letter in enumerate(player_tiles[current_player]):
                tile_rect = pygame.Rect(x_start + i * (tile_size + 10), y_start, tile_size, tile_size)
                if tile_rect.collidepoint(mouse_pos):
                    selected_tile = letter

    # Draw everything
    draw_board()
    draw_player_tiles()

    # Display player scores
    score_text = font.render(f"Player 1: {scores[0]}   Player 2: {scores[1]}", True, BLACK)
    screen.blit(score_text, (board_origin[0], board_origin[1] - 40))

    # Highlight selected tile
    if selected_tile:
        text = font.render(f"Selected: {selected_tile}", True, BLACK)
        screen.blit(text, (board_origin[0], screen_height - 150))

    # Indicate current player's turn
    turn_text = font.render(f"Player {current_player + 1}'s Turn", True, BLACK)
    screen.blit(turn_text, (screen_width - 250, 10))

    pygame.display.flip()

pygame.quit()

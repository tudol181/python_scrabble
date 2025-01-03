import pygame


class ScrabbleTable:
    def __init__(self, screen, grid_size=15, cell_size=40):

        self.screen = screen
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.colors = {
            "background": (255, 255, 255),  # White
            "line": (0, 0, 0),  # Black
            "premium_word": (255, 182, 193),  # Light pink
            "premium_letter": (135, 206, 250),  # Light blue
        }
        self.premium_positions = {
            "word": [(0, 0), (7, 0), (14, 0), (0, 7), (14, 7), (0, 14), (7, 14), (14, 14)],
            "letter": [(5, 1), (9, 1), (1, 5), (13, 5), (5, 13), (9, 13), (1, 9), (13, 9)],
        }

    def draw_grid(self):
        """Draw the Scrabble grid."""
        self.screen.fill(self.colors["background"])
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                if (row, col) in self.premium_positions["word"]:
                    pygame.draw.rect(self.screen, self.colors["premium_word"], rect)
                elif (row, col) in self.premium_positions["letter"]:
                    pygame.draw.rect(self.screen, self.colors["premium_letter"], rect)
                pygame.draw.rect(self.screen, self.colors["line"], rect, 1)

    def display(self):
        """Update the screen."""
        pygame.display.flip()


# Example usage:
def main():
    pygame.init()
    screen_size = 600
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Scrabble Table")

    table = ScrabbleTable(screen, grid_size=15, cell_size=screen_size // 15)
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        table.draw_grid()
        table.display()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()

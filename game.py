import sys

import pygame

from constants import PLAYER_TILE_POSITIONS, LETTERS
from image import LetterParser
from scrabble_rules import Scrabble


class SceneBase:
    def __init__(self):
        self.next = self
    def process_input(self, events, pressed_keys):
        print("uh-oh, you didn't override this in the child class")

    def update(self):
        print("uh-oh, you didn't override this in the child class")

    def render(self, screen):
        print("uh-oh, you didn't override this in the child class")

    def SwitchToScene(self, next_scene):
        self.next = next_scene

    def Terminate(self):
        self.SwitchToScene(None)

def run_game(width, height, fps, starting_scene):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    active_scene = starting_scene

    while active_scene is not None:
        pressed_keys = pygame.key.get_pressed()

        # Event filtering
        filtered_events = []
        for event in pygame.event.get():
            quit_attempt = False
            if event.type == pygame.QUIT:
                quit_attempt = True
            elif event.type == pygame.KEYDOWN:
                alt_pressed = pressed_keys[pygame.K_LALT] or \
                              pressed_keys[pygame.K_RALT]
                if event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                elif event.key == pygame.K_F4 and alt_pressed:
                    quit_attempt = True

            if quit_attempt:
                active_scene.Terminate()
            else:
                filtered_events.append(event)

        active_scene.process_input(filtered_events, pressed_keys)
        active_scene.update()
        active_scene.render(screen)

        active_scene = active_scene.next

        pygame.display.flip()
        clock.tick(fps)

def tile_to_pixel(x, y):
    """
    Takes an x, y coordinate of the board and translates into the
    corresponding pixel coordinate.

    Note: 0, 0 is top left of board.
    """
    pixel_x = 2 + 40*x
    pixel_y = 2 + 40*y
    return pixel_x, pixel_y

def pixel_to_tile(x, y):
    """
    Takes an x, y coordinate of the cursor and translates into the
    corresponding tile coordinate.
    """
    tile_x = (x - 2)//40
    tile_y = (y - 2)//40
    return tile_x, tile_y

class Board(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Tile(pygame.sprite.Sprite):
    def __init__(self, letter, spritesheet, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = spritesheet.image_at(LETTERS[letter])
        self.letter = letter
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.tray_position = location
        self.on_board = False
        self.board_x = 0
        self.board_y = 0

    def move(self, pos):
        """Moves the tile to either the board or back to the tray."""
        tile_x, tile_y = pixel_to_tile(*pos)

        # Move to valid tile otherwise return to tray
        if 0 <= tile_x < 15 and 0 <= tile_y < 15:
            self.rect.topleft = tile_to_pixel(tile_x, tile_y)
            self.on_board = True
            self.board_x = tile_x
            self.board_y = tile_y
        else:
            self.rect.topleft = self.tray_position
            self.on_board = False

    def tile(self):
        """Returns the tuple (board_x, board_y, letter)."""
        return self.board_x, self.board_y, self.letter

    def rerack(self):
        """Moves the tile back to the rack."""
        self.rect.topleft = self.tray_position
        self.on_board = False

class TitleScene(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.selected_players = 2

        self.buttons = {
            2: pygame.Rect(300, 250, 200, 50),
            3: pygame.Rect(300, 320, 200, 50),
            4: pygame.Rect(300, 390, 200, 50),
        }
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for player_count, rect in self.buttons.items():
                    if rect.collidepoint(event.pos):
                        self.selected_players = player_count
                        self.SwitchToScene(GameScene(self.selected_players))

    def update(self):
        pass

    def render(self, screen):
        # For the sake of brevity, the title scene is a blank red screen
        screen.fill((255, 255, 255))
        for player_count, rect in self.buttons.items():
            pygame.draw.rect(screen, (0, 255, 0), rect)
            text = self.font.render(f"{player_count} Players", True, (0, 0, 0))
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

            # Render title text (optional)
        title_text = self.font.render("Select Number of Players", True, (0, 0, 0))
        screen.blit(title_text, (300, 150))


class GameScene(SceneBase):
    def __init__(self, selected_players):
        SceneBase.__init__(self)
        self.scrabble = Scrabble(selected_players)
        self.board = Board('imgs/board.jpg', [0, 0])
        self.letter_ss = LetterParser('imgs/letters.jpg')
        self.player_tiles = []
        self.game_tiles = []
        self.selected_tile = None
        self.offset_x = 0
        self.offset_y = 0
        self.current_player = 1
        self.scrabble._print_board()
        self._update_player_tiles()
        self.changes = [0] * selected_players

    def process_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    self._submit_turn()
                elif event.key == pygame.K_p:
                    self.scrabble._print_board()
                elif event.key == pygame.K_c:  # c to change the tiles
                    if(self.changes[self.scrabble.current_player - 1] >= 2):
                        print("You cannot change more than 3 times")
                        break
                    else:
                        self._change_selected_tile()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for tile in self.player_tiles:
                        if tile.rect.collidepoint(event.pos):
                            self.selected_tile = tile
                            mouse_x, mouse_y = event.pos
                            self.offset_x = tile.rect.left - mouse_x
                            self.offset_y = tile.rect.top - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.selected_tile:
                        if self._hits_tile(event.pos, self.selected_tile):
                            self.selected_tile.rerack()
                        else:
                            self.selected_tile.move(event.pos)

                        # Not selected anymore
                        self.selected_tile = None

            elif event.type == pygame.MOUSEMOTION:
                if self.selected_tile:
                    mouse_x, mouse_y = event.pos
                    self.selected_tile.rect.left = mouse_x + self.offset_x
                    self.selected_tile.rect.top = mouse_y + self.offset_y

    def _change_selected_tile(self):
        """Handles exchanging tiles for the current player."""
        current_rack = self.scrabble.get_rack()

        if not current_rack:
            print("Rack is empty; cannot exchange tiles.")
            return

        self.changes[self.scrabble.current_player - 1] += 1
        print("playerul", self.scrabble.current_player)
        print("schimbari", self.changes)
        print("\n\n")
        print(f"Current rack: {current_rack}")
        self.scrabble.exchange_tiles(current_rack)
        self._update_player_tiles()

    def _update_player_tiles(self):
        """Updates the tiles displayed for the current player's rack."""
        self.player_tiles = [
            Tile(letter, self.letter_ss, PLAYER_TILE_POSITIONS[i])
            for i, letter in enumerate(self.scrabble.get_rack())
        ]

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 255))
        screen.blit(self.board.image, self.board.rect)

        for tile in self.player_tiles:
            screen.blit(tile.image, tile.rect)

        for tile in self.game_tiles:
            screen.blit(tile.image, tile.rect)

        if self.selected_tile:
            screen.blit(self.selected_tile.image, self.selected_tile.rect)
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 30)

        #turn info
        turn_text = font.render(f"Player {self.scrabble.current_player}'s Turn", True, (255, 255, 255))
        screen.blit(turn_text, (250, 700))

        #score info
        scores = self.scrabble.get_scores()
        score_text_y = 50
        score_text_x = 620

        for player_num, score in enumerate(scores, start=1):
            score_text = font.render(f"Player {player_num}: {score} pts", True, (255, 255, 255))
            screen.blit(score_text, (score_text_x, score_text_y))
            score_text_y += 40

        #lost button

    def _hits_tile(self, pos, ignore=None):
        """Checks if the position hits an existing tile."""
        for tile in self.player_tiles + self.game_tiles:
            if tile == ignore:
                continue
            if tile.rect.collidepoint(pos):
                return True
        return False

    def _submit_turn(self):
        """Handles submitting the current turn."""
        tiles = [tile.tile() for tile in self.player_tiles if tile.on_board]

        if not tiles:
            print("No tiles played. Turn skipped.")
            return

        if self.scrabble.submit_turn(tiles):
            for tile in self.player_tiles:
                if tile.on_board:
                    self.game_tiles.append(tile)

            self._update_player_tiles()
            print("Turn successfully submitted. Advancing to the next player.")
        else:
            print("Invalid turn. Returning tiles to the rack.")
            for tile in self.player_tiles:
                tile.rerack()



run_game(800, 800, 60, TitleScene())
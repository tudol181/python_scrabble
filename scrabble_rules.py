from random import shuffle
from constants import LETTERS_FREQS, LETTER_SCORE, WORD_MULTIPLIERS, LETTER_MULTIPLIERS


class Scrabble:
    def __init__(self, max_players=2):
        self._populate_bag()
        self.shuffle_bag()
        self._board = [
            [None] * 15 for _ in range(15)
        ]
        self._move_count = 0
        self.current_player = 1
        self.max_players = max_players
        self.player_racks = [[] for _ in range(self.max_players)]
        self._player_score = [0] * self.max_players
        for i in range(self.max_players):
            self._draw_tiles(7, i + 1)

    def _print_board(self):
        for i in range(15):
            for j in range(15):
                if self._board[i][j] is None:
                    print('_', end='')
                elif self._board[i][j] == ' ':
                    print('-', end='')
                else:
                    print(self._board[i][j], end='')
            print('')

        for i, rack in enumerate(self.player_racks, 1):
            print(f"Player {i}'s rack:", ' '.join(rack))

    def _populate_bag(self):
        self._bag = []
        for letter in LETTERS_FREQS:
            for _ in range(LETTERS_FREQS[letter]):
                self._bag.append(letter)

    def shuffle_bag(self):
        shuffle(self._bag)

    def _draw_tiles(self, amount, player):
        # Draw tiles only for the current player
        if len(self._bag) > 0:
            for _ in range(amount):
                if len(self._bag) > 0:
                    self.player_racks[player - 1].append(self._bag.pop())

    def get_rack(self, player=None):
        if player:
            return self.player_racks[player - 1]
        return self.player_racks[self.current_player - 1]

    def get_racks(self):
        return self.player_racks[:]

    def exchange_tiles(self, old, player=None):
        """
        Returns the old tiles to the bag and draws an equal number to replace
        them.
        """
        # Only can return letters from the player's rack
        if len(old) > len(self._bag):
            return
        # Add the new tiles to the rack
        self._draw_tiles(len(old), player)

        # Remove the old from the rack and add them to the bag
        for letter in old:
            self.player_racks[player - 1].remove(letter)
            self._bag.append(letter)

        self.shuffle_bag()

    def submit_turn(self, tiles):
        if self._is_valid_move(tiles):
            self._score_turn(tiles)
            self._place_move(tiles)
            self._updateplayer_racks(tiles)
            return True
        else:
            return False

    def _is_valid_move(self, tiles):
        """
        Returns True if the list of tiles forms valid words and are placed
        in a correct manner.
        """
        rows = []
        cols = []
        letters = []

        for row, col, letter in tiles:
            rows.append(row)
            cols.append(col)
            letters.append(letter)

        # Reset score accumulation
        self._turn_score = 0

        return (
                self._all_letters_from_rack(letters) and
                self._is_colinear(rows, cols) and
                self._all_unique_places(rows, cols) and
                self._is_contiguous(rows, cols) and
                self._touches_others(rows, cols) and
                self._all_vaild_words(tiles)
        )

    def _all_letters_from_rack(self, letters):
        """
        Determines if all letters are present in the current player's rack.
        """
        # Get the current player's rack
        rack = self.player_racks[self.current_player - 1]  # Access the correct player's rack

        for letter in letters:
            if letter in rack:
                rack.remove(letter)  # Remove the letter from the rack after using it
            else:
                print("Validation: Not all letters are from the rack")
                return False

        return True

    def _is_colinear(self, rows, cols):
        """
        True if all rows are equal or all cols are equal.
        """
        ret = len(set(rows)) == 1 or len(set(cols)) == 1
        if not ret:
            print("Validation: Tiles are not colinear")

        return ret

    def _all_unique_places(self, rows, cols):
        """
        Cannot have duplicate places
        """
        places = list(zip(rows, cols))
        ret = len(set(places)) == len(places)
        if not ret:
            print("Validation: Tiles are not uniquely placed")
            print(places)
        return ret

    def _is_contiguous(self, rows, cols):
        """
        Tiles must be in a contiguous line with existing tiles, if needed.
        """
        # Case: Only one tile
        if len(cols) == len(rows) == 1:
            return True

        is_vertical = len(set(cols)) == 1

        if is_vertical:
            start = min(rows)
            end = max(rows)
            col = cols[0]

            for row in range(start, end):
                if row not in rows and self._board[row][col] is None:
                    print("Validation: Tiles are not contiguous")
                    return False

        else:
            start = min(cols)
            end = max(cols)
            row = rows[0]

            for col in range(start, end):
                if col not in cols and self._board[row][col] is None:
                    print("Validation: Tiles are not contiguous")
                    return False

        return True

    def _touches_others(self, rows, cols):
        """
        Word being played must touch existing tiles, or first move must start
        in the middle of the board.
        """
        places = list(zip(rows, cols))

        if self._move_count == 0:
            ret = (7, 7) in places
            if not ret:
                print("Validation: First move wasn't on star")
            return ret
        else:
            for row, col in places:
                # Above
                if row > 0 and self._board[row - 1][col] is not None:
                    return True
                # Below
                if row < 14 and self._board[row + 1][col] is not None:
                    return True
                # Left
                if col > 0 and self._board[row][col - 1] is not None:
                    return True
                # Right
                if col < 14 and self._board[row][col + 1] is not None:
                    return True
            print("Validation: Tiles do not touch existing tiles")
            return False

    def _all_vaild_words(self, tiles):
        """
        Determines if all the words formed are valid.
        Accumulates the score for valid words
        Assumes tiles are colinear and contiguous.
        """
        rows = []
        cols = []
        letters = {}
        for row, col, letter in tiles:
            rows.append(row)
            cols.append(col)
            letters[(row, col)] = letter

        is_vertical = len(set(cols)) == 1

        if is_vertical:  # Also true if only one tile was placed
            start = min(rows)
            end = max(rows)
            col = cols[0]

            # Start may be extened by existing tiles
            for row in range(start - 1, -1, -1):
                if self._board[row][col] is not None:
                    start = row
                else:
                    # Found first open place, quit
                    break
            # Same for the end
            for row in range(end + 1, 15):
                if self._board[row][col] is not None:
                    end = row
                else:
                    # Found first open place, quit
                    break

            # If only one tile was played, there may not be a vertical word
            if start != end:
                # Check the word that was made vertically
                word = ''
                for row in range(start, end + 1):
                    word += letters.get((row, col), self._board[row][col])
                if not self._is_valid_word(word):
                    print("Validation: Invalid word:", word)
                    return False

                self._score_word((start, col), (end, col), letters)

            # Check all horizontal words made from each of the new tiles
            for row, col, _ in tiles:
                start_h = col
                end_h = col

                # Start may be extened by existing tiles
                for col_h in range(start_h - 1, -1, -1):
                    if self._board[row][col_h] is not None:
                        start_h = col_h
                    else:
                        # Found first open place, quit
                        break
                # Same for the end
                for col_h in range(end_h + 1, 15):
                    if self._board[row][col_h] is not None:
                        end_h = col_h
                    else:
                        # Found first open place, quit
                        break

                # No word made horizontally
                if start_h == end_h:
                    # Issue if only one tile was placed on start
                    if len(tiles) == 1:
                        print("Validation: Invalid word:", word)
                        return False
                    continue

                # Make and check word
                word = ''
                for col_h in range(start_h, end_h + 1):
                    word += letters.get((row, col_h), self._board[row][col_h])
                if not self._is_valid_word(word):
                    print("Validation: Invalid word:", word)
                    return False

                self._score_word((row, start_h), (row, end_h), letters)

        else:  # is horizontal
            start = min(cols)
            end = max(cols)
            row = rows[0]

            # Start may be extened by existing tiles
            for col in range(start - 1, -1, -1):
                if self._board[row][col] is not None:
                    start = col
                else:
                    # Found first open place, quit
                    break
            # Same for the end
            for col in range(end + 1, 15):
                if self._board[row][col] is not None:
                    end = col
                else:
                    # Found first open place, quit
                    break

            # Check the word that was made horizontally
            word = ''
            for col in range(start, end + 1):
                word += letters.get((row, col), self._board[row][col])
            if not self._is_valid_word(word):
                print("Validation: Invalid word:", word)
                return False

            self._score_word((row, start), (row, end), letters)

            # Check all vertical words made from each of the new tiles
            for row, col, _ in tiles:
                start_v = row
                end_v = row

                # Start may be extened by existing tiles
                for row_v in range(start_v - 1, -1, -1):
                    if self._board[row_v][col] is not None:
                        start_v = row_v
                    else:
                        # Found first open place, quit
                        break
                # Same for the end
                for row_v in range(end_v + 1, 15):
                    if self._board[row_v][col] is not None:
                        end_v = row_v
                    else:
                        # Found first open place, quit
                        break

                # No word made vertically
                if start_v == end_v:
                    continue

                # Make and check word
                word = ''
                for row_v in range(start_v, end_v + 1):
                    word += letters.get((row_v, col), self._board[row_v][col])
                if not self._is_valid_word(word):
                    print("Validation: Invalid word:", word)
                    return False

                self._score_word((start_v, col), (end_v, col), letters)

        # Validated all words
        print("All words validated")
        return True

    def _is_valid_word(self, word):
        """
        Uses binary search to determine if the word is valid, directly in the file.
        """
        word = word.upper()  # Ensure the word is in uppercase

        # Open the file for reading
        with open('words.txt', 'r') as file:
            low, high = 0, 279496  # Number of words in the file
            # Binary search
            while low <= high:
                mid = (low + high) // 2
                file.seek(self._get_line_offset(file, mid))
                line = file.readline().strip().upper()  # Convert line to uppercase
                # print(line)
                if line == word:
                    return True
                elif line < word:
                    low = mid + 1
                else:
                    high = mid - 1

        return False

    def _get_line_offset(self, file, line_num):
        """
        Returns the byte offset for the given line number.
        """
        file.seek(0)
        offset = 0
        for i in range(line_num):
            offset += len(file.readline()) + 1
        return offset

    def _place_move(self, tiles):
        """
        Given a valid set of tiles, adds them to the board.
        """
        self._move_count += 1
        for row, col, letter in tiles:
            self._board[row][col] = letter

    def _update_player_racks(self, tiles):
        """
        Removes the letters from the player rack and draws new ones.
        """
        # Get the current player's rack
        current_player_rack = self.player_racks[self.current_player - 1]  # Get the correct player's rack

        # Remove the tiles from the player's rack
        for _, _, letter in tiles:
            if letter in current_player_rack:
                current_player_rack.remove(letter)
            else:
                print(f"Tile {letter} not found in current player's rack.")

        # Draw new tiles for the current player
        self._draw_tiles(len(tiles))  # Draw the same number of tiles that were played

    def _score_word(self, start, end, letters):
        """
        Adds the score of the valid word between start and end.
        """
        score = 0
        multiplier = 1
        for row in range(start[0], end[0] + 1):
            for col in range(start[1], end[1] + 1):
                if (row, col) in letters:
                    # Check for score modifiers
                    multiplier *= WORD_MULTIPLIERS.get((row, col), 1)
                    score += LETTER_SCORE[letters[(row, col)]] * LETTER_MULTIPLIERS.get((row, col), 1)
                else:
                    # Tile must be on board, add it's value
                    score += LETTER_SCORE[self._board[row][col]]

        self._turn_score += score * multiplier

    def _score_turn(self, tiles):
        """
        Applies the score of the last validated move to the player score.
        """
        self._player_score += self._turn_score
        # Check for Bingo
        if len(tiles) == 7:
            self._player_score += 50
        # Reset turn score counter
        self._turn_score = 0
        print("Score:", self._player_score)


# Assuming the Scrabble class is already imported and set up

def test_scrabble_game():
    game = Scrabble(max_players=2)  # Two players for the test

    # Initial board print
    game._print_board()

    # Player 1's rack before the turn
    print(f"Player 1's initial rack: {game.get_rack(1)}")

    # Simulate Player 1's turn: forming the word "CAT" at positions (7, 7), (7, 8), (7, 9)
    tiles_player_1 = [(7, 7, 'C'), (7, 8, 'A'), (7, 9, 'T')]  # A valid word in the center of the board
    print("\nPlayer 1 plays the word 'CAT' at (7, 7), (7, 8), (7, 9)")

    if game.submit_turn(tiles_player_1):
        print("Player 1's move validated successfully.")
    else:
        print("Player 1's move failed validation.")

    # Print board after Player 1's move
    game._print_board()

    # Switch to Player 2 and check their rack
    game.current_player = 2
    print(f"\nPlayer 2's rack: {game.get_rack(2)}")

    # Simulate Player 2's turn: forming the word "DOG" at positions (8, 7), (8, 8), (8, 9)
    tiles_player_2 = [(8, 7, 'D'), (8, 8, 'O'), (8, 9, 'G')]  # Another valid word
    print("\nPlayer 2 plays the word 'DOG' at (8, 7), (8, 8), (8, 9)")

    if game.submit_turn(tiles_player_2):
        print("Player 2's move validated successfully.")
    else:
        print("Player 2's move failed validation.")

    # Print board after Player 2's move
    game._print_board()

    # Check final scores
    print(f"\nPlayer 1's score: {game._player_score[0]}")
    print(f"Player 2's score: {game._player_score[1]}")

# Run the test
# test_scrabble_game()

LETTER_MULTIPLIERS = {
    (0, 3): 2,
    (0, 11): 2,
    (1, 5): 3,
    (1, 9): 3,
    (2, 6): 2,
    (2, 8): 2,
    (3, 0): 2,
    (3, 7): 2,
    (3, 14): 2,
    (5, 1): 3,
    (5, 5): 3,
    (5, 9): 3,
    (5, 13): 3,
    (6, 2): 2,
    (6, 6): 2,
    (6, 8): 2,
    (6, 12): 2,
    (7, 3): 2,
    (7, 11): 2,
    (8, 2): 2,
    (8, 6): 2,
    (8, 8): 2,
    (8, 12): 2,
    (9, 1): 3,
    (9, 5): 3,
    (9, 9): 3,
    (9, 13): 3,
    (11, 0): 2,
    (11, 7): 2,
    (11, 14): 2,
    (12, 6): 2,
    (12, 8): 2,
    (13, 5): 3,
    (13, 9): 3,
    (14, 3): 2,
    (14, 11): 2,
}

WORD_MULTIPLIERS = {
    (0, 0): 3,
    (0, 7): 3,
    (0, 14): 3,
    (1, 1): 2,
    (1, 13): 2,
    (2, 2): 2,
    (2, 12): 2,
    (3, 3): 2,
    (3, 11): 2,
    (4, 4): 2,
    (4, 10): 2,
    (7, 0): 3,
    (7, 7): 2,
    (7, 14): 3,
    (10, 4): 2,
    (10, 10): 2,
    (11, 3): 2,
    (11, 11): 2,
    (12, 2): 2,
    (12, 12): 2,
    (13, 1): 2,
    (13, 13): 2,
    (14, 0): 3,
    (14, 7): 3,
    (14, 14): 3,
}

LETTERS_FREQS = {
    'a': 9,
    'b': 2,
    'c': 2,
    'd': 4,
    'e': 12,
    'f': 2,
    'g': 3,
    'h': 2,
    'i': 9,
    'j': 1,
    'k': 1,
    'l': 4,
    'm': 2,
    'n': 6,
    'o': 8,
    'p': 2,
    'q': 1,
    'r': 6,
    's': 4,
    't': 6,
    'u': 4,
    'v': 2,
    'w': 2,
    'x': 1,
    'y': 2,
    'z': 1,
    ' ': 2,
}

LETTER_SCORE = {
    'a': 1,
    'b': 3,
    'c': 3,
    'd': 2,
    'e': 1,
    'f': 4,
    'g': 2,
    'h': 4,
    'i': 1,
    'j': 8,
    'k': 5,
    'l': 1,
    'm': 3,
    'n': 1,
    'o': 1,
    'p': 3,
    'q': 10,
    'r': 1,
    's': 1,
    't': 1,
    'u': 1,
    'v': 4,
    'w': 4,
    'x': 8,
    'y': 4,
    'z': 10,
    ' ': 0,
}

# Dict to hold spritesheet positions for each letter
LETTERS = {
    'a': (0, 0, 37, 37),
    'b': (38, 0, 37, 37),
    'c': (76, 0, 37, 37),
    'd': (114, 0, 37, 37),
    'e': (152, 0, 37, 37),
    'f': (190, 0, 37, 37),
    'g': (0, 38, 37, 37),
    'h': (38, 38, 37, 37),
    'i': (76, 38, 37, 37),
    'j': (114, 38, 37, 37),
    'k': (152, 38, 37, 37),
    'l': (190, 38, 37, 37),
    'm': (0, 76, 37, 37),
    'n': (38, 76, 37, 37),
    'o': (76, 76, 37, 37),
    'p': (114, 76, 37, 37),
    'q': (152, 76, 37, 37),
    'r': (190, 76, 37, 37),
    's': (0, 114, 37, 37),
    't': (38, 114, 37, 37),
    'u': (76, 114, 37, 37),
    'v': (114, 114, 37, 37),
    'w': (152, 114, 37, 37),
    'x': (190, 114, 37, 37),
    'y': (0, 152, 37, 37),
    'z': (38, 152, 37, 37),
    ' ': (76, 152, 37, 37),
}

PLAYER_TILE_POSITIONS = [
    (162, 640),
    (202, 640),
    (242, 640),
    (282, 640),
    (322, 640),
    (362, 640),
    (402, 640),
]

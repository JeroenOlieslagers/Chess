import pygame
import math
import numpy as np
from init import *


class Board:
    """Class to draw everything on screen (pieces, tile colours etc)"""
    def __init__(self, display, side, offset=0):
        self.display = display                              # pygame display object
        self.size = int(side / 8)                           # Used to convert from x-y coordinates to pixels
        self.offset = offset                                # Offset of top-left of board (tuple)
        self.pieces = piecesDic                             # Dictionary mapping coordinates to pieces
        self.primary_colour = colours['green']
        self.secondary_colour = colours['cream']
        self.highlight_colour_pri = colours['dark_green']
        self.highlight_colour_sec = colours['yellow']
        self.sounds = {'move': None, 'take': None, 'error': None, 'check': None}

    def local_to_global(self, pos):
        """Converts from local to global coordinates"""
        return pos[0] * self.size, pos[1] * self.size

    def global_to_local(self, coords):
        """Converts from local to global coordinates"""
        return int(coords[0] / self.size), int(coords[1] / self.size)

    def set_primary_colour(self, col):
        """Sets the primary colour of the board (rgb tuple)"""
        self.primary_colour = col

    def set_secondary_colour(self, col):
        """Sets the secondary colour of the board (rgb tuple)"""
        self.secondary_colour = col

    def draw_tile(self, pos, col='default'):
        """Draws an individual tile with colour depending on coordinates and specified colour"""
        x, y = self.local_to_global(pos)
        # Default chess board pattern based on set main colours
        if col == 'default':
            if pos[0] % 2 == 0 and pos[1] % 2 == 1:
                pygame.draw.rect(self.display, self.primary_colour, (x, y, self.size, self.size))
            elif pos[0] % 2 == 1 and pos[1] % 2 == 0:
                pygame.draw.rect(self.display, self.primary_colour, (x, y, self.size, self.size))
            else:
                pygame.draw.rect(self.display, self.secondary_colour, (x, y, self.size, self.size))

        # Chess board pattern for highlighted cells
        elif col == 'highlight':
            if pos[0] % 2 == 0 and pos[1] % 2 == 1:
                pygame.draw.rect(self.display, self.highlight_colour_pri, (x, y, self.size, self.size))
            elif pos[0] % 2 == 1 and pos[1] % 2 == 0:
                pygame.draw.rect(self.display, self.highlight_colour_pri, (x, y, self.size, self.size))
            else:
                pygame.draw.rect(self.display, self.highlight_colour_sec, (x, y, self.size, self.size))

        # Red colour to indicate possible captures
        elif col == 'capture':
            if pos[0] % 2 == 0 and pos[1] % 2 == 1:
                pygame.draw.rect(self.display, colours['dark_red'], (x, y, self.size, self.size))
            elif pos[0] % 2 == 1 and pos[1] % 2 == 0:
                pygame.draw.rect(self.display, colours['dark_red'], (x, y, self.size, self.size))
            else:
                pygame.draw.rect(self.display, colours['dark_red'], (x, y, self.size, self.size))

        # Blue colour to indicate check
        elif col == 'check':
            if pos[0] % 2 == 0 and pos[1] % 2 == 1:
                pygame.draw.rect(self.display, colours['blue'], (x, y, self.size, self.size))
            elif pos[0] % 2 == 1 and pos[1] % 2 == 0:
                pygame.draw.rect(self.display, colours['blue'], (x, y, self.size, self.size))
            else:
                pygame.draw.rect(self.display, colours['blue'], (x, y, self.size, self.size))

        # Circles to indicate possible moves
        elif col == 'circles':
            if pos[0] % 2 == 0 and pos[1] % 2 == 1:
                pygame.draw.circle(self.display, colours['dark_grey'], (x + int(self.size / 2),
                                                                        y + int(self.size / 2)), int(self.size / 6))
            elif pos[0] % 2 == 1 and pos[1] % 2 == 0:
                pygame.draw.circle(self.display, colours['dark_grey'], (x + int(self.size / 2),
                                                                        y + int(self.size / 2)), int(self.size / 6))
            else:
                pygame.draw.circle(self.display, colours['light_grey'], (x + int(self.size / 2),
                                                                         y + int(self.size / 2)), int(self.size / 6))

    def draw(self):
        """Draws 8x8 standard chess board"""
        for i in range(8):
            for j in range(8):
                self.draw_tile((i, j))

    def draw_piece(self, piece, pos):
        """Draws individual piece"""
        x, y = self.local_to_global(pos)
        self.display.blit(piece.img(), (x, y))

    def draw_starting_pieces(self):
        """Draws all pieces for staring game"""
        for item in self.pieces:
            self.draw_piece(self.pieces[item], item)


class Controller(Board):
    """Class to handle click events and miscellaneous functions"""
    def __init__(self, board):
        self.__dict__ = board.__dict__
        self.clicked = False                # Whether it is the selecting or moving click
        self.prev_select_click = None       # Position of previous selecting click
        self.prev_move_click = (0, 0)       # Position of previous moving click
        self.turn = 'w'                     # Keeps track of who's turn it is
        self.finished = False               # Determines when the game has ended

    def coords(self, coords):
        """Tells which square coordinates lie in"""
        x, y = self.global_to_local(coords)
        x = math.floor(x)
        y = math.floor(y)
        return x, y

    def select_piece(self, pos):
        """Highlights piece and draws possible moves"""
        if pos in self.pieces and self.pieces[pos].col == self.turn:
            self.draw_tile(pos, col='highlight')
            self.draw_piece(self.pieces[pos], pos)
            self.draw_moves(self.pieces[pos], pos)
            self.draw_capture(self.pieces[pos], pos)
            self.prev_select_click = pos
            self.clicked = True
        elif pos in self.pieces:
            print('Not your turn')
            self.sounds['error'].play()
        else:
            print('No piece at that location')
            self.sounds['error'].play()

    def reset(self):
        """Resets all effects on tiles"""
        # Reset possible moves tiles
        for tile in self.pieces[self.prev_select_click].tiles:
            self.draw_tile(tile)
        # Reset capture tiles
        for tile in self.pieces[self.prev_move_click].capture:
            self.draw_tile(tile)
            self.draw_piece(self.pieces[tile], tile)
        for tile in self.pieces[self.prev_select_click].capture:
            self.draw_tile(tile)
            self.draw_piece(self.pieces[tile], tile)
        self.draw_tile(self.prev_select_click)
        self.draw_piece(self.pieces[self.prev_select_click], self.prev_select_click)
        self.clicked = False

    def move_piece(self, pos1, pos2):
        """Moves piece from pos1 to pos2"""
        if pos2 in self.pieces:
                if self.pieces[pos2] == king_w or self.pieces[pos2] == king_b:
                    self.finished = True
        self.pieces[pos2] = self.pieces[pos1]
        del self.pieces[pos1]
        self.draw_tile(pos2)
        self.draw_piece(self.pieces[pos2], pos2)
        self.draw_tile(pos1)

    def draw_capture(self, piece, pos):
        """Draws possible capture tiles on board"""
        # Resets capture tiles
        piece.capture = []
        # Sets possible moves
        piece.possible_moves(pos, self.pieces)
        # Draws capture tiles
        for pos in piece.capture:
            if self.pieces[pos] == king_w and self.turn == 'b':
                self.draw_tile(pos, col='check')
                self.draw_piece(self.pieces[pos], pos)
                self.sounds['check'].play()
            elif self.pieces[pos] == king_b and self.turn == 'w':
                self.draw_tile(pos, col='check')
                self.draw_piece(self.pieces[pos], pos)
                self.sounds['check'].play()
            else:
                self.draw_tile(pos, col='capture')
                self.draw_piece(self.pieces[pos], pos)

    def draw_moves(self, piece, pos):
        """Draws possible moves on board"""
        # Resets moves
        piece.tiles = []
        # Sets possible moves for piece
        piece.possible_moves(pos, self.pieces)
        # Draws moves
        for pos in piece.tiles:
            self.draw_tile(pos, col='circles')

    def next_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'

    def click(self, event):
        """Handles click events"""
        pos = self.coords(event.pos)
        # Selecting piece
        if not self.clicked:
            self.select_piece(pos)
        # Moving piece
        else:
            # Resetting highlight and moves
            self.reset()
            if pos in self.pieces[self.prev_select_click].tiles:
                self.move_piece(self.prev_select_click, pos)
                self.draw_capture(self.pieces[pos], pos)
                self.prev_move_click = pos
                self.sounds['move'].play()
                self.next_turn()
            elif pos in self.pieces[self.prev_select_click].capture:
                self.move_piece(self.prev_select_click, pos)
                self.draw_capture(self.pieces[pos], pos)
                self.prev_move_click = pos
                self.sounds['take'].play()
                self.next_turn()
            else:
                print("Can't move piece there")


class Piece:
    def __init__(self, path, col):
        self.col = col              # Colour of piece (given)
        self.path = path            # Path to image file (given)
        self.value = 0              # Value of piece according to chess rules
        self.size = 80              # Constant
        self.capture = []           # Init
        self.tiles = []             # Init

    def img(self):
        """Returns Surface object as required by blit function"""
        return pygame.image.load(self.path)


class Pawn(Piece):
    def __init__(self, path, col):
        Piece.__init__(self, path, col)
        self.value = 1

    def possible_moves(self, pos, locations):
        """Sets possible moves for Pawn and possible captures"""
        x, y = pos
        # Pawns behave differently depending on which colour they are
        if self.col == 'w':
            a = 1
        else:
            a = -1
        # Checks for enemy pieces in allowed capture places
        if (x + 1, y - a) in locations and self.col != locations[(x + 1, y - a)].col:
            self.capture.append((x + 1, y - a))
        if (x - 1, y - a) in locations and self.col != locations[(x - 1, y - a)].col:
            self.capture.append((x - 1, y - a))
        # Checks whether or not the pawn is on its starting position
        if y == (280 + 200 * a)/self.size:
            if (x, y - a) not in locations:
                if (x, y - 2 * a) not in locations:
                    self.tiles.append((x, y - 2 * a))
                self.tiles.append((x, y - a))
        else:
            if (x, y - a) not in locations:
                self.tiles.append((x, y - a))


class Knight(Piece):
    def __init__(self, path, col):
        Piece.__init__(self, path, col)
        self.value = 3

    def possible_moves(self, pos, locations):
        """Sets possible moves for Knight and possible captures"""
        px = pos[0]
        py = pos[1] + 3
        qx = pos[0]
        qy = pos[1] - 3
        for n in range(2):
            px += 1
            py -= 1
            qx -= 1
            qy += 1
            if (px, py) in locations:
                if self.col != locations[(px, py)].col:
                    self.capture.append((px, py))
            else:
                self.tiles.append((px, py))
            if (px, qy) in locations:
                if self.col != locations[(px, qy)].col:
                    self.capture.append((px, qy))
            else:
                self.tiles.append((px, qy))
            if (qx, py) in locations:
                if self.col != locations[(qx, py)].col:
                    self.capture.append((qx, py))
            else:
                self.tiles.append((qx, py))
            if (qx, qy) in locations:
                if self.col != locations[(qx, qy)].col:
                    self.capture.append((qx, qy))
            else:
                self.tiles.append((qx, qy))


class Bishop(Piece):
    def __init__(self, path, col):
        Piece.__init__(self, path, col)
        self.value = 3

    def possible_moves(self, pos, locations):
        """Sets possible moves for Bishop and possible captures"""
        p = np.array([pos, pos, pos, pos])
        boo = [True, True, True, True]
        for m in range(8):
            p += [(1, 1), (1, -1), (-1, -1), (-1, 1)]
            for n in range(4):
                if tuple(p[n]) not in locations and boo[n]:
                    self.tiles.append(tuple(p[n]))
                elif boo[n] and self.col != locations[tuple(p[n])].col:
                    self.capture.append(tuple(p[n]))
                    boo[n] = False
                else:
                    boo[n] = False


class Rook(Piece):
    def __init__(self, path, col):
        Piece.__init__(self, path, col)
        self.value = 5

    def possible_moves(self, pos, locations):
        """Sets possible moves for Rook and possible captures"""
        p = np.array([pos, pos, pos, pos])
        boo = [True, True, True, True]
        for m in range(8):
            p += [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for n in range(4):
                if tuple(p[n]) not in locations and boo[n]:
                    self.tiles.append(tuple(p[n]))
                elif boo[n] and self.col != locations[tuple(p[n])].col:
                    self.capture.append(tuple(p[n]))
                    boo[n] = False
                else:
                    boo[n] = False


class Queen(Piece):
    def __init__(self, path, col):
        Piece.__init__(self, path, col)
        self.value = 9

    def possible_moves(self, pos, locations):
        """Sets possible moves for Queen and possible captures"""
        p = np.array([pos, pos, pos, pos, pos, pos, pos, pos])
        boo = [True, True, True, True, True, True, True, True]
        for m in range(8):
            p += [(1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
            for n in range(8):
                if tuple(p[n]) not in locations and boo[n]:
                    self.tiles.append(tuple(p[n]))
                elif boo[n] and self.col != locations[tuple(p[n])].col:
                    self.capture.append(tuple(p[n]))
                    boo[n] = False
                else:
                    boo[n] = False


class King(Piece):
    def __init__(self, path, col):
        Piece.__init__(self, path, col)
        self.value = -1

    def possible_moves(self, pos, locations):
        """Sets possible moves for King and possible captures"""
        p = np.array([pos, pos, pos, pos, pos, pos, pos, pos])
        boo = [True, True, True, True, True, True, True, True]
        p += [(1, 1), (1, -1), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        for n in range(8):
            if tuple(p[n]) not in locations and boo[n]:
                self.tiles.append(tuple(p[n]))
            elif boo[n] and self.col != locations[tuple(p[n])].col:
                self.capture.append(tuple(p[n]))
                boo[n] = False
            else:
                boo[n] = False


pawn_w = Pawn("Pieces/WhitePawn.png", 'w')
pawn_b = Pawn("Pieces/BlackPawn.png", 'b')
knight_w = Knight("Pieces/WhiteKNight.png", 'w')
knight_b = Knight("Pieces/BlackKnight.png", 'b')
bishop_w = Bishop("Pieces/WhiteBishop.png", 'w')
bishop_b = Bishop("Pieces/BlackBishop.png", 'b')
rook_w = Rook("Pieces/WhiteRook.png", 'w')
rook_b = Rook("Pieces/BlackRook.png", 'b')
queen_w = Queen("Pieces/WhiteQueen.png", 'w')
queen_b = Queen("Pieces/BlackQueen.png", 'b')
king_w = King("Pieces/WhiteKing.png", 'w')
king_b = King("Pieces/BlackKing.png", 'b')

piecesDic = {(0, 6): pawn_w,
          (1, 6): pawn_w,
          (2, 6): pawn_w,
          (3, 6): pawn_w,
          (4, 6): pawn_w,
          (5, 6): pawn_w,
          (6, 6): pawn_w,
          (7, 6): pawn_w,

          (0, 1): pawn_b,
          (1, 1): pawn_b,
          (2, 1): pawn_b,
          (3, 1): pawn_b,
          (4, 1): pawn_b,
          (5, 1): pawn_b,
          (6, 1): pawn_b,
          (7, 1): pawn_b,

          (0, 7): rook_w,
          (7, 7): rook_w,

          (1, 7): knight_w,
          (6, 7): knight_w,

          (2, 7): bishop_w,
          (5, 7): bishop_w,

          (3, 7): queen_w,
          (4, 7): king_w,

          (0, 0): rook_b,
          (7, 0): rook_b,

          (1, 0): knight_b,
          (6, 0): knight_b,

          (2, 0): bishop_b,
          (5, 0): bishop_b,

          (3, 0): queen_b,
          (4, 0): king_b,
          }

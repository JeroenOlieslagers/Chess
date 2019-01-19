import pygame

# Init
pygame.init()

display_width = 640
display_height = 640
green = (118, 150, 86)
dark_green = (185, 200, 69)
cream = (238, 238, 210)
yellow = (246, 246, 130)
light_grey = (191, 191, 168)
dark_grey = (94, 120, 69)
dark_red = (255, 0, 0)
blue = (80, 184, 231)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Chess')
clock = pygame.time.Clock()
finished = False
clicked = False
sound = True
turn = 'w'
FPS = 60
gl_mov = []
re = []

pawn_w = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/WhitePawn.png")
pawn_b = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/BlackPawn.png")
knight_w = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/WhiteKNight.png")
knight_b = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/BlackKnight.png")
bishop_w = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/WhiteBishop.png")
bishop_b = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/BlackBishop.png")
rook_w = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/WhiteRook.png")
rook_b = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/BlackRook.png")
queen_w = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/WhiteQueen.png")
queen_b = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/BlackQueen.png")
king_w = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/WhiteKing.png")
king_b = pygame.image.load("C:/Users/Admin/PycharmProjects/GUI/Pieces/BlackKing.png")

move = pygame.mixer.Sound("C:/Users/Admin/PycharmProjects/GUI/Pieces/move.wav")
check = pygame.mixer.Sound("C:/Users/Admin/PycharmProjects/GUI/Pieces/check.wav")
error = pygame.mixer.Sound("C:/Users/Admin/PycharmProjects/GUI/Pieces/error.wav")
take = pygame.mixer.Sound("C:/Users/Admin/PycharmProjects/GUI/Pieces/take.wav")

pieces = {(0, 480): pawn_w,
          (80, 480): pawn_w,
          (160, 480): pawn_w,
          (240, 480): pawn_w,
          (320, 480): pawn_w,
          (400, 480): pawn_w,
          (480, 480): pawn_w,
          (560, 480): pawn_w,

          (0, 80): pawn_b,
          (80, 80): pawn_b,
          (160, 80): pawn_b,
          (240, 80): pawn_b,
          (320, 80): pawn_b,
          (400, 80): pawn_b,
          (480, 80): pawn_b,
          (560, 80): pawn_b,

          (0, 560): rook_w,
          (560, 560): rook_w,

          (80, 560): knight_w,
          (480, 560): knight_w,

          (160, 560): bishop_w,
          (400, 560): bishop_w,

          (240, 560): queen_w,
          (320, 560): king_w,

          (0, 0): rook_b,
          (560, 0): rook_b,

          (80, 0): knight_b,
          (480, 0): knight_b,

          (160, 0): bishop_b,
          (400, 0): bishop_b,

          (240, 0): queen_b,
          (320, 0): king_b,
          }

white_pieces = [pawn_w, knight_w, bishop_w, rook_w, queen_w, king_w]

size = 80


def colour(piece):
    if piece in white_pieces:
        return 'w'
    else:
        return 'b'


def lanes(x, y, pieces, col='w'):
    px = x
    py = y
    qx = x
    qy = y
    p = True
    q = True
    r = True
    s = True
    tiles = []
    capture = []
    for n in range(8):
        px += size
        py += size
        qx -= size
        qy -= size
        if (px, y) not in pieces and p:
            tiles.append((px, y))
        elif p and col != colour(pieces[(px, y)]):
            capture.append((px, y))
            p = False
        else:
            p = False
        if (qx, y) not in pieces and q:
            tiles.append((qx, y))
        elif q and col != colour(pieces[(qx, y)]):
            capture.append((qx, y))
            q = False
        else:
            q = False
        if (x, py) not in pieces and r:
            tiles.append((x, py))
        elif r and col != colour(pieces[(x, py)]):
            capture.append((x, py))
            r = False
        else:
            r = False
        if (x, qy) not in pieces and s:
            tiles.append((x, qy))
        elif s and col != colour(pieces[(x, qy)]):
            capture.append((x, qy))
            s = False
        else:
            s = False
    return tiles, capture


def diagonals(x, y, pieces, col='w'):
    px = x
    py = y
    qx = x
    qy = y
    rx = x
    ry = y
    sx = x
    sy = y
    p = True
    q = True
    r = True
    s = True
    tiles = []
    capture = []
    for n in range(8):
        px += size
        py += size
        qx += size
        qy -= size
        rx -= size
        ry -= size
        sx -= size
        sy += size
        if (px, py) not in pieces and p:
            tiles.append((px, py))
        elif p and col != colour(pieces[(px, py)]):
            capture.append((px, py))
            p = False
        else:
            p = False
        if (qx, qy) not in pieces and q:
            tiles.append((qx, qy))
        elif q and col != colour(pieces[(qx, qy)]):
            capture.append((qx, qy))
            q = False
        else:
            q = False
        if (rx, ry) not in pieces and r:
            tiles.append((rx, ry))
        elif r and col != colour(pieces[(rx, ry)]):
            capture.append((rx, ry))
            r = False
        else:
            r = False
        if (sx, sy) not in pieces and s:
            tiles.append((sx, sy))
        elif s and col != colour(pieces[(sx, sy)]):
            capture.append((sx, sy))
            s = False
        else:
            s = False
    return tiles, capture


def adj(x, y, pieces, col='w'):
    px = x - 2 * size
    py = y - 2 * size
    tiles = []
    capture = []
    for n in range(3):
        px += size
        for m in range(3):
            py += size
            if (px, py) in pieces:
                if col != colour(pieces[(px, py)]):
                    capture.append((px, py))
            else:
                tiles.append((px, py))
        py = y - 2 * size
    return tiles, capture


def horsey(x, y, pieces, col='w'):
    px = x
    py = y + 3 * size
    qx = x
    qy = y - 3 * size
    tiles = []
    capture = []
    for n in range(2):
        px += size
        py -= size
        qx -= size
        qy += size
        if (px, py) in pieces:
            if col != colour(pieces[(px, py)]):
                capture.append((px, py))
        else:
            tiles.append((px, py))
        if (px, qy) in pieces:
            if col != colour(pieces[(px, qy)]):
                capture.append((px, qy))
        else:
            tiles.append((px, qy))
        if (qx, py) in pieces:
            if col != colour(pieces[(qx, py)]):
                capture.append((qx, py))
        else:
            tiles.append((qx, py))
        if (qx, qy) in pieces:
            if col != colour(pieces[(qx, qy)]):
                capture.append((qx, qy))
        else:
            tiles.append((qx, qy))
    return tiles, capture


def pawn(x, y, pieces, col='w'):
    if col == 'w':
        a = 1
    else:
        a = -1
    tiles = []
    capture = []
    if (x + size, y - a * size) in pieces and col != colour(pieces[(x + size, y - a * size)]):
        capture.append((x + size, y - a * size))
    if (x - size, y - a * size) in pieces and col != colour(pieces[(x - size, y - a * size)]):
        capture.append((x - size, y - a * size))
    if y == 280 + 200 * a:
        if (x, y - a * size) not in pieces:
            if (x, y - 2 * a * size) not in pieces:
                tiles.append((x, y - 2 * a * size))
            tiles.append((x, y - a * size))
    else:
        if (x, y - a * size) not in pieces:
            tiles.append((x, y - a * size))
    return tiles, capture


def moves(pos, piece, pieces, col='w'):
    if piece == pawn_w or piece == pawn_b:
        poss, cap = pawn(pos[0], pos[1], pieces, col=col)
    if piece == bishop_w or piece == bishop_b:
        poss, cap = diagonals(pos[0], pos[1], pieces, col=col)
    if piece == knight_w or piece == knight_b:
        poss, cap = horsey(pos[0], pos[1], pieces, col=col)
    if piece == rook_w or piece == rook_b:
        poss, cap = lanes(pos[0], pos[1], pieces, col=col)
    if piece == queen_w or piece == queen_b:
        poss, cap = lanes(pos[0], pos[1], pieces, col=col)
        poss += (diagonals(pos[0], pos[1], pieces, col=col))[0]
        cap += (diagonals(pos[0], pos[1], pieces, col=col))[1]
    if piece == king_w or piece == king_b:
        poss, cap = adj(pos[0], pos[1], pieces, col=col)

    return poss, cap


def draw_bg(x, y, pieces, highlight=False, circles=False, red=False, blu=False):
    replace_piece = False
    if (x, y) in pieces:
        replace_piece = True
    if not highlight and not circles and not red and not blu:
        if x/size % 2 == 0 and y/size % 2 == 1:
            pygame.draw.rect(gameDisplay, green, (x, y, size, size))
        elif x/size % 2 == 1 and y/size % 2 == 0:
            pygame.draw.rect(gameDisplay, green, (x, y, size, size))
        else:
            pygame.draw.rect(gameDisplay, cream, (x, y, size, size))
    elif highlight:
        if x/size % 2 == 0 and y/size % 2 == 1:
            pygame.draw.rect(gameDisplay, dark_green, (x, y, size, size))
        elif x/size % 2 == 1 and y/size % 2 == 0:
            pygame.draw.rect(gameDisplay, dark_green, (x, y, size, size))
        else:
            pygame.draw.rect(gameDisplay, yellow, (x, y, size, size))
    elif red:
        if x/size % 2 == 0 and y/size % 2 == 1:
            pygame.draw.rect(gameDisplay, dark_red, (x, y, size, size))
        elif x/size % 2 == 1 and y/size % 2 == 0:
            pygame.draw.rect(gameDisplay, dark_red, (x, y, size, size))
        else:
            pygame.draw.rect(gameDisplay, dark_red, (x, y, size, size))
    elif blu:
        if x/size % 2 == 0 and y/size % 2 == 1:
            pygame.draw.rect(gameDisplay, blue, (x, y, size, size))
        elif x/size % 2 == 1 and y/size % 2 == 0:
            pygame.draw.rect(gameDisplay, blue, (x, y, size, size))
        else:
            pygame.draw.rect(gameDisplay, blue, (x, y, size, size))
    elif circles:
        if x/size % 2 == 0 and y/size % 2 == 1:
            pygame.draw.circle(gameDisplay, dark_grey, (x + int(size/2), y + int(size/2)), int(size/6))
        elif x/size % 2 == 1 and y/size % 2 == 0:
            pygame.draw.circle(gameDisplay, dark_grey, (x + int(size / 2), y + int(size / 2)), int(size / 6))
        else:
            pygame.draw.circle(gameDisplay, light_grey, (x + int(size / 2), y + int(size / 2)), int(size / 6))
    if replace_piece:
        gameDisplay.blit(pieces[(x, y)], (x, y))


def in_square(x1, y1, x2, y2):
    return x2 < x1 < (x2 + size) and y2 < y1 < (y2 + size)


for i in range(8):
    for j in range(8):
        draw_bg(i * size, j * size, pieces)


for pos, piece in pieces.items():
    gameDisplay.blit(piece, pos)

while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if clicked:
                for item in gl_mov:
                    draw_bg(item[0], item[1], pieces)
                draw_bg(gl_pos[0], gl_pos[1], pieces)
                if gl_pos in re:
                    draw_bg(gl_pos[0], gl_pos[1], pieces, red=True)
                gameDisplay.blit(gl_piece, gl_pos)
                for pos in gl_mov:
                    if in_square(x, y, pos[0], pos[1]):
                        if pos in pieces:
                            take.play()
                        else:
                            move.play()
                        del pieces[gl_pos]
                        pieces[pos] = gl_piece
                        draw_bg(gl_pos[0], gl_pos[1], pieces)
                        draw_bg(pos[0], pos[1], pieces)
                        gameDisplay.blit(gl_piece, pos)
                        for item in re:
                            draw_bg(item[0], item[1], pieces)
                        re = []
                        try:
                            for cap in moves(pos, gl_piece, pieces, col=turn)[1]:
                                draw_bg(cap[0], cap[1], pieces, red=True)
                                re.append(cap)
                                if pieces[cap] == king_w or pieces[cap] == king_b:
                                    check.play()
                                    draw_bg(cap[0], cap[1], pieces, blu=True)
                        except ValueError:
                            pass
                        if turn == 'w':
                            turn = 'b'
                        else:
                            turn = 'w'
                        sound = False
                        break
                if sound:
                    error.play()
                else:
                    sound = True
                clicked = False
            else:
                for pos, piece in pieces.items():
                    if in_square(x, y, pos[0], pos[1]) and colour(piece) == turn:
                        gl_mov = []
                        gl_piece = None
                        draw_bg(pos[0], pos[1], pieces, highlight=True)
                        gameDisplay.blit(piece, pos)
                        for poss in moves(pos, piece, pieces, col=turn)[0]:
                            draw_bg(poss[0], poss[1], pieces, circles=True)
                            gl_mov.append(poss)
                        try:
                            for cap in moves(pos, piece, pieces, col=turn)[1]:
                                draw_bg(cap[0], cap[1], pieces, red=True)
                                gl_mov.append(cap)
                        except ValueError:
                            pass
                        gl_piece = piece
                        gl_pos = pos
                        clicked = True
                        break
        pygame.display.update()
        clock.tick(FPS)
pygame.quit()


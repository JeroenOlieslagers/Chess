import tkinter as tk
from tkinter import CURRENT


class Window:
    def __init__(self, size):
        self.size = size
        self.win = tk.Tk()
        self.win.size()
        self.win.resizable(False, False)
        self.canvas = tk.Canvas(self.win, width=self.size, height=self.size)
        self.canvas.pack()
        self.unit = 0

    def title(self, title):
        self.win.title(title)

    def addGrid(self, lines):
        self.unit = self.size / lines
        for i in range(lines):
            for j in range(lines):
                if i % 2 == 0 and j % 2 == 1:
                    self.canvas.create_rectangle(i * self.unit, j * self.unit, (i + 1) * self.unit, (j + 1) * self.unit,
                                                 fill='green')
                if i % 2 == 1 and j % 2 == 0:
                    self.canvas.create_rectangle(i * self.unit, j * self.unit, (i + 1) * self.unit, (j + 1) * self.unit,
                                                 fill='green')

    def addPiece(self, *pieces):
        for piece in pieces:
            self.canvas.create_image((piece.x + 0.5) * self.unit, (piece.y + 0.5) * self.unit, image=piece.image,
                                     tags=piece.tags)


class Piece:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tags = ("piece",)


class Pawn(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y)
        self.tags += ("pawn",)


class Bishop(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y)
        self.tags += ("bishop",)


class Knight(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y)
        self.tags += ("knight",)


class Rook(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y)
        self.tags += ("rook",)


class Queen(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y)
        self.tags += ("queen",)


class King(Piece):
    def __init__(self, x, y):
        Piece.__init__(self, x, y)
        self.tags += ("king",)


class PawnW(Pawn):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/pawn.png")
        Pawn.__init__(self, x, y)
        self.tags += ("w",)


class PawnB(Pawn):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/pawn_b.png")
        Pawn.__init__(self, x, y)
        self.tags += ("b",)


class BishopW(Bishop):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/bishop_w.png")
        Bishop.__init__(self, x, y)
        self.tags += ("w",)


class BishopB(Bishop):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/bishop_b.png")
        Bishop.__init__(self, x, y)
        self.tags += ("b",)


class KnightW(Knight):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/knight_w.png")
        Knight.__init__(self, x, y)
        self.tags += ("w",)


class KnightB(Knight):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/knight_b.png")
        Knight.__init__(self, x, y)
        self.tags += ("b",)


class RookW(Rook):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/rook_w.png")
        Rook.__init__(self, x, y)
        self.tags += ("w",)


class RookB(Rook):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/rook_b.png")
        Rook.__init__(self, x, y)
        self.tags += ("b",)


class QueenW(Queen):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/queen_w.png")
        Queen.__init__(self, x, y)
        self.tags += ("w",)


class QueenB(Queen):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/queen_b.png")
        Queen.__init__(self, x, y)


class KingW(King):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/king_w.png")
        King.__init__(self, x, y)
        self.tags += ("w",)


class KingB(King):
    def __init__(self, x, y):
        self.image = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/GUI/Pieces/king_b.png")
        King.__init__(self, x, y)


win = Window(800)
win.addGrid(8)

ls = []
for i in range(8):
    if i == 0 or i == 7:
        c = RookB(i, 0)
        d = RookW(i, 7)
    if i == 1 or i == 6:
        c = KnightB(i, 0)
        d = KnightW(i, 7)
    if i == 2 or i == 5:
        c = BishopB(i, 0)
        d = BishopW(i, 7)
    if i == 3:
        c = QueenB(i, 0)
        d = QueenW(i, 7)
    if i == 4:
        c = KingB(i, 0)
        d = KingW(i, 7)
    a = PawnB(i, 1)
    b = PawnW(i, 6)
    ls.extend([a, b, c, d])

win.addPiece(*ls)


def move(event):
    if win.canvas.find_withtag(CURRENT):
        win.canvas.coords(CURRENT, )


win.canvas.tag_bind("pawn", "<1>", move)



win.win.mainloop()




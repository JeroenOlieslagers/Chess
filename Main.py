from classes import *
from init import *

# Initialising pygame environment
pygame.init()
gameDisplay = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption('Chess')

# Setting up board
board = Board(gameDisplay, LENGTH)
controller = Controller(board)
board.draw()

board.draw_starting_pieces()
move = pygame.mixer.Sound("Pieces/move.wav")
check = pygame.mixer.Sound("Pieces/check.wav")
error = pygame.mixer.Sound("Pieces/error.wav")
take = pygame.mixer.Sound("Pieces/take.wav")
board.sounds['move'] = move
board.sounds['take'] = take
board.sounds['error'] = error
board.sounds['check'] = check
# Actual game loop
while not controller.finished:
    # If  window closed, exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            controller.finished = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            global_coords = event.pos
            local_coords = controller.coords(global_coords)
            controller.click(event)
    # Renderer update
    pygame.display.update()
pygame.quit()

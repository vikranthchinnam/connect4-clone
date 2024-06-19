import numpy as np
import pygame
import sys
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board,  piece):

    # check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
            
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    
    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# def score_position(board, piece):
#     ## Score Horizontal
#     for r in range(ROW_COUNT):
#         row_array = [int(i) for i in list(board[r,:])]
#         for c in range(COLUMN_COUNT - 3):
#             window=row_array[c:c+4]


def setup_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, ((c*SQUARESIZE), r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            
            



def print_board(board):
    print(np.flip(board, 0))

board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
setup_board()
myfont = pygame.font.SysFont("monospace", 75)
pygame.display.update()

turn = random.randint(PLAYER, AI)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            posx = event.pos[0]
            col = int(math.floor(posx/SQUARESIZE))
            # Ask for Player 1 Input
            if turn == PLAYER:

                if is_valid_location(board, col):
                    row = get_next_open_row(board=board, col=col)
                    drop_piece(board, row, col, PLAYER_PIECE)
                    if winning_move(board, PLAYER_PIECE):
                        #print("PLAYER 1 WINS!!!!! Congrats!!!")
                        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                        label = myfont.render("Player 1 wins!!", 1 , RED)
                        screen.blit(label, (30, 10))
                        game_over = True
                    turn += 1
                    turn = turn % 2
                    draw_board(board=board)
                        
        
        if turn == AI and not game_over:
            
            col = random.randint(0, COLUMN_COUNT-1)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board=board, col=col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    #print("PLAYER 2 WINS!!!!! Congrats!!!")
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    label = myfont.render("Player 2 wins!!", 1 , YELLOW)
                    screen.blit(label, (30, 10))
                    game_over = True
                        
                turn += 1
                turn = turn % 2
                draw_board(board=board)
        if game_over:
            pygame.time.wait(3000)




    

    



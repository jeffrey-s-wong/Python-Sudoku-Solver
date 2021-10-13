from pandas import *
import pygame as pg
import grid


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500

COLOR_BG = pg.Color(40, 42, 54)  # dark grey
FONT = pg.font.SysFont('Monospace', 80)

pg.init()
window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
canvas = window.get_size()
BOARD_LOCATION = (int(canvas[0]*0.05), int(canvas[1]*0.2))
pg.display.set_caption('Sudoku Solver')
clock = pg.time.Clock()

# initiate sudoku board
empty_board = [[[[0 for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

def fill_board(arr: list, board):
    split = []
    for fig in range(0, len(arr), 3):
        triplet = arr[fig: fig + 3]
        split.append(triplet)
    for mat in range(3):
        for row in range(3):
            for col in range(3):
                board[mat][row][col] = split[mat * 9 + row * 3 + col]
    return board


def main(board):
    frame = grid.Frame()
    sample_grid = grid.Grid(board, BOARD_LOCATION)
    start_button = grid.Button((int(canvas[0]*0.25), int(canvas[1]*0.1)), 'SOLVE', int(canvas[0]*0.0375), COLOR_BG, grid.COLOR_THICK_BORDER, action=1)
    reset_button = grid.Button((int(canvas[0]*0.5), int(canvas[1]*0.1)), 'RESET', int(canvas[0]*0.0375), COLOR_BG, grid.COLOR_THICK_BORDER, action=0)
    quit_button = grid.Button((int(canvas[0]*0.75), int(canvas[1]*0.1)), 'QUIT', int(canvas[0]*0.0375), COLOR_BG, grid.COLOR_THICK_BORDER, action=-1)
    buttons = [start_button, reset_button, quit_button]

    # game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            window.fill(COLOR_BG)
            sample_grid.handle_event(event)
            for i in buttons:
                i.draw(window)
                if i.handle_event(pg.mouse.get_pos(), event) == -1:
                    running = False
                elif i.handle_event(pg.mouse.get_pos(), event) == 0:
                    sample_grid.reset_board()
                elif i.handle_event(pg.mouse.get_pos(), event) == 1:
                    sample_grid.fix_board()
                    result = sample_grid.solve(0)
                    if result[0]:
                        end(1, result[1])
                    else:
                        end(0, result[1])
            window.blit(frame.surf, BOARD_LOCATION)
            pg.display.flip()
            clock.tick(30)
    pg.quit()


def end(result, result_grid):
    frame = grid.Frame()
    reset_button = grid.Button((133, 50), 'RESET', 18, COLOR_BG, grid.COLOR_THICK_BORDER, action=0)
    quit_button = grid.Button((267, 50), 'QUIT', 18, COLOR_BG, grid.COLOR_THICK_BORDER, action=-1)
    buttons = [reset_button, quit_button]
    font = pg.font.Font("Helvetica.ttc", 18, bold=True)
    end_text = font.render('', True, grid.GREEN)

    # game loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            window.fill(COLOR_BG)
            result_grid.handle_event(event)
            for i in buttons:
                i.draw(window)
                if i.handle_event(pg.mouse.get_pos(), event) == -1:
                    running = False
                elif i.handle_event(pg.mouse.get_pos(), event) == 0:
                    result_grid.reset_board()
                    main(empty_board)
            if result == 1:
                end_text = font.render('The sudoku is solved.', True, grid.GREEN)
            elif result == 0:
                end_text = font.render('The sudoku cannot be solved.', True, grid.RED)
            txt_rect = end_text.get_rect(center=(200, 90))
            window.blit(end_text, txt_rect)
            window.blit(frame.surf, BOARD_LOCATION)
            pg.display.flip()
            clock.tick(30)
    pg.quit()


main(empty_board)

import pygame as pg
import pygame.font

pg.init()
pg.font.init()
FONT = pg.font.SysFont('Monospace', 40)
BOARD_LOCATION = (20, 100)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
COLOR_CELL = pg.Color(40, 42, 54)  # dark grey
COLOR_ACTIVE_CELL = pg.Color(68, 71, 90)  # light grey
COLOR_THICK_BORDER = pg.Color(248, 248, 242)
COLOR_CELL_BORDER = pg.Color(98, 114, 164)
WHITE = pg.Color(255, 255, 255)
RED = pg.Color(255, 85, 85)
GREEN = pg.Color(80, 250, 123)
COLOR_DRAFT = pg.Color(169, 181, 219)
CELL_SIDE = 40


num_dict = {pg.K_1: '1', pg.K_2: '2', pg.K_3: '3', pg.K_4: '4', pg.K_5: '5', pg.K_6: '6', pg.K_7: '7', pg.K_8: '8',
            pg.K_9: '9'}

window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)


# find the next cell, or the previous
def get_next_cell(mat, row, col, unit, direction=1):
    digit = [(3 ** i) for i in range(3, -1, -1)]
    pos = sum([mat, row, col, unit][i] * digit[i] for i in range(len(digit)))
    if direction == 1 and pos == 80:
        return [0, 0, 0, 0]
    elif direction == -1 and pos == 0:
        return [2, 2, 2, 2]
    pos += direction
    return to_ter(pos, 4)


def to_ter(dec, digits):
    ter = []
    while dec > 0:
        ter.append(dec % 3)
        dec //= 3
    while len(ter) < digits:
        ter.append(0)
    ter.reverse()
    return ter


def to_dec(ter: list):
    length = len(ter)
    digit = [(3 ** i) for i in range(length - 1, -1, -1)]
    return sum(ter[i] * digit[i] for i in range(length))


# looping through all the cells
def iterate():
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    yield i, j, k, l


class NumCell:
    def __init__(self, x, y, num='0'):
        self.Rect = pg.Rect(x, y, CELL_SIDE, CELL_SIDE)
        self.bg_color = COLOR_CELL
        self.num = num
        self.num_color = WHITE
        self.active = False
        self.fixed = True
        self.wrong = False
        self.completed = False

    def __str__(self):
        return (f'{self.__class__.__name__}('
           f'{self.num!r}, {self.completed!r})')

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.Rect.collidepoint(event.pos):  # if the clicked point is within the rect
                self.active = True
            else:
                self.active = False
            if self.active:
                self.bg_color = COLOR_ACTIVE_CELL
            else:
                self.bg_color = COLOR_CELL
            self.set_num_surface()
        self.set_num_surface()

    # different behaviours of the numbers shown in cell in different situations
    def set_num_surface(self):
        if self.num == '0' or len(self.num) > 1:
            self.num_surface = FONT.render('', True, self.num_color)
        else:
            if self.wrong:
                self.num_surface = FONT.render(self.num, True, RED)
            elif self.completed:
                self.num_surface = FONT.render(self.num, True, GREEN)
            else:
                if self.fixed:
                    self.num_surface = FONT.render(self.num, True, self.num_color)
                else:
                    self.num_surface = FONT.render(self.num, True, COLOR_DRAFT)

    def draw(self, screen):
        # fill the cell
        pg.draw.rect(screen, self.bg_color, self.Rect, 0)
        # draw border
        pg.draw.rect(screen, COLOR_CELL_BORDER, self.Rect, 1)
        # blit them
        screen.blit(self.num_surface, (self.Rect.x + CELL_SIDE / 6, self.Rect.y))


class Grid:
    def __init__(self, board, starting_coordinates=(0, 0)):
        self.x_start = starting_coordinates[0]
        self.y_start = starting_coordinates[1]
        self.board = board
        self.cell_grid = [[[['0' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        self.build_grid(board)

    def build_grid(self, board):
        for i, j, k, l in iterate():
            self.board[i][j][k][l] = NumCell((k * 3 + l) * CELL_SIDE + 5 + BOARD_LOCATION[0],
                                             (i * 3 + j) * CELL_SIDE + 5 + BOARD_LOCATION[1],
                                             str(board[i][j][k][l]))

    def reset_board(self):
        for i, j, k, l in iterate():
            self.board[i][j][k][l].num = '0'
            self.board[i][j][k][l].set_num_surface()

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i, j, k, l in iterate():
                if self.board[i][j][k][l].Rect.collidepoint(event.pos):
                    self.board[i][j][k][l].active = True
        elif event.type == pg.KEYDOWN:
            for i, j, k, l in iterate():
                if self.board[i][j][k][l].active:
                    if event.key == pg.K_RETURN:
                        print(str(self.board[i][j][k][l].num))
                    elif event.key in [pg.K_BACKSPACE, pg.K_DELETE, pg.K_SPACE, pg.K_ESCAPE]:
                        self.board[i][j][k][l].num = ''
                    elif event.key in num_dict:
                        self.board[i][j][k][l].num = num_dict[event.key]
                        self.board[i][j][k][l].active = False
                        self.board[i][j][k][l].bg_color = COLOR_CELL
                        next_cell = self.board[get_next_cell(i, j, k, l)[0]][get_next_cell(i, j, k, l)[1]][
                            get_next_cell(i, j, k, l)[2]][get_next_cell(i, j, k, l)[3]]
                        next_cell.active = True
                        next_cell.bg_color = COLOR_ACTIVE_CELL
                    elif event.key == pg.K_0:
                        self.board[i][j][k][l].num = '0'
                        self.board[i][j][k][l].active = False
                        self.board[i][j][k][l].bg_color = COLOR_CELL
                        next_cell = self.board[get_next_cell(i, j, k, l, 1)[0]][get_next_cell(i, j, k, l, 1)[1]][
                            get_next_cell(i, j, k, l, 1)[2]][get_next_cell(i, j, k, l, 1)[3]]
                        next_cell.active = True
                        next_cell.bg_color = COLOR_ACTIVE_CELL
                    elif event.key == pg.K_UP:
                        self.board[i][j][k][l].active = False
                        self.board[i][j][k][l].bg_color = COLOR_CELL
                        if i == 0 and j == 0:
                            next_cell = self.board[2][2][k][l]
                        else:
                            next_cell = \
                                self.board[to_ter(to_dec([i, j]) - 1, 2)[0]][to_ter(to_dec([i, j]) - 1, 2)[1]][k][l]
                        next_cell.active = True
                        next_cell.bg_color = COLOR_ACTIVE_CELL
                    elif event.key == pg.K_DOWN:
                        self.board[i][j][k][l].active = False
                        self.board[i][j][k][l].bg_color = COLOR_CELL
                        if i == 2 and j == 2:
                            next_cell = self.board[0][0][k][l]
                        else:
                            next_cell = \
                                self.board[to_ter(to_dec([i, j]) + 1, 2)[0]][to_ter(to_dec([i, j]) + 1, 2)[1]][k][l]
                        next_cell.active = True
                        next_cell.bg_color = COLOR_ACTIVE_CELL
                    elif event.key == pg.K_LEFT:
                        self.board[i][j][k][l].active = False
                        self.board[i][j][k][l].bg_color = COLOR_CELL
                        next_cell = self.board[get_next_cell(i, j, k, l, -1)[0]][get_next_cell(i, j, k, l, -1)[1]][
                            get_next_cell(i, j, k, l, -1)[2]][get_next_cell(i, j, k, l, -1)[3]]
                        next_cell.active = True
                        next_cell.bg_color = COLOR_ACTIVE_CELL
                    elif event.key == pg.K_RIGHT:
                        self.board[i][j][k][l].active = False
                        self.board[i][j][k][l].bg_color = COLOR_CELL
                        next_cell = self.board[get_next_cell(i, j, k, l, 1)[0]][get_next_cell(i, j, k, l, 1)[1]][
                            get_next_cell(i, j, k, l, 1)[2]][get_next_cell(i, j, k, l, 1)[3]]
                        next_cell.active = True
                        next_cell.bg_color = COLOR_ACTIVE_CELL
                    break
                else:
                    continue
        else:
            pass
        self.update_grid(event)

    def update_grid(self, event):
        for i, j, k, l in iterate():
            self.board[i][j][k][l].handle_event(event)
            self.board[i][j][k][l].draw(window)

    # all inputted numbers will be in different colour from the fixed numbers
    def fix_board(self):
        for i, j, k, l in iterate():
            if len(self.board[i][j][k][l].num )> 1:
                self.board[i][j][k][l].num = '0'
                self.board[i][j][k][l].fixed = False
                self.board[i][j][k][l].num_color = COLOR_DRAFT
            elif self.board[i][j][k][l].num == '0':
                self.board[i][j][k][l].fixed = False
                self.board[i][j][k][l].num_color = COLOR_DRAFT
            else:
                self.board[i][j][k][l].fixed = True
            self.board[i][j][k][l].set_num_surface()

    def solve(self, pos):
        # if all 81 cells are solved
        if pos >= 81:
            for i, j, k, l in iterate():
                if not self.board[i][j][k][l].fixed:
                    self.board[i][j][k][l].completed = True
            return [True, self]
        for i, j, k, l in iterate():
            # calculate the number of cells solved
            pos = i * 27 + j * 9 + k * 3 + l
            # only solve blank cells
            if self.board[i][j][k][l].num == '0':
                # check horizontal
                horizontal = []
                for col in range(3):
                    for unit in range(3):
                        horizontal.append(self.board[i][j][col][unit].num)
                # check vertical
                vertical = []
                for mat in range(3):
                    for row in range(3):
                        vertical.append(self.board[mat][row][k][l].num)
                # check own 3x3 grid
                mini_grid = []
                for row in range(3):
                    for unit in range(3):
                        mini_grid.append(self.board[i][row][k][unit].num)
                # try figure from 1-9
                for n in range(1, 10):
                    self.board[i][j][k][l].num = str(n)
                    self.board[i][j][k][l].set_num_surface()
                    # validate the inputted number
                    if (str(n) in horizontal) or (str(n) in vertical) or (str(n) in mini_grid):
                        self.board[i][j][k][l].wrong = True
                        self.board[i][j][k][l].set_num_surface()
                        self.board[i][j][k][l].wrong = False
                        self.board[i][j][k][l].num = '0'
                    else:
                        # recurring the function if passed validation
                        if self.solve(pos + 1)[0]:
                            return [True, self]
                        # backtrack if failed
                        self.board[i][j][k][l].num = '0'
                        self.board[i][j][k][l].set_num_surface()
                return [False, self]


# draw frame border for the 9 matrices
class Frame(pg.sprite.Sprite):
    def __init__(self):
        super(Frame, self).__init__()
        self.surf = pg.Surface((CELL_SIDE * 9 + 5, CELL_SIDE * 9 + 5))
        self.surf.fill((0, 0, 0))
        self.surf.set_colorkey((0, 0, 0))
        for x in range(3):
            for y in range(3):
                pg.draw.rect(self.surf, COLOR_THICK_BORDER,
                             (3 * x * CELL_SIDE + 3, 3 * y * CELL_SIDE + 3, CELL_SIDE * 3, CELL_SIDE * 3), 3)
        self.rect = self.surf.get_rect()


# draw start button
class Button(pg.sprite.Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        self.mouse_over = False
        self.action = action
        self.font = pygame.font.Font("Helvetica.ttc", font_size, bold=True, underline=True)
        self.large_font = pygame.font.Font("Helvetica.ttc", int(font_size * 1.2), bold=True, underline=True)
        default_img = self.font.render(text, True, text_rgb, bg_rgb)
        highlight_img = self.large_font.render(text, True, text_rgb, COLOR_ACTIVE_CELL)
        self.images = [default_img, highlight_img]
        self.rects = [default_img.get_rect(center=center_position),
                      highlight_img.get_rect(center=center_position)]
        super().__init__()

    @property
    def image(self):
        if self.mouse_over:
            return self.images[1]
        else:
            return self.images[0]

    @property
    def rect(self):
        if self.mouse_over:
            return self.rects[1]
        else:
            return self.rects[0]

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def handle_event(self, mouse_pos, event):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if event.type == pg.MOUSEBUTTONUP:
                if self.action == 0:
                    return 0
                elif self.action == -1:
                    return -1
                elif self.action == 1:
                    return 1
        else:
            self.mouse_over = False

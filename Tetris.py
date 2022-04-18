import pygame
import random
import time
import sys

pygame.init()

# GLOBALS VARS
s_width = 600
s_height = 620
play_width = 250  # meaning 250 // 10 = 25 width per block
play_height = 500  # meaning 500 // 20 = 25 height per block
block_size = 25


top_left_x = s_width//7
top_left_y = s_height - play_height - 20

# SHAPE FORMATS

S = [['11111',
      '11111',
      '11001',
      '10011',
      '11111'],
     ['11111',
      '11011',
      '11001',
      '11101',
      '11111']]

Z = [['11111',
      '11111',
      '10011',
      '11001',
      '11111'],
     ['11111',
      '11011',
      '10011',
      '10111',
      '11111']]

I = [['11011',
      '11011',
      '11011',
      '11011',
      '11111'],
     ['11111',
      '00001',
      '11111',
      '11111',
      '11111']]

O = [['11111',
      '11111',
      '10011',
      '10011',
      '11111']]

J = [['11111',
      '10111',
      '10001',
      '11111',
      '11111'],
     ['11111',
      '11001',
      '11011',
      '11011',
      '11111'],
     ['11111',
      '11111',
      '10001',
      '11101',
      '11111'],
     ['11111',
      '11011',
      '11011',
      '10011',
      '11111']]

L = [['11111',
      '11101',
      '10001',
      '11111',
      '11111'],
     ['11111',
      '11011',
      '11011',
      '11001',
      '11111'],
     ['11111',
      '11111',
      '10001',
      '10111',
      '11111'],
     ['11111',
      '10011',
      '11011',
      '11011',
      '11111']]

T = [['11111',
      '11011',
      '10001',
      '11111',
      '11111'],
     ['11111',
      '11011',
      '11001',
      '11011',
      '11111'],
     ['11111',
      '11111',
      '10001',
      '11011',
      '11111'],
     ['11111',
      '11011',
      '10011',
      '11011',
      '11111']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(255,100,10), (220, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (85, 255, 85)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy+ i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.Font('fonts/Hi Jack.ttf', 30)
    label = font.render('NEXT SHAPE - ', 1, (255,255,255))

    sx = play_width + 120
    sy = play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface, grid, score=0):
    surface.fill((0, 0, 0))

    pygame.init()
    font = pygame.font.Font('fonts/Hi Jack.ttf', 60)
    label = font.render('Tetris', True, (0, 255, 0))

    surface.blit(label, (s_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.Font('fonts/Hi Jack.ttf', 30)
    label = font.render('Score -  ' + str(score), True, (255, 255, 255))
    surface.blit(label, (play_width + 150, play_height / 2 + 100))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    

def main(win):  # *
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            font = pygame.font.Font("fonts/Hi Jack.ttf", 80)
            label = font.render("YOU LOST!", True, (255, 255, 255))
            win.blit(label, (s_width / 2 - label.get_width() / 2, s_height / 2 - label.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            # main_menu(win)


def main_menu(window):
    x = 0
    run = True
    while run:

        window.fill((0, 0, 0))
        window.blit(background, (0, 0))
        font1 = pygame.font.Font("fonts/Platinum Sign.ttf", 50)
        font2 = pygame.font.Font("fonts/EA_font.ttf", 50)

        if x > 70:
            time.sleep(1)
            label = font2.render('PRESS  SPACE', True, (0, 200, 0))
            window.blit(label, (s_width / 2 - label.get_width() / 2, s_height / 2 - label.get_height() / 2))
            label = font2.render('To  Begin', True, (0, 200, 0))
            window.blit(label, (s_width / 2 - label.get_width() / 2, s_height / 2 + label.get_height() / 2))

        else:
            x += 1

        label = font1.render('TETRIS', True, (255, 255, 255))
        window.blit(label, (s_width / 2 - label.get_width() / 2, x))
        pygame.draw.line(window, (255, 255, 255), (s_width / 2 - label.get_width() / 2, x + 100),
                         (s_width / 2 + label.get_width() / 2, x + 100), width=5)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main(win)


def intro(screen):
    clock = pygame.time.Clock()
    font1 = pygame.font.Font('fonts/Hi Jack.ttf', 60)
    font2 = pygame.font.Font('fonts/Hi Jack.ttf', 40)

    rendered_text_1 = font1.render("Vaibhav Games", True, (255, 0, 0))
    rendered_text_2 = font1.render("   Production", True, (255, 0, 0))
    rendered_text_3 = font2.render("    Presents...", True, (255, 0, 0))
    text_rect_1 = rendered_text_1.get_rect(center=(300, 270))
    text_rect_2 = rendered_text_1.get_rect(center=(300, 320))
    text_rect_3 = rendered_text_1.get_rect(center=(360, 390))


    ST_FADEIN = 0
    ST_FADEOUT = 1

    state = ST_FADEIN
    last_state_change = time.time()
    x = 0


    while x < 510:
        x += 1
        # Update the state
        state_time = time.time() - last_state_change

        if state == ST_FADEIN:
            if state_time >= FADE_IN_TIME:
                state = ST_FADEOUT
                state_time -= FADE_IN_TIME
                last_state_change = time.time() - state_time

        elif state == ST_FADEOUT:
            if state_time >= FADE_OUT_TIME:
                state = ST_FADEIN
                state_time -= FADE_OUT_TIME
                last_state_change = time.time() - state_time

        else:
            break

        if state == ST_FADEIN:
            alpha = FADE_IN_EASING(1.0 * state_time / FADE_IN_TIME)
            rt1 = rendered_text_1
            rt2 = rendered_text_2
            rt3 = rendered_text_3
        elif state == ST_FADEOUT:
            alpha = 1. - FADE_OUT_EASING(1.0 * state_time / FADE_OUT_TIME)
            rt1 = rendered_text_1
            rt2 = rendered_text_2
            rt3 = rendered_text_3
        else:
            break

        surf2 = pygame.surface.Surface((text_rect_1.width, text_rect_1.height))
        surf2.set_alpha(255 * alpha)
        surf3 = pygame.surface.Surface((text_rect_2.width, text_rect_1.height))
        surf3.set_alpha(255 * alpha)
        surf4 = pygame.surface.Surface((text_rect_3.width, text_rect_1.height))
        surf4.set_alpha(255 * alpha)

        screen.fill((0, 0, 0))
        surf2.blit(rt1, (0, 0))
        surf3.blit(rt2, (0, 0))
        surf4.blit(rt3, (0, 0))
        screen.blit(surf2, text_rect_1)
        screen.blit(surf3, text_rect_2)
        screen.blit(surf4, text_rect_3)

        pygame.display.flip()
        clock.tick(50)
    return True

FADE_IN_TIME = 5
FADE_OUT_TIME = 5
FADE_IN_EASING = lambda x: x  # Linear
FADE_OUT_EASING = lambda x: x  # Linear

if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('TETRIS')
    icon = pygame.image.load('images/tetris.ico')
    pygame.display.set_icon(icon) 
    background = pygame.image.load('images/back.png')
    background = pygame.transform.scale(background, (s_width,s_height)) 

    n = intro(win)
    if n:
        main_menu(win)

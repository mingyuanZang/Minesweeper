import sys
import time
from enum import Enum
import pygame
from pygame.locals import *
from Block import *

SCREEN_WIDTH = BLOCK_WIDTH * SIZE
SCREEN_HEIGHT = (BLOCK_HEIGHT + 2) * SIZE

class GameStatus(Enum):
    ready = 1,
    start = 2,
    died = 3,
    win = 4

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    mainText = font.render(text, True, fcolor)
    screen.blit(mainText, (x, y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Minesweeper')

    scoreFont = pygame.font.Font('images/a.TTF', SIZE*2)
    fwidth, fheight = scoreFont.size('999')
    red = (200, 40, 40)

    #load the images & proper scaling needed
    img0 = pygame.image.load('images/0.bmp').convert()
    img0 = pygame.transform.smoothscale(img0, (SIZE, SIZE))
    img1 = pygame.image.load('images/1.bmp').convert()
    img1 = pygame.transform.smoothscale(img1, (SIZE, SIZE))
    img2 = pygame.image.load('images/2.bmp').convert()
    img2 = pygame.transform.smoothscale(img2, (SIZE, SIZE))
    img3 = pygame.image.load('images/3.bmp').convert()
    img3 = pygame.transform.smoothscale(img3, (SIZE, SIZE))
    img4 = pygame.image.load('images/4.bmp').convert()
    img4 = pygame.transform.smoothscale(img4, (SIZE, SIZE))
    img5 = pygame.image.load('images/5.bmp').convert()
    img5 = pygame.transform.smoothscale(img5, (SIZE, SIZE))
    img6 = pygame.image.load('images/6.bmp').convert()
    img6 = pygame.transform.smoothscale(img6, (SIZE, SIZE))
    img7 = pygame.image.load('images/7.bmp').convert()
    img7 = pygame.transform.smoothscale(img7, (SIZE, SIZE))
    img8 = pygame.image.load('images/8.bmp').convert()
    img8 = pygame.transform.smoothscale(img8, (SIZE, SIZE))
    img_blank = pygame.image.load('images/blank.bmp').convert()
    img_blank = pygame.transform.smoothscale(img_blank, (SIZE, SIZE))
    img_flag = pygame.image.load('images/flag.bmp').convert()
    img_flag = pygame.transform.smoothscale(img_flag, (SIZE, SIZE))
    img_marker = pygame.image.load('images/marker.bmp').convert()
    img_marker = pygame.transform.smoothscale(img_marker, (SIZE, SIZE))
    img_mine = pygame.image.load('images/mine.bmp').convert()
    img_mine = pygame.transform.smoothscale(img_mine, (SIZE, SIZE))
    img_blood = pygame.image.load('images/blood.bmp').convert()
    img_blood = pygame.transform.smoothscale(img_blood, (SIZE, SIZE))
    img_error = pygame.image.load('images/error.bmp').convert()
    img_error = pygame.transform.smoothscale(img_error, (SIZE, SIZE))
    emoji_size = int(SIZE * 1.25)
    img_emoji_fail = pygame.image.load('images/emoji_fail.bmp').convert()
    img_emoji_fail = pygame.transform.smoothscale(img_emoji_fail, (emoji_size, emoji_size))
    img_emoji_normal = pygame.image.load('images/emoji_normal.bmp').convert()
    img_emoji_normal = pygame.transform.smoothscale(img_emoji_normal, (emoji_size, emoji_size))
    img_emoji_success = pygame.image.load('images/emoji_success.bmp').convert()
    img_emoji_success = pygame.transform.smoothscale(img_emoji_success, (emoji_size, emoji_size))
    emoji_pos_x = (SCREEN_WIDTH - emoji_size) // 2
    emoji_pos_y = (SIZE * 2 - emoji_size) // 2

    img_dict = {
        0: img0,
        1: img1,
        2: img2,
        3: img3,
        4: img4,
        5: img5,
        6: img6,
        7: img7,
        8: img8
    }

    bgColor = (225, 225, 225)

    block = MineBlock()
    game_status = GameStatus.ready
    start_time = None
    elapsed_time = 0

    while True:
        screen.fill(bgColor)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                x = mouse_x // SIZE
                y = mouse_y // SIZE - 2
                b1, b2, b3 = pygame.mouse.get_pressed()
                if game_status == GameStatus.start:
                    if b1 and b3:           # both buttons are clicked
                        mine = block.getmine(x, y)
                        if mine.status == BlockStatus.clicked:
                            if not block.double_mouse_down(x, y):
                                game_status = GameStatus.died
            elif event.type == MOUSEBUTTONUP:
                if y < 0:
                    if emoji_pos_x <= mouse_x <= emoji_pos_x + emoji_size \
                            and emoji_pos_y <= mouse_y <= emoji_pos_y + emoji_size:
                        game_status = GameStatus.ready
                        block = MineBlock()
                        start_time = time.time()
                        elapsed_time = 0
                        continue

                if game_status == GameStatus.ready:
                    game_status = GameStatus.start
                    start_time = time.time()
                    elapsed_time = 0

                if game_status == GameStatus.start:
                    mine = block.getmine(x, y)
                    if b1 and not b3:       # left button of the mouse is clicked
                        if mine.status == BlockStatus.unclick:
                            if not block.click_mine(x, y):
                                game_status = GameStatus.died
                    elif not b1 and b3:     # right button of the mouse is clicked
                        if mine.status == BlockStatus.unclick:
                            mine.status = BlockStatus.flaged
                        elif mine.status == BlockStatus.flaged:
                            mine.status = BlockStatus.marked
                        elif mine.status == BlockStatus.marked:
                            mine.status = BlockStatus.unclick
                    elif b1 and b3:
                        if mine.status == BlockStatus.doubled:
                            block.double_mouse_up(x, y)

        flag_count = 0
        clicked_count = 0

        for row in block.block:
            for mine in row:
                position = (mine.x * SIZE, (mine.y + 2) * SIZE)
                if mine.status == BlockStatus.clicked:
                    screen.blit(img_dict[mine.number_mines_around], position)
                    clicked_count += 1
                elif mine.status == BlockStatus.doubled:
                    screen.blit(img_dict[mine.number_mines_around], position)
                elif mine.status == BlockStatus.bomb:
                    screen.blit(img_blood, position)
                elif mine.status == BlockStatus.flaged:
                    screen.blit(img_flag, position)
                    flag_count += 1
                elif mine.status == BlockStatus.marked:
                    screen.blit(img_marker, position)
                elif mine.status == BlockStatus.hint:
                    screen.blit(img0, position)
                elif game_status == GameStatus.died and mine.value:
                    screen.blit(img_mine, position)
                elif mine.value == 0 and mine.status == BlockStatus.flaged:
                    screen.blit(img_error, position)
                elif mine.status == BlockStatus.unclick:
                    screen.blit(img_blank, position)

        print_text(screen, scoreFont, 30, (SIZE * 2 - fheight) // 2 - 2, '%02d' % (MINE_COUNT - flag_count), red)
        if game_status == GameStatus.start:
            elapsed_time = int(time.time() - start_time)
        print_text(screen, scoreFont, SCREEN_WIDTH - fwidth - 30, (SIZE * 2 - fheight) // 2 - 2, '%03d' % elapsed_time, red)

        if flag_count + clicked_count == BLOCK_WIDTH * BLOCK_HEIGHT:
            game_status = GameStatus.win

        if game_status == GameStatus.died:
            screen.blit(img_emoji_fail, (emoji_pos_x, emoji_pos_y))
        elif game_status == GameStatus.win:
            screen.blit(img_emoji_success, (emoji_pos_x, emoji_pos_y))
        else:
            screen.blit(img_emoji_normal, (emoji_pos_x, emoji_pos_y))

        pygame.display.update()


if __name__ == '__main__':
    main()   

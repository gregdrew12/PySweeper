import os, sys
import pygame
import random
import numpy as np
from pygame.locals import *

if not pygame.font: print('Warning, fonts disabled')
if not pygame.mixer: print('Warning, sound disabled')

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Cannot load sound:', fullname)
        raise SystemExit(message)
    return sound

def det_num(matrix, x, y):
    mine_count = 0

    if matrix[y][x] == 1: return -1

    if y > 0:
        if matrix[y-1][x] == 1: mine_count+=1
    if y > 0 and x < len(matrix[0])-1:
        if matrix[y-1][x+1] == 1: mine_count+=1
    if x < len(matrix[0])-1:
        if matrix[y][x+1] == 1: mine_count+=1
    if y < len(matrix)-1 and x < len(matrix[0])-1:
        if matrix[y+1][x+1] == 1: mine_count+=1
    if y < len(matrix)-1:
        if matrix[y+1][x] == 1: mine_count+=1
    if y < len(matrix)-1 and x > 0:
        if matrix[y+1][x-1] == 1: mine_count+=1
    if x > 0:
        if matrix[y][x-1] == 1: mine_count+=1
    if y > 0 and x > 0:
        if matrix[y-1][x-1] == 1: mine_count+=1

    return mine_count

def neighbors(tile1, tile2):
    t1x = tile1.x
    t1y = tile1.y
    t2x = tile2.x
    t2y = tile2.y

    if t1x == t2x and t1y-1 == t2y: return 1
    elif t1x-1 == t2x and t1y-1 == t2y: return 1
    elif t1x-1 == t2x and t1y == t2y: return 1
    elif t1x-1 == t2x and t1y+1 == t2y: return 1
    elif t1x == t2x and t1y+1 == t2y: return 1
    elif t1x+1 == t2x and t1y+1 == t2y: return 1
    elif t1x+1 == t2x and t1y == t2y: return 1
    elif t1x+1 == t2x and t1y-1 == t2y: return 1
    elif t1x == t2x and t1y == t2y: return 1
    else: return 0

class NumTileList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def insert(self, tile):
        if self.head == None:
            self.head = tile
        else:
            self.tail.next = tile
            tile.prev = self.tail
        self.tail = tile
        self.count += 1

    def all_tiles_clicked(self):
        cur = self.head
        clicked_count = 0
        while cur != None:
            if cur.clicked:
                clicked_count += 1
            cur = cur.next
        if clicked_count == self.count: return 1
        else: return 0

class NumTile(pygame.sprite.Sprite):
    def __init__(self, num, x, y):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_hidden.png')
        screen = pygame.display.get_surface()
        
        self.num = num
        self.prev = None
        self.next = None
        self.x = x
        self.y = y
        self.xpos = x*22
        self.ypos = y*22
        self.rect.topleft = self.xpos, self.ypos
        self.clicked = 0
        self.flagged = 0
        self.revealed = 0
        self.win = 0
        

    def update(self):
        if self.clicked:
            if self.num == 0:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_empty.png')
            elif self.num == 1:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_one.png')
            elif self.num == 2:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_two.png')
            elif self.num == 3:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_three.png')
            elif self.num == 4:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_four.png')
            elif self.num == 5:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_five.png')
            elif self.num == 6:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_six.png')
            elif self.num == 7:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_seven.png')
            else:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_eight.png')
            screen = pygame.display.get_surface()
            self.rect.topleft = self.xpos, self.ypos
            self.revealed = 1

    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.clicked = 1
            if self.num == 0:
                cur = self
                while cur.prev != None: cur = cur.prev
                self.zero_clicked(cur)
        return 0

    def zero_clicked(self, start):
        if self.num == 0:
            cur = start
            while cur != None:
                if neighbors(self, cur) and not cur.clicked:
                    cur.clicked = 1
                    cur.zero_clicked(start)
                cur = cur.next

    def check_flag(self, mouse):
        if self.rect.collidepoint(mouse):
            if not self.revealed:
                if self.flagged:
                    self.flagged = 0
                    self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_hidden.png')
                    screen = pygame.display.get_surface()
                    self.rect.topleft = self.xpos, self.ypos
                else:
                    self.flagged = 1
                    self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_flag.png')
                    screen = pygame.display.get_surface()
                    self.rect.topleft = self.xpos, self.ypos

class MineTile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_hidden.png')
        screen = pygame.display.get_surface()
        
        self.num = -1
        self.x = x
        self.y = y
        self.xpos = x*22
        self.ypos = y*22
        self.rect.topleft = self.xpos, self.ypos
        self.clicked = 0
        self.flagged = 0
        self.revealed = 0
        self.win = 0
        

    def update(self):
        if self.clicked:
            self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_mine_explode.png')
            screen = pygame.display.get_surface()
            self.rect.topleft = self.xpos, self.ypos
            self.revealed = 1
        if self.win:
                self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_flag_win.png')
                screen = pygame.display.get_surface()
                self.rect.topleft = self.xpos, self.ypos


    def check_click(self, mouse):
        if self.rect.collidepoint(mouse):
            self.clicked = 1
            return 1
        else: return 0

    def check_flag(self, mouse):
        if self.rect.collidepoint(mouse):
            if not self.revealed:
                if self.flagged:
                    self.flagged = 0
                    self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_hidden.png')
                    screen = pygame.display.get_surface()
                    self.rect.topleft = self.xpos, self.ypos
                else:
                    self.flagged = 1
                    self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_flag.png')
                    screen = pygame.display.get_surface()
                    self.rect.topleft = self.xpos, self.ypos

    def other_mine_clicked(self):
        self.image, self.rect = load_image(r'C:\Users\gregd\OneDrive\Desktop\PySweeper\tile_mine.png')
        screen = pygame.display.get_surface()
        self.rect.topleft = self.xpos, self.ypos
            

pygame.init()

while 1:
    difficulty = input("Choose a difficulty!\nBeginner: 9x9 with 10 mines\nIntermediate: 16x16 with 40 mines\nExpert: 30x16 with 99 mines\n").lower()
    if difficulty == "beginner" or difficulty == "intermediate" or difficulty == "expert": break
    print("Invalid difficulty, please try again!")

board_x = 0
board_y = 0
num_mines = 0

if difficulty == "beginner":
    board_x = 9
    board_y = 9
    num_mines = 10
elif difficulty == "intermediate":
    board_x = 16
    board_y = 16
    num_mines = 40
else:
    board_x = 30
    board_y = 16
    num_mines = 99

pixels_width = (board_x*22)-2
pixels_height = (board_y*22)-2
screen = pygame.display.set_mode((pixels_width, pixels_height))
pygame.display.set_caption("PySweeper")
pygame.mouse.set_visible(1)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((116, 116, 116, 1))

screen.blit(background, (0, 0))
pygame.display.flip()

board_size = board_x * board_y
mine_field = np.full(num_mines, 1)
mine_field = np.pad(mine_field, (0, board_size-num_mines), 'constant')
random.shuffle(mine_field)
mine_field = mine_field.reshape(board_y, board_x)
print(mine_field)
print()

allsprites = pygame.sprite.RenderUpdates()
ntl = NumTileList()
for i in range(board_y):
    for j in range(board_x):
        if mine_field[i][j] == 0:
            tile_num = det_num(mine_field, j, i)
            tile = NumTile(tile_num, j, i)
            allsprites.add(tile)
            ntl.insert(tile)
        elif mine_field[i][j] == 1:
            allsprites.add(MineTile(j, i))
clock = pygame.time.Clock()

running = 1
game_over = 0
game_win = 0
game_start = 0

while running:
    clock.tick(60)

    if game_start:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = 0
            elif game_win:
                for t in allsprites: t.win = 1
            elif event.type == MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    for t in allsprites:
                        game_over = game_over | t.check_click(event.pos)
                    if ntl.all_tiles_clicked():
                        game_over = 1
                        game_win = 1
                        for k in allsprites:
                            if isinstance(k, MineTile):
                                if not k.flagged: k.flagged = 1
                elif event.button == 3:
                    for t in allsprites:
                        t.check_flag(event.pos)
    else:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = 0
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clickedx = 0
                    clickedy = 0
                    clickednum = 0
                    for t in allsprites:
                        t.check_click(event.pos)
                        if t.clicked == 1:
                            clickedx = t.x
                            clickedy = t.y
                            clickednum = t.num
                            break
                    if clickednum != 0:
                        hit = 0
                        while not hit:
                            mine_field = mine_field.flatten()
                            random.shuffle(mine_field)
                            mine_field = mine_field.reshape(board_y, board_x)
                            if det_num(mine_field, clickedx, clickedy) == 0: hit = 1
                        print(mine_field)
                        allsprites = pygame.sprite.RenderUpdates()
                        ntl = NumTileList()
                        for i in range(board_y):
                            for j in range(board_x):
                                if mine_field[i][j] == 0:
                                    tile_num = det_num(mine_field, j, i)
                                    tile = NumTile(tile_num, j, i)
                                    allsprites.add(tile)
                                    ntl.insert(tile)
                                elif mine_field[i][j] == 1:
                                    allsprites.add(MineTile(j, i))
                        for k in allsprites:
                            k.check_click(event.pos)
                    game_start = 1
    
    allsprites.update()

    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()
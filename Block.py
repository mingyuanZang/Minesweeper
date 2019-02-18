import random
from enum import Enum

BLOCK_WIDTH = 30
BLOCK_HEIGHT = 16
SIZE = 20
MINE_COUNT = 99

class BlockStatus(Enum):
    unclick = 1
    clicked = 2
    mine = 3
    flaged = 4
    marked = 5
    bomb = 6
    hint = 7
    doubled = 8


class Mine:
    def __init__(self, x, y, value=0):
        self._x = x
        self._y = y
        self._value = 0
        self._number_mines_around = -1
        self._status = BlockStatus.unclick
        self.setvalue(value)

    def __repr__(self):
        return str(self._value)

    def getx(self):
        return self._x

    def setx(self, x):
        self._x = x

    x = property(getx, setx)

    def gety(self):
        return self._y

    def sety(self, y):
        self._y = y

    y = property(gety, sety)

    def getvalue(self):
        return self._value

    def setvalue(self, value):
        if value:
            self._value = 1
        else:
            self._value = 0

    value = property(getvalue, setvalue, "0: no mine 1: mine here")

    def get_number_mines_around(self):
        return self._number_mines_around

    def set_number_mines_around(self, number_mines_around):
        self._number_mines_around = number_mines_around

    number_mines_around = property(get_number_mines_around, set_number_mines_around, "number of mines around here") 

    def getstatus(self):
        return self._status

    def setstatus(self, value):
        self._status = value

    status = property(getstatus, setstatus, "block status")

class MineBlock:
    def __init__(self):
        self._block = [[Mine(i, j) for i in range(BLOCK_WIDTH)] for j in range(BLOCK_HEIGHT)]

        #bury the mines
        for i in random.sample(range(BLOCK_WIDTH * BLOCK_HEIGHT), MINE_COUNT):
            self._block[i // BLOCK_WIDTH][i % BLOCK_WIDTH].value = 1

    def getblock(self):
        return self._block

    block = property(fget=getblock)

    def getmine(self, x, y):
        return self._block[y][x]

    def click_mine(self, x, y):
        #a mine is clicked
        if self._block[y][x].value:
            self._block[y][x].status = BlockStatus.bomb
            return False

        self._block[y][x].status = BlockStatus.clicked #change the status to be clicked

        around = _get_around(x, y)

        _sum = 0
        for i, j in around:
            if self._block[j][i].value:
                _sum += 1
        self._block[y][x].number_mines_around = _sum

        #scenario: when click  single clock, a large area of blocks clicked
        #if there's no mine around, iterate the 8 unclicked blocks aroung this block
        if _sum == 0:
            for i, j in around:
                if self._block[j][i].number_mines_around == -1:
                    self.click_mine(i, j)

        return True

    def double_mouse_down(self, x, y):
        if self._block[y][x].number_mines_around == 0:
            return True

        self._block[y][x].status = BlockStatus.doubled

        around = _get_around(x, y)
            
        flag_sum = 0 #number of flaged mine
        for i,j in _get_around(x, y):
            if self._block[j][i].status == BlockStatus.flaged:
                flag_sum += 1
        result = True

        if flag_sum == self._block[y][x].number_mines_around:
            for i, j in around:
                if self._block[j][i].status == BlockStatus.unclick:
                    if not self.open_mine(i, j):
                        result = False
        else:
            for i, j in around:
                if self._block[j][i].status == BlockStatus.unclick:
                    self._block[j][i].status = BlockStatus.hint
        return result

    def double_mouse_up(self, x, y):
        self._block[y][x].status = BlockStatus.clicked
        for i, j in _get_around(x, y):
            if self._block[j][i].status == BlockStatus.hint:
                self._block[j][i].status = BlockStatus.unclick

def _get_around(x, y):
    """return coordinates around (x, y)"""
    return [(i, j) for i in range(max(0, x - 1), min(BLOCK_WIDTH - 1, x + 1) + 1)
            for j in range(max(0, y - 1), min(BLOCK_HEIGHT - 1, y + 1) + 1) if i != x or j != y]


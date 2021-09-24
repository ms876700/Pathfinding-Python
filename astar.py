import pygame, sys, random, math
from tkinter import Tk
import os
import time

# -----------------------------------color define-----------------------------------------
red = (178, 34, 34)
orange = (255, 110, 0)
lightblue = (30, 144, 255)
blue = (25, 25, 112)
pink = (255, 105, 180)
black = (0, 0, 0)
aqua = (32, 178, 170)
white = (220, 220, 220)
green = (0,255,0)

# --------------------------------------------------------------------------------------------
# number between 2 - 200
sizeofarr = 20
showgrid = 1
if sizeofarr >= 150:
    showgrid = 0  # only 1 or 0
# --------------------------------------------------------------------------------------------
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 30)
root = Tk()
root.title("Start Window")

screen_width = root.winfo_screenwidth() - 50  # screen window width
screen_height = root.winfo_screenheight() - 100  # screen window height

screen_height = screen_height - screen_height % sizeofarr
sizeof = screen_height // sizeofarr
screen_width = screen_width - screen_width % sizeof

# -----------------------------------------------------------------------------------------
height = screen_height
width = screen_width


size = (width, height + 30)

pygame.init()
pygame.display.set_caption("A* Path Finding")
win = pygame.display.set_mode(size)
clock = pygame.time.Clock()

rows = sizeofarr
cols = screen_width // sizeof

# ------------------------------------------------------------------------------------

grid = []
openSet, closeSet = [], []
path = []

w = width // cols
h = height // rows



class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        if random.randint(0, 100) < 15:
            self.wall = True

    def show(self, win, col):
        if self.wall:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x * w, self.y * h, w - 1, h - 1))

    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        # Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y + 1])
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x + 1][self.y - 1])
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x - 1][self.y + 1])
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x - 1][self.y - 1])


def clickWall(pos, state):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    grid[i][j].wall = state
    # print(grid[i][j].wall)


def place(pos):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    return i, j


def heuristics(a, b):
    return math.sqrt((a.x - b.x) ** 2 + abs(a.y - b.y) ** 2)


def displayMessage(message):  # message box
    fonts = pygame.font.SysFont('comicsans', 40)
    pygame.draw.rect(win, black, (0, screen_height, screen_width, 30))
    win.blit(fonts.render(message, True, white), (20, screen_height + 3))
    pygame.display.update()


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)


def close():
    pygame.quit()
    sys.exit()


def main():
    start_time = 0
    flag = False
    startflag = False
    start = None
    end = None
    run = True

    message = "Choose Start, End points and Press SPACE BAR to Start"

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed(3)[0]:
                    i, j = pygame.mouse.get_pos()
                    spot = grid[i // sizeof][j // sizeof]
                    if start not in openSet:
                        start = spot
                        openSet.append(start)

                    elif end is None and spot != start:
                        end = spot

                    elif spot != end and spot != start:
                        clickWall(pygame.mouse.get_pos(), True)

                elif pygame.mouse.get_pressed(3)[2]:
                    i, j = pygame.mouse.get_pos()
                    spot = grid[i // sizeof][j // sizeof]
                    if spot == start:
                        openSet.remove(start)
                        start = None
                    elif spot == end:
                        end = None
                    clickWall(pygame.mouse.get_pos(), False)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startflag = True
                    start_time = time.time()
                    message = "start = {},{} , End = {},{}".format(start.x, start.y, end.x, end.y)

        if startflag:
            if len(openSet) > 0:
                winner = 0
                for i in range(len(openSet)):
                    if openSet[i].f < openSet[winner].f:
                        winner = i

                current = openSet[winner]

                if current == end:
                    temp = current
                    while temp.prev:
                        path.append(temp.prev)
                        temp = temp.prev
                    if not flag:
                        flag = True

                        end_time = time.time()
                        sec = end_time - start_time
                        message = "start = {},{} , End = {},{} || Time = {:.2f}s,  Path = {},  Discovered = {}".format(start.x, start.y, end.x, end.y, sec , len(path), len(openSet)+len(closeSet))

                    # elif flag:
                    #     continue

                if flag == False:
                    openSet.remove(current)
                    closeSet.append(current)

                    for neighbor in current.neighbors:
                        if neighbor in closeSet or neighbor.wall:
                            continue
                        tempG = current.g + 1

                        newPath = False
                        if neighbor in openSet:
                            if tempG < neighbor.g:
                                neighbor.g = tempG
                                newPath = True
                        else:
                            neighbor.g = tempG
                            newPath = True
                            openSet.append(neighbor)

                        if newPath:
                            neighbor.h = heuristics(neighbor, end)
                            neighbor.f = neighbor.g + neighbor.h
                            neighbor.prev = current

            else:
                message = "No Solution"
                # run = False


        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, white)
                if flag and spot in path:
                    spot.show(win, green)
                elif spot in closeSet:
                    spot.show(win, red)
                elif spot in openSet:
                    spot.show(win, lightblue)

                if spot == start:
                    spot.show(win, orange)
                if spot == end:
                    spot.show(win, pink)

        displayMessage(message)
        pygame.display.update()


main()

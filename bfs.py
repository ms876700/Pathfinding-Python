import pygame, sys, random
from collections import deque
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
width = screen_width
height = screen_height

size = (width, height + 30)

pygame.init()
pygame.display.set_caption('Breadth First Search')
win = pygame.display.set_mode(size)
clock = pygame.time.Clock()

rows = sizeofarr
cols = screen_width // sizeof

# ------------------------------------------------------------------------------------



grid = []
queue, visited = deque(), []
path = []

class Spot:
    def __init__(self, i, j):
        self.x, self.y = i, j
        self.f, self.g, self.h = 0, 0, 0
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.visited = False
        # if random.randint(0, 100) < 20:
        #     self.wall = True
        
    def show(self, win, col):
        if self.wall == True:
            col = (0, 0, 0)
        pygame.draw.rect(win, col, (self.x*sizeof, self.y*sizeof, sizeof-1, sizeof-1))
    
    def add_neighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])



def clickWall(pos, state):
    i = pos[0] // sizeof
    j = pos[1] // sizeof
    grid[i][j].wall = state

def place(pos):
    i = pos[0] // sizeof
    j = pos[1] // sizeofarr
    return i,j

def displayMessage(message):  # message box
    fonts = pygame.font.SysFont('comicsans', 40)
    pygame.draw.rect(win, black, (0, screen_height, screen_width, 30))
    win.blit(fonts.render(message, True, white), (20, screen_height + 3))
    pygame.display.update()

def close():
    pygame.quit()
    sys.exit()


for i in range(cols):
    arr = []
    for j in range(rows):
        arr.append(Spot(i, j))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].add_neighbors(grid)

    
# start = grid[2][2]
# end = grid[20][10]
# start.wall = False
# end.wall = False
#
# queue.append(start)
# start.visited = True

def main():
    start_time = 0
    flag = False
    noflag = True
    startflag = False
    start = None
    end = None
    visitcount = 0


    message = "Choose Start, End points and Press SPACE BAR to Start"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed(3)[0]:
                    i, j = pygame.mouse.get_pos()
                    spot = grid[i // sizeof][j // sizeof]
                    if start not in queue:
                        start = spot
                        queue.append(start)
                    elif end is None and spot != start:
                        end = spot
                    elif spot != end and spot != start:
                        clickWall(pygame.mouse.get_pos(), True)

                elif pygame.mouse.get_pressed(3)[2]:
                    i, j = pygame.mouse.get_pos()
                    spot = grid[i // sizeof][j // sizeof]
                    if spot == start:
                        queue.remove(start)
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
            if len(queue) > 0:
                current = queue.popleft()
                if current == end:
                    run2 = True
                    temp = current
                    while temp.prev and run2:
                        path.append(temp.prev)
                        if temp == start:
                            run2 = False
                        temp = temp.prev

                    if not flag:
                        flag = True

                        end_time = time.time()
                        sec = end_time - start_time
                        message = "start = {},{} , End = {},{} || Time = {:.2f}s,  Path = {},  Discovered = {}".format(
                            start.x, start.y, end.x, end.y, sec, len(path),visitcount)

                    elif flag:
                        continue
                if not flag:
                    for i in current.neighbors:
                        if not i.visited and not i.wall:
                            i.visited = True
                            visitcount += 1
                            i.prev = current
                            queue.append(i)
            else:
                if noflag and not flag:
                    message = "No Solution"
                    noflag = False
                else:
                    continue


        win.fill((0, 20, 20))
        for i in range(cols):
            for j in range(rows):
                spot = grid[i][j]
                spot.show(win, white)
                if spot in path:
                    spot.show(win, green)
                elif spot.visited:
                    spot.show(win, red)
                if spot in queue:
                    spot.show(win, lightblue)
                if spot == start:
                    spot.show(win, orange)
                if spot == end:
                    spot.show(win, pink)

        displayMessage(message)
        pygame.display.flip()


main()

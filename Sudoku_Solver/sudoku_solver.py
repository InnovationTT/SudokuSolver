import curses
from curses import wrapper

import time

# perhaps bad practice to use global variable like this
colorgrid = [[1 for x in range(9)] for y in range(9)]

# print a grid
def print_grid(grid):
    for sl in grid:
        print(sl)
    print()

# get the subgrid for a given index pair
def get_subgrid(x, y, grid):
    startx = x//3*3
    starty = y//3*3
    return [row[starty:starty+3] for row in grid[startx:startx+3]]

# check if grid is valid after inserting number at given index
# valid IFF: inserting said number does not create a duplicate in that indice's row, col, and 3x3 subgrid
def check_grid_valid(num, x, y, grid):
    flag = True 

    for i in range(9):
        if num == grid[x][i] or num == grid[i][y]:
            flag = False
    
    if any(num in sl for sl in get_subgrid(x, y, grid)):
        flag = False

    #print(flag)
    return flag


# the main recursive solve function
def solve(screen, grid):
    

    x,y = -1, -1

    # check if there are unassigned boxes
    if any(0 in sl for sl in grid):

        # get index of unassigned box
        for sl2 in grid:
            if 0 in sl2:
                x = grid.index(sl2)
                y = sl2.index(0)
                if colorgrid[x][y] == 1:
                    colorgrid[x][y] = 3              
                break
        
        # recursively call the function for every valid number that can be assigned to the current unassigned box
        for i in range(1,10):
            if check_grid_valid(i, x, y, grid):
                grid[x][y] = i

                # the following code displays the grid as it is being worked on by the algorithm
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
                curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                # optional timer if we want to slow down the animation 
                time.sleep(0.25)     
                
                screen.clear()
                for sl in grid:
                    for item in sl:
                        screen.addstr(f"{item}  ", curses.color_pair(colorgrid[grid.index(sl)][sl.index(item)]))
                    screen.move(screen.getyx()[0]+1, 0)
                    screen.refresh()    

                
                # the recursive call. if any recursive calls return true (i.e. solved the entire grid), the process is finished
                if solve(screen, grid):
                    return True

                # if the recursive call failed to return true, then this branch has failed, revert this box to unassigned state
                grid[x][y] = 0
                colorgrid[x][y] = 2


        # if we reach this point, it means that this branch of recursive calls has reached a dead end (i.e. found an unassigned box with no valid assignable numbers)
        return False
    else:
        return True

def main(screen):
    grid1 = [[0, 0, 0, 0, 1, 0, 0, 0, 2],
            [9, 3, 0, 8, 0, 0, 0, 5, 0],
            [0, 0, 4, 0, 0, 0, 0, 0, 0],
            [6, 4, 0, 0, 0, 2, 0, 0, 5],
            [0, 0, 7, 6, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 4, 0],
            [5, 6, 0, 9, 0, 0, 0, 3, 0],
            [7, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 8, 9, 0, 0]]

    grid2 = [[5, 3, 0, 8, 0, 0, 6, 0, 0],
            [0, 4, 9, 5, 0, 2, 8, 3, 1],
            [0, 2, 7, 1, 0, 0, 5, 0, 9],
            [7, 5, 0, 9, 0, 1, 0, 0, 4],
            [2, 0, 8, 4, 0, 0, 0, 0, 6],
            [4, 0, 0, 0, 0, 8, 0, 0, 0],
            [0, 6, 0, 0, 0, 3, 4, 1, 0],
            [3, 0, 0, 0, 1, 0, 0, 2, 0],
            [1, 8, 0, 2, 0, 4, 0, 0, 0]]         

    # assign the solution grid to the grid we want to solve
    # note grid1 is considered very difficult by human standards, and will take a very long time until the program finishes if we want to see the visual process of the algorithm
    solGrid = grid1

    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    screen.clear()
    screen.addstr("Green numbers ", curses.color_pair(3))
    screen.addstr("are numbers that the algorithm tries. ")
    screen.addstr("Yellow numbers ", curses.color_pair(2))
    screen.addstr("indicate points at which the algorithm had to retrace back to. Press any key to start.")
    screen.refresh()
    screen.getch()

    if solve(screen, solGrid):
        print_grid(solGrid)
    else: 
        print("no solution")

wrapper(main)
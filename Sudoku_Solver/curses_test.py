import curses
from curses import wrapper

import time

def main(screen):

    delay = 5
    for i in range(delay):
        #screen.clear()
        screen.addstr(f"Time until program terminates: {delay-i}s")
        screen.move(screen.getyx()[0]+1, 0)
        screen.refresh()
        time.sleep(1)
    
    screen.refresh()
    screen.getch()
    
wrapper(main)
import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.addstr(10, 10, '+')
        screen.refresh()
        #screen.addstr(self.life.rows - 1, 0, '+')
        #screen.addstr(0, self.life.cols - 1, '+')
        #screen.addstr(self.life.rows - 1, self.life.cols - 1, '+')
        #for i in range(1, self.life.cols - 1):
         #   screen.addstr(0, i, '-')
          #  screen.addstr(self.life.rows - 1, i, '-')
        #for i in range(1, self.life.rows - 1):
         #   screen.addstr(i, 0, '|')
        #screen.addstr(i, self.life.cols - 1, '|')
        return
        # pass

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        pass

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.draw_borders(screen)
        time.sleep(5)
        curses.endwin()


life = GameOfLife((24, 80), max_generations=50)
ui = Console(life)
ui.run()

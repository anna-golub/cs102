import pathlib
import random

from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        res = []
        if row > 0:
            res.append(self.curr_generation[row - 1][col])
            if col > 0:
                res.append(self.curr_generation[row - 1][col - 1])
            if col < self.cols - 1:
                res.append(self.curr_generation[row - 1][col + 1])

        if row < self.rows - 1:
            res.append(self.curr_generation[row + 1][col])
            if col > 0:
                res.append(self.curr_generation[row + 1][col - 1])
            if col < self.cols - 1:
                res.append(self.curr_generation[row + 1][col + 1])

        if col > 0:
            res.append(self.curr_generation[row][col - 1])
        if col < self.cols - 1:
            res.append(self.curr_generation[row][col + 1])

        return res

    def get_next_generation(self) -> Grid:
        for i in range(self.rows):
            for j in range(self.cols):
                self.prev_generation[i][j] = self.curr_generation[i][j]

        alive = []
        dead = []

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = sum(self.get_neighbours((i, j)))
                if neighbours < 2 or neighbours > 3:
                    dead.append((i, j))
                elif neighbours == 3 and self.curr_generation[i][j] == 0:
                    alive.append((i, j))

        for t in alive:
            self.curr_generation[t[0]][t[1]] = 1
        for t in dead:
            self.curr_generation[t[0]][t[1]] = 0
        return self.curr_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.prev_generation[i][j] != self.curr_generation[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """

        with open(filename, 'r') as f:
            lines = f.readlines()
        rows = len(lines)
        cols = len(lines[0].strip())
        game = GameOfLife(size=(rows, cols), randomize=False)

        with open(filename, 'r') as f:
            for i in range(rows):
                lines[i].strip()
                for j in range(cols):
                    game.curr_generation[i][j] = int(lines[i][j])
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'w') as f:
            for row in self.curr_generation:
                f.write(''.join(str(v) for v in row) + '\n')
        return

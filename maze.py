from graphics import Cell
import time
import random


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r()
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for column_idx in range(self.__num_cols):
            column = []
            for row_idx in range(self.__num_rows):
                x1 = self.__x1 + (column_idx * self.__cell_size_x)
                x2 = x1 + self.__cell_size_x
                y1 = self.__y1 + (row_idx * self.__cell_size_y)
                y2 = y1 + self.__cell_size_y
                cell = Cell(x1, y1, x2, y2, self.__win)
                column.append(cell)
            self._cells.append(column)

        for column_idx in range(self.__num_cols):
            for row_idx in range(self.__num_rows):
                self._draw_cell(column_idx, row_idx)

    def _draw_cell(self, i, j):
        if self.__win is None:
            return
        self._cells[i][j].draw()
        self._animate()

    def _break_entrance_and_exit(self):
        if self.__win is None:
            return
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[self.__num_cols - 1][self.__num_rows - 1]

        attributes = ["has_top_wall", "has_right_wall", "has_bottom_wall"]
        for attr in attributes:
            setattr(entrance_cell, attr, False)

        attributes = ["has_top_wall", "has_left_wall", "has_bottom_wall"]
        for attr in attributes:
            setattr(exit_cell, attr, False)

        entrance_cell.draw("black")
        exit_cell.draw("black")
        self._animate()

    def _break_walls_r(self, i=0, j=0):
        self._cells[i][j].visited = True
        while True:
            next_visit = []
            # left cell
            if i > 0 and not self._cells[i - 1][j].visited:
                next_visit.append((i - 1, j))
            # top cell
            if j > 0 and not self._cells[i][j - 1].visited:
                next_visit.append((i, j - 1))
            # right cell
            if i < self.__num_cols - 1 and not self._cells[i + 1][j].visited:
                next_visit.append((i + 1, j))
            # bottom cell
            if j < self.__num_rows - 1 and not self._cells[i][j + 1].visited:
                next_visit.append((i, j + 1))

            if len(next_visit) == 0:
                self._draw_cell(i, j)
                return

            direction = random.randrange(len(next_visit))
            next_visit_cell = next_visit[direction]

            # right
            if next_visit_cell[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False

            # left
            if next_visit_cell[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            # down
            if next_visit_cell[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            # up
            if next_visit_cell[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_visit_cell[0], next_visit_cell[1])

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        self._solve_r()

    def _solve_r(self, i=0, j=0):
        self._animate()
        self._cells[i][j].visited = True

        if i == self.__num_cols - 1 and j == self.__num_rows - 1:
            return True

        # left cell
        if (
            i > 0
            and not self._cells[i - 1][j].visited
            and not self._cells[i - 1][j].has_right_wall
        ):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        # top cell
        if (
            j > 0
            and not self._cells[i][j - 1].visited
            and not self._cells[i][j - 1].has_bottom_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        # right cell
        if (
            i < self.__num_cols - 1
            and not self._cells[i + 1][j].visited
            and not self._cells[i + 1][j].has_left_wall
        ):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        # bottom cell
        if (
            j < self.__num_rows - 1
            and not self._cells[i][j + 1].visited
            and not self._cells[i][j + 1].has_top_wall
        ):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        return False

    def _animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.005)

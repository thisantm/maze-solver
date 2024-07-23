class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=fill_color,
            width=2,
        )


class Cell:
    def __init__(
        self,
        x1,
        y1,
        x2,
        y2,
        window,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited = False
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._win = window
        self.left_wall = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
        self.top_wall = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self.bottom_wall = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        self.right_wall = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))

    def draw(self, wall_color="white"):
        if self._win is None:
            return
        if self.has_left_wall:
            self._win.draw_line(self.left_wall, wall_color)
        else:
            self._win.draw_line(self.left_wall, "black")
        if self.has_top_wall:
            self._win.draw_line(self.top_wall, wall_color)
        else:
            self._win.draw_line(self.top_wall, "black")
        if self.has_bottom_wall:
            self._win.draw_line(self.bottom_wall, wall_color)
        else:
            self._win.draw_line(self.bottom_wall, "black")
        if self.has_right_wall:
            self._win.draw_line(self.right_wall, wall_color)
        else:
            self._win.draw_line(self.right_wall, "black")

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return

        middle_self_x = (self._x1 + self._x2) // 2
        middle_self_y = (self._y1 + self._y2) // 2
        middle_dst_x = (to_cell._x1 + to_cell._x2) // 2
        middle_dst_y = (to_cell._y1 + to_cell._y2) // 2
        move = Line(
            Point(middle_self_x, middle_self_y), Point(middle_dst_x, middle_dst_y)
        )
        if not undo:
            self._win.draw_line(move, "green")
            return
        self._win.draw_line(move, "red")

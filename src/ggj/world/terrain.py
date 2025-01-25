from curses import window
from ..drawing import shape as s

class Grass:
    def __init__(self, x: int, y: int, win: window):
        self.window = win
        self.pos = [x, y]

    def update(self):
        pass

    def draw(self):
        x, y = self.pos
        s.world_char(self.window, x, y, ';', s.GREEN)

    def get_pos(self) -> tuple[int, int]:
        return self.pos[0], self.pos[1]

    def zindex(self) -> int:
        return 0

    def impassable(self) -> bool:
        return False

class Boundary:
    def __init__(self, x: int, y: int, win: window):
        self.window = win
        self.pos = [x, y]

    def update(self):
        pass

    def draw(self):
        x, y = self.pos
        s.world_char(self.window, x, y, '♠', s.DARK_GREEN)

    def get_pos(self) -> tuple[int, int]:
        return self.pos[0], self.pos[1]

    def zindex(self) -> int:
        return 0

    def impassable(self) -> bool:
        return True

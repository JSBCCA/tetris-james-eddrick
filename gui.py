from core import *
import tkinter
import random
SCALE = 20


class Tetris:
    def __init__(self, parent):
        self.gameover = False
        self.blocks = 0
        self.parent = parent
        self.canvas = tkinter.Canvas(parent,
                                     width=WIDTH * SCALE,
                                     height=HEIGHT * SCALE,
                                     bg='white')
        self.canvas.pack()

        self.g = Grid([], ActiveBlock(WIDTH // 2, HEIGHT - 1, new_block()))

        self.parent.bind('<Left>', self.move_left)
        self.parent.bind('<Right>', self.move_right)
        self.parent.bind('<Up>', self.rotate)
        self.parent.bind('<Down>', self.drop)
        self.parent.bind('n', self.new_game)
        self.parent.bind('q', self.quit)
        self.parent.after(self.tick_rate(), self.keep_dropping)

    def tick_rate(self):
        return 300 - (self.blocks * 2)

    def quit(self, event):
        self.parent.destroy()

    def new_game(self, event):
        self.gameover = False
        self.g = Grid([], ActiveBlock(WIDTH // 2, HEIGHT - 1, new_block()))
        self.blocks = 0
        self.parent.after(self.tick_rate(), self.keep_dropping)

    def move_left(self, event):
        if not self.gameover:
            g = self.g.move('left')
            if g.is_valid():
                self.g = g
            self.draw()

    def move_right(self, event):
        if not self.gameover:
            g = self.g.move('right')
            if g.is_valid():
                self.g = g
            self.draw()

    def rotate(self, event):
        if not self.gameover:
            g = self.g.rotate()
            if g.is_valid():
                self.g = g
            self.draw()

    def drop(self, event):
        if not self.gameover:
            g = self.g.drop()
            if g.is_valid():
                self.g = g
            self.draw()

    def keep_dropping(self):
        g = self.g.drop()
        if g.is_valid():
            self.g = g
            self.parent.after(self.tick_rate(), self.keep_dropping)
        else:
            self.blocks += 1
            self.g = Grid(self.g.place_block().blocks,
                          ActiveBlock(WIDTH // 2, HEIGHT - 1, new_block()))
            self.g = self.g.clear_full_rows()
            if self.g.is_valid():
                self.parent.after(self.tick_rate(), self.keep_dropping)
            else:
                self.gameover = True
        self.draw()

    def draw(self):
        self.canvas.delete(tkinter.ALL)
        self._draw_stripes()
        self._draw_placed_blocks()
        self._draw_current_block()

    def _draw_stripes(self):
        for x in range(0, WIDTH * SCALE, 40):
            self.canvas.create_rectangle(5 + x,
                                         0,
                                         5 + x + SCALE // 2,
                                         HEIGHT * SCALE,
                                         fill='light grey',
                                         outline='white')

        gx = self.g.current_block.x * SCALE + SCALE // 5
        self.canvas.create_rectangle(5 + gx,
                                     0,
                                     5 + gx + SCALE // 10,
                                     HEIGHT * SCALE,
                                     fill='red2',
                                     outline='white')

    def _draw_placed_blocks(self):
        for b in self.g.blocks:
            for p in b.posns:
                self._draw_posn(p)

    def _draw_current_block(self):
        for px, py in self.g.current_block.block.posns:
            self._draw_posn(
                (self.g.current_block.x + px, self.g.current_block.y + py))

    def random_color(self):
        return random.choice(['red', 'blue', 'yellow', 'orange', 'purple',
                              'green', 'light blue', 'pink', 'brown'])

    def _draw_posn(self, p):
        x, y = p
        self.canvas.create_rectangle(
            5 + x * SCALE, (HEIGHT * SCALE) - (y * SCALE),
            5 + x * SCALE + SCALE // 2,
            (HEIGHT * SCALE) - (y * SCALE + SCALE // 2),
            fill=self.random_color())


if __name__ == '__main__':
    root = tkinter.Tk()
    tetris = Tetris(root)
    root.mainloop()

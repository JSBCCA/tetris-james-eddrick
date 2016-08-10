'''
Our model of Tetris will be a Grid.

A Grid contains the following elements:
    - A list of Blocks
    - The current Block
    - The current Block's position and orientation.

A Block is collection of occupied points.

An ActiveBlock is a block (oriented independent of the grid), with an x and y
coordinates.
'''
from collections import namedtuple
import random

HEIGHT = 40
WIDTH = 15

Block = namedtuple('Block', 'posns')
ActiveBlock = namedtuple('ActiveBlock', 'x y block')


class Grid:
    def __init__(self, blocks, current_block):
        self.blocks = blocks
        self.current_block = current_block

    def drop(self):
        ''' Grid -> Grid

        Returns a new grid with the current block dropped 1 row.
        '''
        x, y, block = self.current_block
        return Grid(self.blocks, ActiveBlock(x, y - 1, block))

    def move(self, dir):
        ''' (Grid, Direction) -> Grid

        Returns a new grid with the current blocked moved 1 column to the left
        or right. Returns None if an invalid Direction is provided.
        A Direction is either 'left' or 'right'.
        '''
        raise NotImplementedError("Replace this line with your implementation")

    def rotate(self):
        ''' Grid -> Grid

        Returns a new grid with the current block rotated 90 degrees clockwise.
        '''
        x, y, block = self.current_block
        return Grid(self.blocks, ActiveBlock(x, y, Block(
            [(y, -x) for x, y in block.posns])))

    def is_valid(self):
        ''' Grid -> bool

        Returns True iff the Grid is in a valid state.
        A Grid is in a valid state if all blocks (including the ActiveBlock)
        are in bounds and not overlapping.
        '''
        raise NotImplementedError("Replace this line with your implementation")

    def is_occupied(self, p):
        ''' (Grid, (int, int)) -> bool

        Returns True iff the posn `p` is occupied by a non-active block.
        '''
        raise NotImplementedError("Replace this line with your implementation")

    def _drop_above(self, r):
        return Grid([Block([(x, y if y < r else y - 1) for x, y in b.posns])
                     for b in self.blocks], self.current_block)

    def _clear_full_row(self, r):
        if r == HEIGHT:
            return self
        elif all(self.is_occupied((c, r)) for c in range(WIDTH)):
            cleared = Grid([Block([(x, y) for x, y in b.posns if y != r])
                            for b in self.blocks
                            if any(y != r
                                   for _, y in b.posns)], self.current_block)
            dropped = cleared._drop_above(r)
            return dropped._clear_full_row(r)
        else:
            return self._clear_full_row(r + 1)

    def clear_full_rows(self):
        ''' Grid -> Grid

        Returns a new Grid with any full rows cleared and the rows above them
        dropped.
        '''
        return self._clear_full_row(0)

    def place_block(self):
        ''' Grid -> Grid

        Returns a new grid with the current block moved into the placed blocks
        and a None current block
        '''
        return Grid(self.blocks + [Block([
            (self.current_block.x + bx, self.current_block.y + by)
            for bx, by in self.current_block.block.posns
        ])], None)

    def __eq__(self, other):
        try:
            return (other.current_block == self.current_block and
                    other.blocks == self.blocks)
        except AttributeError:
            return False


def new_block():
    ''' () -> Block

    Returns a new block randomly chosen from the L, backwards L, |, T, S, and
    backwards S.
    '''
    return random.choice([Block([(0, 2), (0, 1), (0, 0), (1, 0)]),
                          Block([(1, 2), (1, 1), (1, 0), (0, 0)]),
                          Block([(0, 3), (0, 2), (0, 1), (0, 0)]),
                          Block([(-1, 1), (0, 1), (1, 1), (0, 0)]),
                          Block([(-1, 0), (0, 0), (1, 0), (1, 1)]),
                          Block([(-1, 1), (0, 1), (0, 0), (1, 0)]),
                          Block([(0, 1), (1, 1), (0, 0), (1, 0)])])

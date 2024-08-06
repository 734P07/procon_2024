import random

class Grid:
    '''The grid of the game'''
    EMPTY = -1

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.cells = self.generate_empty_grid()

    def random_cells(self):
        for i in range(self.height):
            for j in range(self.width):
                rand = random.random()
                if rand < 0.25:
                    self.cells[i][j] = 0  
                elif rand < 0.5:
                    self.cells[i][j] = 1
                elif rand < 0.75:
                    self.cells[i][j] = 2  
                else:
                    self.cells[i][j] = 3

    def retrieve_empty_cells(self):
        empty_cells = []
        for i in range(self.height):
            for j in range(self.width):
                if self.cells[i][j] == Grid.EMPTY:
                    empty_cells.append((i, j))
        return empty_cells

    def generate_empty_grid(self):
        return [[Grid.EMPTY] * self.width for i in range(self.height)]

    def transpose(self):
        self.cells = [list(t) for t in zip(*self.cells)]
        self.height, self.width = \
                    self.width, self.height

    def reverse(self):
        for i in range(self.height):
            start = 0
            end = self.width - 1
            while start < end:
                self.cells[i][start], self.cells[i][end] = \
                    self.cells[i][end], self.cells[i][start]
                start += 1
                end -= 1

    def left_compress(self):
        new_grid = self.generate_empty_grid()
        for i in range(self.height):
            count = 0
            for j in range(self.width):
                if self.cells[i][j] != Grid.EMPTY:
                    new_grid[i][count] = self.cells[i][j]
                    count += 1
        self.cells = new_grid

    def set_cells(self, cells):
        self.cells = cells

    def print_grid(self):
        print('-' * 40)
        for i in range(self.height):
            for j in range(self.width):
                print('%d\t' % self.cells[i][j], end='')
            print()
        print('-' * 40)

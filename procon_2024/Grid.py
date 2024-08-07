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

    def up_compress(self):
        new_grid = self.generate_empty_grid()
        for j in range(self.width):
            count = 0
            for i in range(self.height):
                if self.cells[i][j] != Grid.EMPTY:
                    new_grid[count][j] = self.cells[i][j]
                    count += 1
        self.cells = new_grid

    def down_compress(self):
        new_grid = self.generate_empty_grid()
        for j in range(self.width):
            count = self.height - 1
            for i in range(self.height - 1, -1, -1):
                if self.cells[i][j] != Grid.EMPTY:
                    new_grid[count][j] = self.cells[i][j]
                    count -= 1
        self.cells = new_grid

    def left_compress(self):
        new_grid = self.generate_empty_grid()
        for i in range(self.height):
            count = 0
            for j in range(self.width):
                if self.cells[i][j] != Grid.EMPTY:
                    new_grid[i][count] = self.cells[i][j]
                    count += 1
        self.cells = new_grid

    def right_compress(self):
        new_grid = self.generate_empty_grid()
        for i in range(self.height):
            count = self.width - 1
            for j in range(self.width - 1, -1, -1):
                if self.cells[i][j] != Grid.EMPTY:
                    new_grid[i][count] = self.cells[i][j]
                    count -= 1
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

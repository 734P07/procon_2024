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

    def generate_empty_grid(self):
        return [[Grid.EMPTY] * self.width for i in range(self.height)]

    def set_cells(self, cells):
        self.cells = cells

    def print_grid(self):
        print('-' * 40)
        for i in range(self.height):
            for j in range(self.width):
                print('%d\t' % self.cells[i][j], end='')
            print()
        print('-' * 40)

from Grid import Grid

import random
class Problem:

    def __init__(self, height = 20, width=10):
        Problem.width = width
        Problem.height = height
        Problem.start_grid = Grid(self.height, self.width)
        Problem.goal_grid = Grid(self.height, self.width)
        Problem.patterns = [Grid(1, 1)]
        Problem.patterns[0].set_cells([[1]])
        for i in range(1, 9):
            ls = [[1] * 2**i for j in range(2**i)]
            k = Grid(2**i, 2**i)
            k.set_cells(ls)
            Problem.patterns.append(k)

            ls = []
            for j in range(2**i):
                ls.append([1]*2**i) if j%2==0 else ls.append([0]*2**i)
            k = Grid(2**i, 2**i)
            k.set_cells(ls)
            Problem.patterns.append(k)
            
            ls = [list(k) for k in zip(*ls)]
            k = Grid(2**i, 2**i)
            k.set_cells(ls)
            Problem.patterns.append(k)
        
    def generate_problem():
        Problem.start_grid.random_cells()
        for i in range(Problem.height):
            for j in range(Problem.width):
                Problem.goal_grid.cells[i][j] = Problem.start_grid.cells[i][j]
        random.shuffle(Problem.goal_grid.cells)
        for i in range(len(Problem.goal_grid.cells)):
            random.shuffle(Problem.goal_grid.cells[i])
        print("########## Problem generated! ##########")
        Problem.start_grid.print_grid()
        Problem.goal_grid.print_grid()

# problem = Problem()
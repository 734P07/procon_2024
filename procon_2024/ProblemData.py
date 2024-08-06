from Grid import Grid
class Problem:

    def __init__(self, height = 20, width=10):
        self.width = width
        self.height = height
        self.start_grid = Grid(self.height, self.width)
        self.goal_grid = Grid(self.height, self.width)
        self.patterns = [Grid(1, 1)]
        self.patterns[0].set_cells([[1]])
        for i in range(1, 9):
            ls = [[1] * 2**i for j in range(2**i)]
            k = Grid(2**i, 2**i)
            k.set_cells(ls)
            self.patterns.append(k)

            ls = []
            for j in range(2**i):
                ls.append([1]*2**i) if j%2==0 else ls.append([0]*2**i)
            k = Grid(2**i, 2**i)
            k.set_cells(ls)
            self.patterns.append(k)
            
            ls = [list(k) for k in zip(*ls)]
            k = Grid(2**i, 2**i)
            k.set_cells(ls)
            self.patterns.append(k)

# problem = Problem()
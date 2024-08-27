from Grid import Grid
from ProblemData import Problem

from copy import *

class Agent:
    def __init__(self):
        self.solution = []
        self.fail = 0
        self.grid = deepcopy(Problem.start_grid)
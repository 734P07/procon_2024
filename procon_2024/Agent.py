from Grid import Grid
from ProblemData import Problem

from copy import *

class Agent:
    def __init__(self):
        self.solution = []
        self.grid = deepcopy(Problem.start_grid)
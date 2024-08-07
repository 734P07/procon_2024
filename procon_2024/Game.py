from __future__ import print_function
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import random
import math, time

from ProblemData import Problem
from Grid import Grid

class GamePanel:
    '''The GUI view class'''
    ### Very lag, only use in analysis
    SHOW_BOARD = False

    CELL_PADDING = 1
    BACKGROUND_COLOR = '#92877d'
    EMPTY_CELL_COLOR = '#9e948a'
    CELL_BACKGROUND_COLOR_DICT = '#edc850'
    CELL_COLOR_DICT = "#f9f6f2"
    CELL_MATCHED = "#008000"
    FONT = ('Verdana', 7, 'bold')
    UP_KEYS = ('w', 'W', 'Up')
    LEFT_KEYS = ('a', 'A', 'Left')
    DOWN_KEYS = ('s', 'S', 'Down')
    RIGHT_KEYS = ('d', 'D', 'Right')

    def __init__(self, grid: Grid):
        self.grid = grid
        self.root = tk.Tk()
        self.root.title('Procon 2024')
        self.root.resizable(True, True)
        self.gridBackground = tk.Frame(self.root, bg=GamePanel.BACKGROUND_COLOR)
        self.interactBackground = tk.Frame(self.root, bg=GamePanel.CELL_COLOR_DICT)
        self.cell_labels = []
        if(GamePanel.SHOW_BOARD):
            for i in range(self.grid.height):
                row_labels = []
                for j in range(self.grid.width):
                    label = tk.Label(self.gridBackground, text='',
                                    bg=GamePanel.EMPTY_CELL_COLOR,
                                    justify=tk.CENTER, font=GamePanel.FONT,
                                    width=2)
                    label.grid(row=i, column=j, padx=GamePanel.CELL_PADDING, pady=GamePanel.CELL_PADDING)
                    row_labels.append(label)
                self.cell_labels.append(row_labels)
            self.gridBackground.pack(side='left', expand=True)

        tk.Label(self.interactBackground, text='X (width)').pack(side="top")
        xEntry = tk.Entry(self.interactBackground, justify='center', name="xEntry")
        xEntry.pack(side="top",fill="x")

        tk.Label(self.interactBackground, text='Y (height)').pack(side="top")
        yEntry = tk.Entry(self.interactBackground, justify='center', name="yEntry")
        yEntry.pack(side="top", fill="x")

        patternLabel = tk.Label(self.interactBackground, text='Pattern')
        patternLabel.pack(side="top")
        patternEntry = tk.Entry(self.interactBackground, justify='center', name="patternEntry")
        patternEntry.pack(side="top", fill="x")

        tk.Label(self.interactBackground, text='Direction').pack(side="top")
        directCombobox = ttk.Combobox(self.interactBackground, name="directCombobox", state='readonly')
        directCombobox['values'] = ('up', 'down', 'left', 'right')
        directCombobox.pack(side="top")

        makemoveButton = tk.Button(self.interactBackground, text='Make a move', name="makemoveButton")
        makemoveButton.pack(side='top')
        fetchButton = tk.Button(self.interactBackground, text='Fetch game data')
        fetchButton.pack(side='top')
        algoButton = tk.Button(self.interactBackground, text='Solve with algorithm', name="algoButton")
        algoButton.pack(side='top')
        self.interactBackground.pack(side='left', expand=True, fill="both")

    def paint(self):
        if(GamePanel.SHOW_BOARD):
            for i in range(self.grid.height):
                for j in range(self.grid.width):
                    if self.grid.cells[i][j] == Grid.EMPTY:
                        self.cell_labels[i][j].configure(
                            text='',
                            bg=GamePanel.EMPTY_CELL_COLOR)
                    elif self.grid.cells[i][j] == Problem.goal_grid.cells[i][j]:
                        cell_text = str(self.grid.cells[i][j])
                        bg_color = GamePanel.CELL_MATCHED
                        fg_color = GamePanel.CELL_COLOR_DICT
                        self.cell_labels[i][j].configure(
                            text=cell_text,
                            bg=bg_color, fg=fg_color)
                    else:
                        cell_text = str(self.grid.cells[i][j])
                        bg_color = GamePanel.CELL_BACKGROUND_COLOR_DICT
                        fg_color = GamePanel.CELL_COLOR_DICT
                        self.cell_labels[i][j].configure(
                            text=cell_text,
                            bg=bg_color, fg=fg_color)

class Game:
    '''Controller of the game.'''
    Direction = {'up' : 0, 'down' : 1, 'left':2, 'right':3}
    def __init__(self, panel: GamePanel):
        self.grid = Problem.start_grid
        self.panel = panel

    def start(self):
        Problem.generate_problem()
        self.panel.root.bind('<Key>', self.key_handler)
        self.panel.interactBackground.nametowidget("makemoveButton").bind('<Button-1>', self.make_move_btn)
        self.panel.interactBackground.nametowidget("algoButton").bind('<Button-1>', self.solve_with_alg_btn)
        self.panel.paint()
        self.panel.root.mainloop()

    def key_handler(self, event):
        pass

    def solve_with_alg_btn(self, event):
        self.solve_with_alg()

    def make_move_btn(self, event):
        pattern = int(self.panel.interactBackground.nametowidget("patternEntry").get())
        x = int(self.panel.interactBackground.nametowidget("xEntry").get())
        y = int(self.panel.interactBackground.nametowidget("yEntry").get())
        s = self.panel.interactBackground.nametowidget("directCombobox").get()
        self.make_move(pattern, x, y, s)
        self.panel.paint()

    def solve_with_alg(self):
        total = 0
        def align(power, col, row, s: str):
            print(f"Type/col/row/direction: {max(0,3*power-2)}/{col}/{row}/" + s)
            self.make_move(max(0,3*power-2), col, row, s)

        for row in range(Problem.height):
            for col in range(Problem.width):
                # Find in row
                for j in range(col, Problem.width):
                    if self.grid.cells[row][j] == Problem.goal_grid.cells[row][col]:
                        diff = j-col
                        while(diff != 0):
                            power = int(math.log2(diff))
                            if(2**power > diff):
                                power -= 1
                            align(power, col, row, 'left')
                            diff -= 2**power
                            total+=1
                            self.panel.paint()
                            self.panel.root.update()
                        break
                # Find in col
                for i in range(row, Problem.height):
                    if self.grid.cells[i][col] == Problem.goal_grid.cells[row][col]:
                        diff = i-row
                        while(diff != 0):
                            power = int(math.log2(diff))
                            if(2**power > diff):
                                power -= 1
                            align(power, col, row, 'up')
                            diff -= 2**power
                            total+=1
                            self.panel.paint()
                            self.panel.root.update()
                        break
                # Find in the rest of table
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    for i in range(row+1, Problem.height):
                        for j in range(Problem.width):
                            if self.grid.cells[i][j] == Problem.goal_grid.cells[row][col]:
                                diff = (col - j if col>j else j-col) 
                                while(diff != 0):
                                    power = int(math.log2(diff))
                                    if(2**power > diff):
                                        power -= 1
                                    align(power, j+1, i, 'right') if(j < col) else align(power, col, i, 'left')
                                    j+=2**power ## be careful
                                    diff -= 2**power
                                    total+=1
                                    self.panel.paint()
                                    self.panel.root.update()
                                break
                        if self.grid.cells[i][col] == Problem.goal_grid.cells[row][col]:
                            diff = (row - i if row>i else i-row)
                            while(diff != 0):
                                power = int(math.log2(diff))
                                if(2**power > diff):
                                    power -= 1
                                align(power, col, row, 'up')
                                diff -= 2**power
                                total+=1
                                self.panel.paint()
                                self.panel.root.update()
                            break

        print("Total step: ", total)
        fail = 0
        for row in range(Problem.height):
            for col in range(Problem.width):
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    fail+=1
        print("Fail: ", fail)

    def make_move(self, p, x, y, s: str):
        ls = self.erased_cells(p=p, x=x, y=y)
        # for i in ls:
        #     print(i, end=' ')
        # print("\n")
        getattr(self, s)()
        empty_cells = self.grid.retrieve_empty_cells()
        for i in range(len(ls)):
            self.grid.cells[empty_cells[i][0]][empty_cells[i][1]] = ls[i]

    def erased_cells(self, p, x, y) -> list:
        ## error with >24th pattern
        ls = []
        for i in range(Problem.patterns[p].height):
            for j in range(Problem.patterns[p].width):
                if Problem.patterns[p].cells[i][j] == 1:
                    try:
                        if(y+i>=0 and x+j>=0):
                            ls.append(self.grid.cells[y+i][x+j])
                            self.grid.cells[y+i][x+j] = Grid.EMPTY
                    except:
                        break
        return ls
        

    def up(self):
        self.grid.up_compress()

    def left(self):
        self.grid.left_compress()

    def down(self):
        self.grid.down_compress()

    def right(self):
        self.grid.right_compress()


if __name__ == '__main__':
    problem = Problem(35, 35)
    panel = GamePanel(problem.start_grid)
    test_game = Game(panel)
    test_game.start()

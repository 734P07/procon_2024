from __future__ import print_function
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import math
import requests
import json

from ProblemData import Problem
from Grid import Grid
from Agent import Agent

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

        tk.Label(self.interactBackground, text='Token').pack(side="top")
        tokenEntry = tk.Entry(self.interactBackground, justify='center', name="tokenEntry")
        tokenEntry.pack(side="top", fill="x")

        tk.Label(self.interactBackground, text='Question ID').pack(side="top")
        qIDEntry = tk.Entry(self.interactBackground, justify='center', name="qIDEntry")
        qIDEntry.pack(side="top", fill="x")

        tk.Label(self.interactBackground, text='Answer index').pack(side="top")
        answerEntry = tk.Entry(self.interactBackground, justify='center', name="answerEntry")
        answerEntry.pack(side="top", fill="x")

        tk.Label(self.interactBackground, text='X (width)').pack(side="top")
        xEntry = tk.Entry(self.interactBackground, justify='center', name="xEntry")
        xEntry.pack(side="top",fill="x")

        tk.Label(self.interactBackground, text='Y (height)').pack(side="top")
        yEntry = tk.Entry(self.interactBackground, justify='center', name="yEntry")
        yEntry.pack(side="top", fill="x")

        tk.Label(self.interactBackground, text='Pattern').pack(side="top")
        patternEntry = tk.Entry(self.interactBackground, justify='center', name="patternEntry")
        patternEntry.pack(side="top", fill="x")

        tk.Label(self.interactBackground, text='Direction').pack(side="top")
        directCombobox = ttk.Combobox(self.interactBackground, name="directCombobox", state='readonly')
        directCombobox['values'] = ('up', 'down', 'left', 'right')
        directCombobox.pack(side="top")

        makemoveButton = tk.Button(self.interactBackground, text='Make a move', name="makemoveButton")
        makemoveButton.pack(side='top')

        fetchButton = tk.Button(self.interactBackground, text='Fetch game data', name="fetchDataBtn")
        fetchButton.pack(side='top')

        tk.Label(self.interactBackground, text='Solver').pack(side="top")

        basicSolveBtn = tk.Button(self.interactBackground, text='Find basic solution', name="basicSolveBtn")
        basicSolveBtn.pack(side='top')

        advSolveBtn = tk.Button(self.interactBackground, text='Advance solution', name="advSolveBtn")
        advSolveBtn.pack(side='top')

        advSolveBtn2 = tk.Button(self.interactBackground, text='Advance solution 2', name="advSolveBtn2")
        advSolveBtn2.pack(side='top')

        testSolveBtn = tk.Button(self.interactBackground, text='Testing solution', name="testSolveBtn")
        testSolveBtn.pack(side='top')

        tk.Label(self.interactBackground, text='Answer').pack(side="top")

        showAnsBtn = tk.Button(self.interactBackground, text='Show answers', name="showAnsBtn")
        showAnsBtn.pack(side='top')

        sendAnsBtn = tk.Button(self.interactBackground, text='Send answer', name="sendAnsBtn")
        sendAnsBtn.pack(side='top')

        self.interactBackground.pack(side='left', expand=True, fill="both")

    def switch_grid(self, grid):
        self.grid = grid

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
    url = "https://proconvn.duckdns.org"

    def __init__(self, panel: GamePanel):
        self.grid = Problem.start_grid
        self.panel = panel
        self.agents = []

    def start(self):
        self.panel.root.bind('<Key>', self.key_handler)
        self.panel.interactBackground.nametowidget("fetchDataBtn").bind('<Button-1>', self.fetch_data_btn)
        self.panel.interactBackground.nametowidget("makemoveButton").bind('<Button-1>', self.make_move_btn)

        self.panel.interactBackground.nametowidget("basicSolveBtn").bind('<Button-1>', self.basic_solve_btn)
        self.panel.interactBackground.nametowidget("advSolveBtn").bind('<Button-1>', self.adv_solve_btn)
        self.panel.interactBackground.nametowidget("advSolveBtn2").bind('<Button-1>', self.adv_solve_btn2)
        self.panel.interactBackground.nametowidget("testSolveBtn").bind('<Button-1>', self.kmp_solve_btn)
        
        self.panel.interactBackground.nametowidget("showAnsBtn").bind('<Button-1>', self.show_answer_btn)
        self.panel.interactBackground.nametowidget("sendAnsBtn").bind('<Button-1>', self.send_answer_btn)
        self.panel.paint()
        self.panel.root.mainloop()

    def key_handler(self, event):
        pass

    def basic_solve_btn(self, event):
        self.agents.append(Agent())
        self.grid = self.agents[len(self.agents)-1].grid
        self.panel.switch_grid(self.grid)
        self.basic_solve()

    def adv_solve_btn(self, event):
        self.agents.append(Agent())
        self.grid = self.agents[len(self.agents)-1].grid
        self.panel.switch_grid(self.grid)
        self.adv_solve()

    def adv_solve_btn2(self, event):
        self.agents.append(Agent())
        self.grid = self.agents[len(self.agents)-1].grid
        self.panel.switch_grid(self.grid)
        self.adv_solve2()
    
    def kmp_solve_btn(self, event):
        self.agents.append(Agent())
        self.grid = self.agents[len(self.agents)-1].grid
        self.panel.switch_grid(self.grid)
        self.solve_with_kmp()

    def make_move_btn(self, event):
        pattern = int(self.panel.interactBackground.nametowidget("patternEntry").get())
        x = int(self.panel.interactBackground.nametowidget("xEntry").get())
        y = int(self.panel.interactBackground.nametowidget("yEntry").get())
        s = self.panel.interactBackground.nametowidget("directCombobox").get()
        self.make_move(pattern, x, y, s)

    def fetch_data_btn(self, event):
        self.agents.clear()

        headers = {"Authorization": self.panel.interactBackground.nametowidget("tokenEntry").get()}
        question_id = int(self.panel.interactBackground.nametowidget("qIDEntry").get())
        question_response = requests.get(f"{Game.url}/question/{question_id}", headers=headers)
        question_json = question_response.json()

        print("----------------------------------------")
        print(f"Status code: {question_response.status_code}")
        print("----------------------------------------")

        question_data = json.loads(question_json["question_data"])
        
        Problem.width = question_data["board"]["width"]
        Problem.height = question_data["board"]["height"]
        Problem.start_grid = Grid(Problem.height, Problem.width)
        Problem.start_grid.cells = question_data["board"]["start"]
        Problem.goal_grid = Grid(Problem.height, Problem.width)
        Problem.goal_grid.cells = question_data["board"]["goal"]

    def show_answer_btn(self, event):
        print("----------------------------------------")
        print(f"{len(self.agents)} answers created:")
        for i in range(len(self.agents)):
            print(f"+ {i}: {len(self.agents[i].solution)} steps, {self.agents[i].fail} cells failed")
        print("----------------------------------------")

    def send_answer_btn(self, event):
        headers = {"Authorization": self.panel.interactBackground.nametowidget("tokenEntry").get()}
        question_id = int(self.panel.interactBackground.nametowidget("qIDEntry").get())
        answer_id = int(self.panel.interactBackground.nametowidget("answerEntry").get())

        payload = {"question_id": question_id, "answer_data": {"n": len(self.agents[answer_id].solution), "ops": self.agents[answer_id].solution}}
        response = requests.post(f"{Game.url}/answer", json=payload, headers=headers)

        print("----------------------------------------")
        print(f"Status code: {response.status_code}")
        print("----------------------------------------")

    def basic_solve(self):
        total = 0
        fail = 0
        def align(power, col, row, s: str):
            self.make_move_log(max(0,3*power-2), col, row, s)

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
                        break
                # Find in the rest of table
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    for i in range(row+1, Problem.height):
                        for j in range(Problem.width):
                            if self.grid.cells[i][j] == Problem.goal_grid.cells[row][col]:
                                diff = abs(col - j) 
                                self.make_move_log(23, Problem.width - diff, i, 'right') if(j < col) else self.make_move_log(23, diff, i, 'right')
                                total+=1
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
                            break

        print("Total step: ", total)
        for row in range(Problem.height):
            for col in range(Problem.width):
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    fail+=1
        self.agents[len(self.agents) - 1].fail = fail
        print("Fail: ", fail)

    ### Bad solution
    def solve_with_kmp(self):
        total = 0
        fail = 0

        def align(power, col, row, s: str):
            self.make_move_log(max(0,3*power-2), col, row, s)

        for row in range(Problem.height):
            for col in range(Problem.width):
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    # Phase 1: find best match
                    best = [0, 0, 0]
                    lps = [0]
                    ### find lps
                    for i in range(col+1, Problem.width):
                        j = lps[i - col - 1]
                        while j > 0 and Problem.goal_grid.cells[row][j+col] != Problem.goal_grid.cells[row][i]:
                            j = lps[j - 1]
                        lps.append(j + 1 if Problem.goal_grid.cells[row][j+col] == Problem.goal_grid.cells[row][i] else j)
                    ### find in row
                    j=0
                    for i in range(col, Problem.width):
                        while j > 0 and self.grid.cells[row][i] != Problem.goal_grid.cells[row][j+col]:
                            j = lps[j - 1]
                        if self.grid.cells[row][i] == Problem.goal_grid.cells[row][j+col]: 
                            j += 1
                            if j > best[2]:
                                best = [row, i - j + 1, j]
                    ### find in rest
                    for m in range(row+1, Problem.height):
                        j = 0
                        for i in range(Problem.width):
                            while j > 0 and self.grid.cells[m][i] != Problem.goal_grid.cells[row][j+col]:
                                j = lps[j - 1]
                            if self.grid.cells[m][i] == Problem.goal_grid.cells[row][j+col]: 
                                j += 1
                                if j > best[2]:
                                    best = [m, i - j + 1, j]
                            if j == len(lps): 
                                best = [m, i - j + 1, j]
                                break
                        if(best[2] == len(lps)): break

                    # Phase 2: fit best match to right place
                    ### align best match to right column
                    diff = abs(col - best[1])
                    while(diff != 0):
                        power = int(math.log2(diff))
                        if(2**power > diff):
                            power -= 1
                        align(power, best[1]+best[2], best[0], 'right') if(best[1] < col) else align(power, col, best[0], 'left')
                        best[1]+=2**power ## be careful
                        diff -= 2**power
                        total+=1
                    ### bring best match to right row
                    diff = abs(row - best[0])
                    while(diff != 0):
                        power = int(math.log2(diff))
                        if(2**power > diff):
                            power -= 1
                        tmp = col
                        while(tmp < col + best[2]):
                            align(power, tmp, row, 'up')
                            total+=1
                            tmp+=2**power
                        diff -= 2**power
        print("Total step: ", total)
        for row in range(Problem.height):
            for col in range(Problem.width):
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    fail+=1
        self.agents[len(self.agents) - 1].fail = fail
        print("Fail: ", fail)

    def adv_solve(self):
        total = 0
        fail = 0
        cell_done = False
        def align(power, col, row, s: str):
            self.make_move_log(max(0,3*power-2), col, row, s)

        for row in range(Problem.height - 1, -1, -1):
            for col in range(Problem.width):
                match = -1
                if cell_done:
                    cell_done = False
                    continue
                check = False
                ### Find in col (max step 1 or 1/2)
                for i in range(Problem.height - 1 - row, Problem.height):
                    if self.grid.cells[i][col] == Problem.goal_grid.cells[row][col]:
                        # if i == 0:
                        #     check = True
                        #     break
                        if col < Problem.width - 1 and self.grid.cells[i][col+1] == Problem.goal_grid.cells[row][col+1]:
                            self.make_move_log(2, col, i, 'down')
                            cell_done = True
                            total+=1
                            check = True
                            break
                        else:
                            match = i    
                if(match!=-1 and not check):
                    self.make_move_log(0, col, match, 'down')
                    total+=1
                    continue
                ### Find in rest (max step 2)
                if not check:
                    for i in range(Problem.height - row, Problem.height):
                        for j in range(Problem.width):
                            if self.grid.cells[i][j] == Problem.goal_grid.cells[row][col]:
                                diff = abs(col - j) 
                                self.make_move_log(23, Problem.width - diff, i, 'right') if(j < col) else self.make_move_log(23, diff, i, 'right')
                                total+=1
                                check = True
                                break
                        if check:
                            self.make_move_log(0, col, i, 'down')
                            total+=1
                            break
                ### Find in row (max step 8) -> optimize to 3
                if not check:
                    for j in range(col, Problem.width):
                        if self.grid.cells[Problem.height - 1 - row][j] == Problem.goal_grid.cells[row][col]:
                            diff = j-col
                            while(diff != 0):
                                power = int(math.log2(diff))
                                if(2**power > diff):
                                    power -= 1
                                align(power, col, Problem.height - 1 - row, 'left')
                                diff -= 2**power
                                total+=1
                            check = True
                            break
                    if check:
                        self.make_move_log(0, col, Problem.height - 1 - row, 'down')
                        total+=1
        print("Total step: ", total)
        for row in range(Problem.height):
            for col in range(Problem.width):
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    fail+=1
        self.agents[len(self.agents) - 1].fail = fail
        print("Fail: ", fail)

    def adv_solve2(self):
        total = 0
        fail = 0
        cell_done = False
        def align(power, col, row, s: str):
            self.make_move_log(max(0,3*power-2), col, row, s)

        for col in range(Problem.width - 1, -1, -1):
            for row in range(Problem.height):
                match = -1
                if cell_done:
                    cell_done = False
                    continue
                check = False
                ### Find in row (max step 1 or 1/2)
                for j in range(Problem.width - 1 - col, Problem.width):
                    if self.grid.cells[row][j] == Problem.goal_grid.cells[row][col]:
                        # if j == 0:
                        #     check = True
                        #     break
                        if row < Problem.height - 1 and self.grid.cells[row+1][j] == Problem.goal_grid.cells[row+1][col]:
                            self.make_move_log(3, j, row, 'right')
                            cell_done = True
                            total+=1
                            check = True
                            break
                        else:
                            match = j
                if(match!=-1 and not check):
                    self.make_move_log(0, match, row, 'right')
                    total+=1
                    continue
                ### Find in rest (max step 2)
                if not check:
                    for j in range(Problem.width - col, Problem.width):
                        for i in range(Problem.height):
                            if self.grid.cells[i][j] == Problem.goal_grid.cells[row][col]:
                                diff = abs(row - i) 
                                self.make_move_log(24, j, Problem.height - diff, 'down') if(i < row) else self.make_move_log(24, j, diff, 'down')
                                total+=1
                                check = True
                                break
                        if check:
                            self.make_move_log(0, j, row, 'right')
                            total+=1
                            break
                ### Find in col (max step 8) -> optimize to 3
                if not check:
                    for i in range(row, Problem.height):
                        if self.grid.cells[i][Problem.width - 1 - col] == Problem.goal_grid.cells[row][col]:
                            diff = i-row
                            while(diff != 0):
                                power = int(math.log2(diff))
                                if(2**power > diff):
                                    power -= 1
                                align(power, Problem.width - 1 - col, row, 'up')
                                diff -= 2**power
                                total+=1
                            check = True
                            break
                    if check:
                        self.make_move_log(0, Problem.width - 1 - col, row, 'right')
                        total+=1
        print("Total step: ", total)
        for row in range(Problem.height):
            for col in range(Problem.width):
                if(self.grid.cells[row][col] != Problem.goal_grid.cells[row][col]):
                    fail+=1
        self.agents[len(self.agents) - 1].fail = fail
        print("Fail: ", fail)

    def make_move_log(self, p, x, y, s:str):
        self.make_move(p,x,y,s)
        self.agents[len(self.agents) - 1].solution.append({"p":p, "x":x, "y":y, "s":Game.Direction[s]})

    def make_move(self, p, x, y, s:str):
        print(f"Type/col/row/direction: {p}/{x}/{y}/" + s)
        xLow = max(0, x)
        yLow = max(0, y)
        xHigh = min(Problem.width, x + Problem.patterns[p].width)
        yHigh = min(Problem.height, y + Problem.patterns[p].height)
        if(s == 'up'):
            for j in range(xLow, xHigh):
                erase = []
                keep = []
                for i in range(yLow, Problem.height):
                    iPattern = i - y
                    jPattern = j - x
                    try:
                        if Problem.patterns[p].cells[iPattern][jPattern] == 1:
                            erase.append(self.grid.cells[i][j])
                        else:
                            keep.append(self.grid.cells[i][j])
                    except:
                        keep.append(self.grid.cells[i][j])
                for i in range(len(keep)):
                    self.grid.cells[yLow+i][j] = keep[i]
                for i in range(len(erase)):
                    self.grid.cells[yLow+len(keep)+i][j] = erase[i]
            self.panel.paint()
            self.panel.root.update()
            return
        if(s == 'down'):
            for j in range(xLow, xHigh):
                erase = []
                keep = []
                jPattern = j - x
                for i in range(yHigh - 1, -1, -1):
                    iPattern = i - y
                    try:
                        if Problem.patterns[p].cells[iPattern][jPattern] == 1 and iPattern>=0:
                            erase.append(self.grid.cells[i][j])
                        else:
                            keep.append(self.grid.cells[i][j])
                    except:
                        keep.append(self.grid.cells[i][j])
                for i in range(len(keep)):
                    self.grid.cells[yHigh-1-i][j] = keep[i]
                for i in range(len(erase)):
                    self.grid.cells[yHigh-1-len(keep)-i][j] = erase[i]
            self.panel.paint()
            self.panel.root.update()
            return
        if(s == 'left'):
            for i in range(yLow, yHigh):
                erase = []
                keep = []
                for j in range(xLow, Problem.width):
                    iPattern = i - y
                    jPattern = j - x
                    try:
                        if Problem.patterns[p].cells[iPattern][jPattern] == 1:
                            erase.append(self.grid.cells[i][j])
                        else:
                            keep.append(self.grid.cells[i][j])
                    except:
                        keep.append(self.grid.cells[i][j])
                for j in range(len(keep)):
                    self.grid.cells[i][xLow+j] = keep[j]
                for j in range(len(erase)):
                    self.grid.cells[i][xLow+len(keep)+j] = erase[j]
            self.panel.paint()
            self.panel.root.update()
            return
        for i in range(yLow, yHigh):
            erase = []
            keep = []
            iPattern = i - y
            for j in range(xHigh - 1, -1, -1):
                jPattern = j - x
                try:
                    if Problem.patterns[p].cells[iPattern][jPattern] == 1 and jPattern>=0:
                        erase.append(self.grid.cells[i][j])
                    else:
                        keep.append(self.grid.cells[i][j])
                except:
                    keep.append(self.grid.cells[i][j])
            for j in range(len(keep)):
                self.grid.cells[i][xHigh-1-j] = keep[j]
            for j in range(len(erase)):
                self.grid.cells[i][xHigh-1-len(keep)-j] = erase[j]
        self.panel.paint()
        self.panel.root.update()
        return

if __name__ == '__main__':
    problem = Problem(32, 32)
    panel = GamePanel(problem.start_grid)
    test_game = Game(panel)
    test_game.start()

#######################################################
#### MazeGame uses a grid of rows X cols to demonstrate
#### pathfinding using A*.
####
#### AI, Spring 2024
#######################################################
import queue
import sys
import re
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
from queue import PriorityQueue


######################################################

#### A cell stores f(), g() and h() values
#### A cell is either open or part of a wall
######################################################

class Cell:
    #### Initially, arre maze cells have g() = inf and h() = 0
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None
        self.priority = None


    #### Compare two cells based on their evaluation functions
    def __lt__(self, other):
        return self.f < other.f


######################################################
# A maze is a grid of size rows X cols
######################################################
class MazeGame:
    def __init__(self, root, maze, file):
        self.root = root
        self.maze = maze

        self.rows = 30
        self.cols = 36
        self.path_stack = []

        self.cells = [[Cell(x, y, maze[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]


        self.algorithm, self.start, self.delivery = self.file_read(file)

        for i in range(self.rows):
            for j in range(self.cols):
                if (maze[i][j] == 'u' or maze[i][j] == 'e' or maze[i][j] == 'o' or maze[i][j] == 'b'):
                    self.cells[i][j].priority = -5
                elif (maze[i][j] == 's' or maze[i][j] == 'm'):
                    self.cells[i][j].priority = -4
                elif (maze[i][j] == 'h' or maze[i][j] == 'p'):
                    self.cells[i][j].priority = -3
                elif (maze[i][j] == 'd' or maze[i][j] == 'g'):
                    self.cells[i][j].priority = -2
                elif (maze[i][j] == 'a' or maze[i][j] == 'i'):
                    self.cells[i][j].priority = -1
                else:
                    self.cells[i][j].priority = 0

        self.delivery_locations = PriorityQueue()

        for i in self.delivery:
            self.delivery_locations.put((self.cells[i[0]][i[1]].priority, i))


        #### Start state: (0,0) or top left
        self.agent_pos = eval(self.start)

        #### Goal state:  (rows-1, cols-1) or bottom right
        self.goal_pos = (0,0)

        self.goals_completed = []
        self.goals_failed = []

        #### Start state's initial values for f(n) = g(n) + h(n)
        self.cells[self.agent_pos[0]][self.agent_pos[1]].g = 0
        if (self.algorithm=="A*"):
            self.cells[self.agent_pos[0]][self.agent_pos[1]].h = self.a_star_heuristic(self.agent_pos)
            self.cells[self.agent_pos[0]][self.agent_pos[1]].f = self.a_star_heuristic(self.agent_pos)

        if (self.algorithm=="Dijkstra's"):
            self.cells[self.agent_pos[0]][self.agent_pos[1]].h = self.dijkstra_heuristic(self.agent_pos)
            self.cells[self.agent_pos[0]][self.agent_pos[1]].f = self.dijkstra_heuristic(self.agent_pos)

        #### The maze cell size in pixels
        self.cell_size = 30
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()

        #### Display the optimum path in the maze
        while not self.delivery_locations.empty():
            print(self.delivery_locations.empty())
            self.goal_pos = self.delivery_locations.get()[1]
            print(self.goal_pos)
            self.find_path()
            self.agent_pos = self.goal_pos

    #Needs a lot of work
    def file_read(self, file):
        all_lines = []
        with open(file, 'r') as file:
            for line in file:
                all_lines.append(line.strip())
            algorithm = None
            start = None
            delivery = None
            if all_lines[0].startswith('Delivery algorithm:'):
                algorithm = all_lines[0].split(':')[1].strip()

            if all_lines[1].startswith('Start location:'):
                start = re.match(r'Start location:\s*\((\d+),\s*(\d+)\)', all_lines[1])
                if (start != None):
                   start=all_lines[1].split(':')[1].strip()

            if all_lines[2].startswith('Delivery locations:'):
                delivery = re.findall(r'\s*\((\d+),\s*(\d+)\)', all_lines[2])
                delivery = [(int(x), int(y)) for x, y in delivery]

            return algorithm, start, delivery

    def assign_priorities(self):
        for i in range(self.cols):
            for j in range(self.rows):
                if(self.cells[i][j] == 'u' or self.cells[i][j] == 'e' or self.cells[i][j] == 'o' or self.cells[i][j] == 'b'):
                    self.cells[i][j].priority = 5
                elif(self.cells[i][j] == 's' or self.cells[i][j] == 'm'):
                    self.cells[i][j].priority = 4
                elif (self.cells[i][j] == 'h' or self.cells[i][j] == 'p'):
                    self.cells[i][j].priority = 3
                elif (self.cells[i][j] == 'd' or self.cells[i][j] == 'g'):
                    self.cells[i][j].priority = 2
                elif (self.cells[i][j] == 'a' or self.cells[i][j] == 'i'):
                    self.cells[i][j].priority = 1
                else:
                    self.cells[i][j].priority = 0



    ############################################################
    #### This is for the GUI part. No need to modify this unless
    #### GUI changes are needed.
    ############################################################
    def draw_maze(self):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.maze[x][y] == 'm':
                    color = 'deepskyblue'
                elif self.maze[x][y] == 'g':
                    color = 'red'
                elif self.maze[x][y] == 'e':
                    color = 'yellow'
                elif self.maze[x][y] == 'u':
                    color = 'orange'
                elif self.maze[x][y] == 'o':
                    color = 'mediumseagreen'
                elif self.maze[x][y] == 'p':
                    color = 'lightgreen'
                elif self.maze[x][y] == 's':
                    color = 'lightpink'
                elif self.maze[x][y] == 'b':
                    color = 'plum'
                elif self.maze[x][y] == 'h':
                    color = 'lightsalmon'
                elif self.maze[x][y] == 'a':
                    color = 'silver'
                elif self.maze[x][y] == 'd':
                    color = 'yellowgreen'
                elif self.maze[x][y] == 'i':
                    color = 'lightblue'
                elif self.maze[x][y] == 1:
                    color = 'black'
                else:
                    color = 'white'
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)

    ############################################################
    #### Manhattan distance
    ############################################################
    def a_star_heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))

    def dijkstra_heuristic(self, pos):
        return 0

    ############################################################
    #### Algorithm
    ############################################################
    def find_path(self):

        #print(self.goal_pos)
        #print(self.agent_pos)

        open_set = PriorityQueue()

        print(self.agent_pos)
        #### Add the start state to the queue
        open_set.put((0, self.agent_pos))

        #### Continue exploring until the queue is exhausted
        while not open_set.empty():
            current_cost, current_pos = open_set.get()
            current_cell = self.cells[current_pos[0]][current_pos[1]]

            #### Stop if goal is reached
            if current_pos == self.goal_pos:
                self.reconstruct_path()
                while not open_set.empty():
                    _, current_cell = open_set.get()
                    # Resetting the attributes of the current cell
                    self.cells[current_cell[0]][current_cell[1]].g = float("inf")
                    self.cells[current_cell[0]][current_cell[1]].f = float("inf")
                    self.cells[current_cell[0]][current_cell[1]].h = 0
                    self.cells[current_cell[0]][current_cell[1]].parent = None
                while not open_set.empty():
                    # clear the list to make it possible to go backwards
                    open_set.get()
                self.agent_pos = self.goal_pos
                break


            #### Agent goes E, W, N, and S, whenever possible
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_pos = (current_pos[0] + dx, current_pos[1] + dy)

                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and not self.cells[new_pos[0]][
                    new_pos[1]].is_wall:

                    #### The cost of moving to a new position is 1 unit
                    new_g = current_cell.g + 1

                    if new_g < self.cells[new_pos[0]][new_pos[1]].g:
                        ### Update the path cost g()
                        self.cells[new_pos[0]][new_pos[1]].g = new_g

                        ### Update the heurstic h()
                        if (self.algorithm=="A*"):
                            self.cells[new_pos[0]][new_pos[1]].h = self.a_star_heuristic(new_pos)
                        if (self.algorithm=="Dijkstra's"):
                            self.cells[new_pos[0]][new_pos[1]].h = self.dijkstra_heuristic(new_pos)

                        ### Update the evaluation function for the cell n: f(n) = g(n) + h(n)
                        self.cells[new_pos[0]][new_pos[1]].f = new_g + self.cells[new_pos[0]][new_pos[1]].h
                        self.cells[new_pos[0]][new_pos[1]].parent = current_cell

                        #### Add the new cell to the priority queue
                        open_set.put((self.cells[new_pos[0]][new_pos[1]].f, new_pos))


    ############################################################
    #### This is for the GUI part. No need to modify this unless
    #### screen changes are needed.
    ############################################################
    def reconstruct_path(self):
        current_cell = self.cells[self.goal_pos[0]][self.goal_pos[1]]
        while current_cell.parent:
            x, y = current_cell.x, current_cell.y
            self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                         (x + 1) * self.cell_size, fill='green')
            current_cell = current_cell.parent
            self.path_stack.append(current_cell)
            # Redraw cell with updated g() and h() values
            color = 'darkblue'
            self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                         (x + 1) * self.cell_size, fill=color)



    ############################################################
    #### This is for the GUI part. No need to modify this unless
    #### screen changes are needed.
    ############################################################
    def move_agent(self, event):

        #### Move right, if possible
        if event.keysym == 'Right' and self.agent_pos[1] + 1 < self.cols and not self.cells[self.agent_pos[0]][
            self.agent_pos[1] + 1].is_wall:
            self.agent_pos = (self.agent_pos[0], self.agent_pos[1] + 1)


        #### Move Left, if possible
        elif event.keysym == 'Left' and self.agent_pos[1] - 1 >= 0 and not self.cells[self.agent_pos[0]][
            self.agent_pos[1] - 1].is_wall:
            self.agent_pos = (self.agent_pos[0], self.agent_pos[1] - 1)

        #### Move Down, if possible
        elif event.keysym == 'Down' and self.agent_pos[0] + 1 < self.rows and not self.cells[self.agent_pos[0] + 1][
            self.agent_pos[1]].is_wall:
            self.agent_pos = (self.agent_pos[0] + 1, self.agent_pos[1])

        #### Move Up, if possible
        elif event.keysym == 'Up' and self.agent_pos[0] - 1 >= 0 and not self.cells[self.agent_pos[0] - 1][
            self.agent_pos[1]].is_wall:
            self.agent_pos = (self.agent_pos[0] - 1, self.agent_pos[1])

        #### Erase agent from the previous cell at time t
        self.canvas.delete("agent")

        ### Redraw the agent in color navy in the new cell position at time t+1
        self.canvas.create_rectangle(self.agent_pos[1] * self.cell_size, self.agent_pos[0] * self.cell_size,
                                     (self.agent_pos[1] + 1) * self.cell_size, (self.agent_pos[0] + 1) * self.cell_size,
                                     fill='navy', tags="agent")


############################################################
#### Modify the wall cells to experiment with different maze
#### configurations.
############################################################
m = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0]
]

maze = [
[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 'm', 'm', 'm', 'm', 'm', 1, 'm', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 'm', 'm', 'm', 1, 'm', 'm', 'm', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 'm', 1, 1, 1, 'm', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 1, 1, 1, 'm', 'm', 1, 'g', 'g', 'g', 1, 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 'm', 'm', 1, 1, 1, 'g', 'g', 1, 'g', 'g', 1, 1, 'g', 1, 'g', 1, 1, 1, 'g', 1, 1, 'g', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 0, 0, 1, 'e', 1, 'e', 'e', 1, 'a', 1],
[1, 0, 0, 1, 'i', 1, 1, 1, 1, 1, 'g', 1, 1, 'g', 1, 1, 'g', 'g', 1, 1, 'g', 1, 'g', 1, 1, 1, 0, 0, 1, 1, 1, 'e', 'e', 1, 'a', 'a'],
[1, 0, 0, 1, 'i', 1, 'i', 'i', 1, 'g', 'g', 'g', 'g', 'g', 1, 'g', 'g', 'g', 'g', 1, 'g', 1, 'g', 1, 'i', 1, 0, 0, 'e', 'e', 1, 'e', 'e', 1, 1, 1],
[1, 0, 0, 0, 1, 1, 1, 'i', 1, 'g', 'g', 'g', 'g', 'g', 'g', 1, 1, 'g', 1, 1, 1, 1, 1, 1, 'i', 1, 0, 0, 1, 1, 1, 'e', 'e', 1, 1, 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 'g', 'g', 1, 'g', 'g', 'g', 'g', 1, 'g', 'g', 'g', 1, 'e', 1, 1, 'i', 1, 0, 0, 'e', 'e', 'e', 'e', 'e', 1, 'a', 'a'],
[1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 1, 1, 1, 'b', 1, 1, 1, 1, 'g', 'g', 1, 'e', 1, 'i', 'i', 'i', 0, 0, 1, 1, 1, 1, 1, 1, 'a', 'a'],
[1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 'b', 'b', 'b', 'b', 'b', 'b', 'b', 1, 'g', 'g', 1, 'e', 1, 1, 1, 1, 0, 0, 1, 'u', 'a', 'a', 'a', 'a', 'a', 1],
[1, 0, 0, 1, 'o', 'o', 'o', 'o', 'o', 1, 'b', 'b', 1, 1, 'b', 1, 1, 1, 'g', 'g', 1, 'e', 1, 1, 'e', 'e', 0, 0, 'u', 'u', 1, 1, 1, 1, 1, 1],
[1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 'b', 'b', 'b', 1, 'b', 1, 'g', 'g', 'g', 'g', 1, 'e', 1, 'o', 1, 'e', 0, 0, 1, 'u', 'u', 'u', 'u', 'u', 'u', 1],
[1, 0, 0, 1, 'o', 1, 1, 1, 'o', 1, 'b', 1, 1, 1, 'b', 1, 1, 1, 1, 1, 0, 0, 'o', 'o', 1, 1, 0, 0, 1, 'u', 'u', 'u', 'u', 1, 'u', 1],
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'u', 'u', 1, 1, 1, 1, 1],
[1, 0, 0, 0, 0, 1, 'i', 1, 1, 'a', 1, 'a', 1, 1, 'h', 1, 1, 1, 'h', 1, 0, 1, 1, 's', 1, 1, 'o', 1, 1, 1, 'u', 'u', 'u', 'u', 'u', 1],
[1, 0, 0, 0, 0, 1, 'i', 1, 1, 'a', 1, 'a', 1, 1, 'h', 'h', 'h', 'h', 'h', 1, 0, 1, 's', 's', 1, 'o', 'o', 'o', 'o', 1, 1, 1, 1, 1, 1, 1],
[1, 1, 1, 0, 0, 1, 1, 1, 'o', 1, 1, 1, 1, 1, 1, 1, 1, 'h', 'h', 1, 0, 's', 's', 's', 1, 'o', 'o', 'o', 'o', 'o', 'o', 'o', 1, 0, 0, 0],
[0, 0, 1, 0, 0, 'o', 'o', 'o', 'o', 'o', 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 0, 1, 's', 's', 1, 'o', 'o', 1, 'o', 'o', 'o', 'o', 1, 0, 0, 0],
[0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 'p', 1, 1, 1, 'p', 1, 1, 1, 1, 0, 1, 1, 's', 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 's', 's', 's', 's', 's', 's', 's', 's', 's', 1, 0, 0, 0],
[0, 0, 1, 'i', 1, 1, 1, 1, 1, 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1, 's', 1, 's', 1, 1, 0, 0, 0],
[0, 0, 1, 'i', 1, 1, 'p', 'p', 'p', 1, 1, 1, 'p', 'p', 1, 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 1, 1, 's', 's', 's', 's', 1, 0, 0, 0],
[0, 0, 1, 'i', 'i', 1, 1, 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1, 's', 's', 's', 's', 1, 0, 0, 0],
[0, 0, 1, 'i', 'i', 1, 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 'd', 's', 's', 1, 's', 1, 0, 0, 0],
[0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
]

############################################################
#### The mainloop activates the GUI.
############################################################
root = tk.Tk()
root.title("A* Maze")

game = MazeGame(root, maze, 'inputfile.txt')
root.bind("<KeyPress>", game.move_agent)

root.mainloop()

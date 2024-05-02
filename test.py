import queue
import sys
import re
import tkinter as tk
from PIL import ImageTk, Image, ImageOps
from queue import PriorityQueue

def main():
    if len(sys.argv) != 2:
        print("Usage: python FindPath_.py inputfile.txt")
        sys.exit(1)

    input_file = sys.argv[1]


class Cell:
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.parent = None
        self.priority = None

    def __lt__(self, other):
        return self.f < other.f


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

        self.agent_pos = eval(self.start)
        self.goals_completed = []
        self.goals_failed = []

        self.cell_size = 30
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_maze()
        self.find_and_draw_paths()

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

    def a_star_heuristic(self, pos):
        return (abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1]))

    def dijkstra_heuristic(self, pos):
        return 0

    def find_and_draw_paths(self):
        while not self.delivery_locations.empty():
            self.goal_pos = self.delivery_locations.get()[1]
            path = self.find_path(self.agent_pos, self.goal_pos)
            if path:
                self.goals_completed.append(self.goal_pos)
            else:
                self.goals_failed.append(self.goal_pos)
            self.agent_pos = self.goal_pos
        print("Completed Goals: ", self.goals_completed)
        print("Failed Goals: ", self.goals_failed)

    def find_path(self, start, end):
        open_set = PriorityQueue()
        open_set.put((0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not open_set.empty():
            current = open_set.get()[1]

            if current == end:
                path = self.reconstruct_path(came_from, start, end)
                self.draw_path(path)
                return path

            for next in self.get_neighbors(current):
                new_cost = cost_so_far[current] + 1  # cost is always 1 because all moves are valid

                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    open_set.put((priority, next))
                    came_from[next] = current

        return None

    def get_neighbors(self, pos):
        neighbors = []

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = pos[0] + dx, pos[1] + dy
            if 0 <= new_x < self.rows and 0 <= new_y < self.cols and not self.cells[new_x][new_y].is_wall:
                neighbors.append((new_x, new_y))

        return neighbors

    def reconstruct_path(self, came_from, start, end):
        current = end
        path = []

        while current != start:
            path.append(current)
            current = came_from[current]

        path.append(start)
        path.reverse()
        return path

    def draw_path(self, path):
        for cell in path:
            x, y = cell
            self.canvas.create_oval(y * self.cell_size + 5, x * self.cell_size + 5,
                                    (y + 1) * self.cell_size - 5, (x + 1) * self.cell_size - 5, fill='blue')


def main(file):
    root = tk.Tk()
    root.title("Delivery Agent")

    maze = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 'm', 'm', 'm', 'm', 'm', 1, 'm', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 1, 'm', 'm', 'm', 1, 'm', 'm', 'm', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0],
        [0, 1, 'm', 1, 1, 1, 'm', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
         0],
        [0, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g',
         1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 'm', 'm', 1, 'g', 'g', 'g', 1, 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, 0,
         0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g',
         1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 'm', 'm', 1, 1, 1, 'g', 'g', 1, 'g', 'g', 1, 1, 'g', 1, 'g', 1, 1, 1, 'g', 1, 1, 'g', 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g',
         'g', 0, 0, 1, 'e', 1, 'e', 'e', 1, 'a', 1],
        [1, 0, 0, 1, 'i', 1, 1, 1, 1, 1, 'g', 1, 1, 'g', 1, 1, 'g', 'g', 1, 1, 'g', 1, 'g', 1, 1, 1, 0, 0, 1, 1, 1, 'e',
         'e', 1, 'a', 'a'],
        [1, 0, 0, 1, 'i', 1, 'i', 'i', 1, 'g', 'g', 'g', 'g', 'g', 1, 'g', 'g', 'g', 'g', 1, 'g', 1, 'g', 1, 'i', 1, 0,
         0, 'e', 'e', 1, 'e', 'e', 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 1, 'i', 1, 'g', 'g', 'g', 'g', 'g', 'g', 1, 1, 'g', 1, 1, 1, 1, 1, 1, 'i', 1, 0, 0, 1, 1, 1,
         'e', 'e', 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 'g', 'g', 1, 'g', 'g', 'g', 'g', 1, 'g', 'g', 'g', 1, 'e', 1, 1, 'i', 1, 0, 0, 'e',
         'e', 'e', 'e', 'e', 1, 'a', 'a'],
        [1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 1, 1, 1, 'b', 1, 1, 1, 1, 'g', 'g', 1, 'e', 1, 'i', 'i', 'i', 0, 0, 1, 1,
         1, 1, 1, 1, 'a', 'a'],
        [1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 'b', 'b', 'b', 'b', 'b', 'b', 'b', 1, 'g', 'g', 1, 'e', 1, 1, 1, 1, 0, 0,
         1, 'u', 'a', 'a', 'a', 'a', 'a', 1],
        [1, 0, 0, 1, 'o', 'o', 'o', 'o', 'o', 1, 'b', 'b', 1, 1, 'b', 1, 1, 1, 'g', 'g', 1, 'e', 1, 1, 'e', 'e', 0, 0,
         'u', 'u', 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 'b', 'b', 'b', 1, 'b', 1, 'g', 'g', 'g', 'g', 1, 'e', 1, 'o', 1, 'e', 0, 0,
         1, 'u', 'u', 'u', 'u', 'u', 'u', 1],
        [1, 0, 0, 1, 'o', 1, 1, 1, 'o', 1, 'b', 1, 1, 1, 'b', 1, 1, 1, 1, 1, 0, 0, 'o', 'o', 1, 1, 0, 0, 1, 'u', 'u',
         'u', 'u', 1, 'u', 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'u', 'u', 1, 1, 1, 1,
         1],
        [1, 0, 0, 0, 0, 1, 'i', 1, 1, 'a', 1, 'a', 1, 1, 'h', 1, 1, 1, 'h', 1, 0, 1, 1, 's', 1, 1, 'o', 1, 1, 1, 'u',
         'u', 'u', 'u', 'u', 1],
        [1, 0, 0, 0, 0, 1, 'i', 1, 1, 'a', 1, 'a', 1, 1, 'h', 'h', 'h', 'h', 'h', 1, 0, 1, 's', 's', 1, 'o', 'o', 'o',
         'o', 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 'o', 1, 1, 1, 1, 1, 1, 1, 1, 'h', 'h', 1, 0, 's', 's', 's', 1, 'o', 'o', 'o', 'o', 'o',
         'o', 'o', 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 'o', 'o', 'o', 'o', 'o', 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 0, 1, 's', 's', 1, 'o', 'o',
         1, 'o', 'o', 'o', 'o', 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 'p', 1, 1, 1, 'p', 1, 1, 1, 1, 0, 1, 1, 's', 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
         0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 's', 's', 's', 's', 's', 's', 's', 's',
         's', 1, 0, 0, 0],
        [0, 0, 1, 'i', 1, 1, 1, 1, 1, 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1,
         's', 1, 's', 1, 1, 0, 0, 0],
        [0, 0, 1, 'i', 1, 1, 'p', 'p', 'p', 1, 1, 1, 'p', 'p', 1, 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 1, 1,
         's', 's', 's', 's', 1, 0, 0, 0],
        [0, 0, 1, 'i', 'i', 1, 1, 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd',
         'd', 1, 's', 's', 's', 's', 1, 0, 0, 0],
        [0, 0, 1, 'i', 'i', 1, 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 1, 'p', 1, 'p', 1, 's', 1, 'd',
         'd', 'd', 's', 's', 1, 's', 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    ]

    maze_game = MazeGame(root, maze, file)
    root.mainloop()


if __name__ == "__main__":
    main('inputfile.txt')

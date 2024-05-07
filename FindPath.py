#######################################
#//*** Authors: Michael Wood, Jack Gallagher
#//*** Course Title: CSC 362 Artificial Intelligence Spring 2024
#//*** Submission Date: 5/7/2024
#//*** Assignment: Final Project
#//*** Purpose of Program: Take input values and use the A* or Dijkstra's algorithm to map out optimal paths for a
#//***                     delivery agent from a valid starting location to one or more valid delivery locations.
#######################################

# Import necessary packages
#import queue
import sys
import re
import tkinter as tk
#from PIL import ImageTk, Image, ImageOps
from queue import PriorityQueue

#######################################
# Cell class
#######################################
class Cell:
    def __init__(self, x, y, is_wall=False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.g = float("inf")
        self.h = 0
        self.f = float("inf")
        self.priority = None

    def __lt__(self, other):
        return self.f < other.f

#######################################
# Hospital Map class
#######################################
class HospitalMap:

    # Same ward priority cases
    def adjust_priority_for_ward(self, start_pos):
        # Get the value of the starting location
        start_value = self.matrix[start_pos[0]][start_pos[1]]

        for i in self.delivery:
            x, y = i
            # Set a higher priority for delivery in the same ward
            if self.matrix[x][y] == start_value:
                self.cells[x][y].priority = -7

    def __init__(self, root, map, file):

        # Initialize class variables
        self.root = root
        self.matrix = map
        self.rows = 30
        self.cols = 36

        # Stack for multiple paths found
        self.path_stack = []

        # Set alternating colors for different paths found when drawn
        self.colors = ['blue', 'lightcoral', 'darkorchid', 'chocolate', 'dodgerblue', 'sienna']
        self.color_index = 0

        self.cells = [[Cell(x, y, map[x][y] == 1) for y in range(self.cols)] for x in range(self.rows)]

        # Set variables for input values
        self.algorithm, self.start, self.delivery = self.file_read(file)

        # Error checking for bad start position
        if not self.is_valid_position(self.start):
            print("Invalid starting position!")
            sys.exit(1)

        # Set priority for each cell in matrix
        for i in range(self.rows):
            for j in range(self.cols):
                if map[i][j] == 'u' or map[i][j] == 'e' or map[i][j] == 'o' or map[i][j] == 'b':
                    self.cells[i][j].priority = -5
                elif map[i][j] == 's' or map[i][j] == 'm':
                    self.cells[i][j].priority = -4
                elif map[i][j] == 'h' or map[i][j] == 'p':
                    self.cells[i][j].priority = -3
                elif map[i][j] == 'd' or map[i][j] == 'g':
                    self.cells[i][j].priority = -2
                elif map[i][j] == 'a' or map[i][j] == 'i':
                    self.cells[i][j].priority = -1
                else:
                    self.cells[i][j].priority = 0

        # Set up delivery priority queue and adjust priorities if necessary
        self.delivery_locations = PriorityQueue()
        self.adjust_priority_for_ward(eval(self.start))
        for i in self.delivery:
            self.delivery_locations.put((self.cells[i[0]][i[1]].priority, i))

        # Initialize start state variables
        self.agent_pos = eval(self.start)

        # Initialize stacks for completed and failed goal states (delivery locations)
        self.goals_completed = []
        self.goals_failed = []

        # Initialize cell size and canvas for the output of the map
        self.cell_size = 30
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        self.draw_map()
        self.find_and_draw_paths()

    # Function for error checking start location
    def is_valid_position(self, pos):
        if pos is None:
            return False

        x, y = eval(pos)

        if x >= self.rows or y > self.cols:
            return False

        if self.matrix[x][y] == 1 or self.matrix[x][y] == -2:
            return False

        return True

    # Function for reading the input file
    def file_read(self, file):
        all_lines = []
        with open(file, 'r') as file:
            for line in file:
                all_lines.append(line.strip())

            # Set up variables for the given algorithm, starting location, and delivery location(s)
            algorithm = None
            start = None
            delivery = None

            if all_lines[0].startswith('Delivery algorithm:'):
                algorithm_text = all_lines[0].split(':')[1].strip().lower()
                if algorithm_text == "a*":
                    algorithm = "A*"
                elif algorithm_text == "dijkstra's":
                    algorithm = "Dijkstra's"
                elif algorithm_text == "Dijkstra's":
                    algorithm = "Dijkstra's"
                else:
                    print("Invalid algorithm specified in input file. Please use either 'A*' or 'Dijkstra's' only.")
                    sys.exit(1)

            if all_lines[1].startswith('Start location:'):
                start = re.match(r'Start location:\s*\((\d+),\s*(\d+)\)', all_lines[1])
                if start is not None:
                   start = all_lines[1].split(':')[1].strip()

            if all_lines[2].startswith('Delivery locations:'):
                delivery = re.findall(r'\s*\((\d+),\s*(\d+)\)', all_lines[2])
                delivery = [(int(x), int(y)) for x, y in delivery]

            return algorithm, start, delivery

    def draw_map(self):
        # Set color for each cell in matrix/map
        for x in range(self.rows):
            for y in range(self.cols):
                if self.matrix[x][y] == 'm':
                    color = 'deepskyblue'
                elif self.matrix[x][y] == 'g':
                    color = 'red'
                elif self.matrix[x][y] == 'e':
                    color = 'yellow'
                elif self.matrix[x][y] == 'u':
                    color = 'orange'
                elif self.matrix[x][y] == 'o':
                    color = 'mediumseagreen'
                elif self.matrix[x][y] == 'p':
                    color = 'lightgreen'
                elif self.matrix[x][y] == 's':
                    color = 'lightpink'
                elif self.matrix[x][y] == 'b':
                    color = 'plum'
                elif self.matrix[x][y] == 'h':
                    color = 'lightsalmon'
                elif self.matrix[x][y] == 'a':
                    color = 'silver'
                elif self.matrix[x][y] == 'd':
                    color = 'yellowgreen'
                elif self.matrix[x][y] == 'i':
                    color = 'lightblue'
                elif self.matrix[x][y] == 1:
                    color = 'black'
                elif self.matrix[x][y] == -2:
                    color = 'slategrey'
                else:
                    color = 'white'
                self.canvas.create_rectangle(y * self.cell_size, x * self.cell_size, (y + 1) * self.cell_size,
                                             (x + 1) * self.cell_size, fill=color)

    def a_star_heuristic(self, pos):
        return abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1])

    def dijkstra_heuristic(self, pos):
        return pos*0

    def find_and_draw_paths(self):
        def draw_next_path():
            if not self.delivery_locations.empty():
                self.goal_pos = self.delivery_locations.get()[1]
                path = self.find_path(self.agent_pos, self.goal_pos)
                if path:
                    self.goals_completed.append(self.goal_pos)
                else:
                    self.goals_failed.append(self.goal_pos)
                self.agent_pos = self.goal_pos
                self.root.after(7500, draw_next_path)
            else:
                # Print out completed and failed goals
                print("Completed Goals:")
                for goal in self.goals_completed:
                    print(goal)
                print("Failed Goals:")
                for goal in self.goals_failed:
                    print(goal)

        draw_next_path()

    #####################################################
    # Finding the path with the given input algorithm
    #####################################################
    def find_path(self, start, end):

        # Set priority queue for path
        open_set = PriorityQueue()

        # Enter starting location
        open_set.put((0, start))

        # Use dictionaries for storing nodes and their costs to establish the optimal paths
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
                new_cost = cost_so_far[current] + 1  # goal cost is always 1 for each move

                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost

                    # Calculate cost based on input algorithm
                    if self.algorithm == "Dijkstra's":
                        priority = new_cost
                        open_set.put((priority, next))
                    elif self.algorithm == "A*":
                        priority = new_cost + self.a_star_heuristic(next)
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
        start_color = 'gold'  # Color for the start state
        goal_color = 'green'  # Color for the goal state
        path_color = self.colors[self.color_index % len(self.colors)]  # Get current path color

        # Increment color index for the next path
        self.color_index += 1

        # Define a helper function to draw each circle with a delay
        def draw_circle_with_delay(i):
            if i < len(path):
                x, y = path[i]
                fill_color = start_color if i == 0 else (goal_color if i == len(path) - 1 else path_color)
                self.canvas.create_oval(y * self.cell_size + 5, x * self.cell_size + 5,
                                        (y + 1) * self.cell_size - 5, (x + 1) * self.cell_size - 5,
                                        fill=fill_color)
                # Schedule the next circle drawing after a delay
                self.root.after(100, draw_circle_with_delay, i + 1)

        # Start drawing the circles with delay, starting from index 0
        draw_circle_with_delay(0)


def main(file):
    root = tk.Tk()
    root.title("Delivery Agent")

    # Set up 30 x 36 matrix
    hospital_matrix = [
        [-2, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 'm', 'm', 1, 'm', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 1, 'm', 'm', 'm', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 1, 1, 1, 'm', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 1, 1, 1, 'm', 'm', 1, 'g', 'g', 'g', 1, 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g',1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [1, 1, 1, 1, 'm', 'm', 1, 1, 1, 'g', 'g', 1, 'g', 'g', 1, 1, 'g', 1, 'g', 1, 1, 1, 'g', 1, 1, 'g', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 0, 0, 'e', 'e', 1, 'e', 'e', 1, 'a', 1],
        [1, 0, 0, 1, 'i', 1, 1, 1, 1, 1, 'g', 1, 1, 'g', 1, 1, 'g', 'g', 1, 1, 'g', 1, 'g', 1, 1, 1, 0, 0, 1, 1, 1, 'e', 'e', 1, 'a', 'a'],
        [1, 0, 0, 1, 'i', 1, 'i', 'i', 1, 'g', 'g', 'g', 'g', 'g', 1, 'g', 'g', 'g', 'g', 1, 'g', 1, 'g', 1, 'i', 1, 0, 0, 'e', 'e', 1, 'e', 'e', 1, 'a', 1],
        [1, 0, 0, 0, 1, 1, 1, 'i', 1, 'g', 'g', 'g', 'g', 'g', 'g', 1, 1, 'g', 1, 1, 1, 1, 1, 1, 'i', 1, 0, 0, 1, 1, 1, 'e', 'e', 1, 'a', 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 'g', 'g', 1, 'g', 'g', 'g', 'g', 1, 'g', 'g', 'g', 1, 'e', 1, 1, 'i', 1, 0, 0, 'e', 'e', 'e', 'e', 'e', 1, 'a', 'a'],
        [1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 1, 1, 1, 'b', 1, 1, 1, 1, 'g', 'g', 1, 'e', 1, 'i', 'i', 'i', 0, 0, 1, 1, 1, 1, 1, 1, 'a', 'a'],
        [1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 'b', 'b', 'b', 'b', 'b', 'b', 'b', 1, 'g', 'g', 1, 'e', 1, 1, 1, 1, 0, 0, 1, 'u', 'a', 'a', 'a', 'a', 'a', 1],
        [1, 0, 0, 1, 'o', 'o', 'o', 'o', 'o', 1, 'b', 'b', 1, 1, 'b', 1, 1, 1, 'g', 'g', 1, 'e', 1, 1, 'e', 'e', 0, 0, 'u', 'u', 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 'o', 1, 'o', 1, 'o', 1, 'b', 'b', 'b', 1, 'b', 1, 'g', 'g', 'g', 'g', 1, 'e', 1, 'o', 1, 'e', 0, 0, 1, 'u', 'u', 'u', 'u', 'u', 'u', 1],
        [1, 0, 0, 1, 'o', 1, 1, 1, 'o', 1, 'b', 1, 1, 1, 'b', 1, 1, 1, 1, 1, 0, 0, 'o', 'o', 1, 1, 0, 0, 1, 'u', 'u', 'u', 'u', 1, 'u', 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 'u', 'u', 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 'i', 1, 1, 'a', 1, 'a', 1, 1, 'h', 1, 1, 1, 'h', 1, 0, 1, 1, 's', 1, 1, 'o', 1, 1, 1, 'u', 'u', 'u', 'u', 'u', 1],
        [1, 0, 0, 0, 0, 1, 'i', 1, 1, 'a', 1, 'a', 1, 1, 'h', 'h', 'h', 'h', 'h', 1, 0, 1, 's', 's', 1, 'o', 'o', 'o', 'o', 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 'o', 1, 1, 1, 1, 1, 1, 1, 1, 'h', 'h', 1, 0, 's', 's', 's', 1, 'o', 'o', 'o', 'o', 'o', 'o', 'o', 1, -2, -2, -2],
        [-2, -2, 1, 0, 0, 'o', 'o', 'o', 'o', 'o', 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 0, 1, 's', 's', 1, 'o', 'o', 1, 'o', 'o', 'o', 'o', 1, -2, -2, -2],
        [-2, -2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 'p', 1, 1, 1, 'p', 1, 1, 1, 1, 0, 1, 1, 's', 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2],
        [-2, -2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 's', 's', 's', 's', 's', 's', 's', 's', 's', 1, -2, -2, -2],
        [-2, -2, 1, 'i', 1, 1, 1, 'p', 1, 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1, 's', 1, 's', 1, 1, -2, -2, -2],
        [-2, -2, 1, 'i', 1, 1, 'p', 'p', 'p', 1, 1, 1, 'p', 'p', 1, 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 1, 1, 's', 's', 's', 's', 1, -2, -2, -2],
        [-2, -2, 1, 'i', 'i', 1, 1, 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1, 's', 's', 's', 's', 1, -2, -2, -2],
        [-2, -2, 1, 'i', 'i', 1, 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 'd', 's', 's', 1, 's', 1, -2, -2, -2],
        [-2, -2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2]
    ]

    HospitalMap(root, hospital_matrix, file)
    root.mainloop()

# Accept an input file
if __name__ == "__main__":
    main('inputfile.txt')

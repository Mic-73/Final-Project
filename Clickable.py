import tkinter as tk

def on_click(row, col, destinations):
    # sets up global variables
    global click_count, destinations_string, start

    # iterates the function so that buttons disable after given amount is hit
    click_count += 1

    # sets up the starting point for the first iteration
    if click_count==1:
        print("Starting Point Selected:")
        start=(row,col)
        print (start)

    # initializes the string for the first iteration
    if click_count==2:
        destinations_string = f"({row},{col})"

    # adds a comma in before each added on row and column beyond 1st destination
    else:
        print("Select Destination Point(s):")
        destinations_string += f",({row},{col})"
    print(f"Clicked on cell ({row}, {col})")

    # prints start and destinations and disables ability to click
    if click_count == 1 + destinations:
        print (start)
        print(destinations_string)
        disable_all_buttons()

def write_to_file(algorithm, start_point, destinations):
    # since you cant use ' in format make Dijkstra's a variable
    dijkstra="Dijkstra's"

    # formatting to the input file and writing out to inputfile.txt
    with open("inputfile.txt", "w") as file:
        file.write(f"Delivery algorithm: {dijkstra if algorithm == '1' else 'A*'}\n")
        file.write(f"Start location: {start_point}\n")
        file.write(f"Delivery locations: {destinations}\n")

    # confirms the data was written to our inputfile
    print("Data written to inputfile.txt")



def disable_all_buttons():
    # disables clickable 2d array
    for row in grid:
        for button in row:
            button.config(state=tk.DISABLED)


def create_grid(root, rows, columns, destinations):
    # setting up the 2d grid based on what is in FindPath.py
    grid = []
    for row_index in range(rows):
        current_row = []
        for col_index in range(columns):

            # gives a color based on maze values
            maze_value = maze[row_index][col_index]
            if maze_value == 0:
                color = "white"
            elif maze_value == 1:
                color = "black"
            elif maze_value == -2:
                color = "slategray"
            elif maze_value == "m":
                color = "deepskyblue"
            elif maze_value == "g":
                color = "red"
            elif maze_value == "i":
                color = "lightblue"
            elif maze_value == "o":
                color = "mediumseagreen"
            elif maze_value == "b":
                color = "plum"
            elif maze_value == "p":
                color = "lightgreen"
            elif maze_value == "s":
                color = "lightpink"
            elif maze_value == "d":
                color = "yellowgreen"
            elif maze_value == "a":
                color = "silver"
            elif maze_value == "e":
                color = "yellow"
            elif maze_value == "u":
                color = "orange"
            else:
                color = "white"  # Default color

            # adds the clickable aspect to the 2d array as well as giving it the onclick function which gives opperations
            # when a button is pressed
            cell = tk.Button(root, text="", width=3, height=1, bg=color,
                             command=lambda row=row_index, col=col_index: on_click(row, col,destinations))
            cell.grid(row=row_index, column=col_index)
            current_row.append(cell)
        grid.append(current_row)
    return grid


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Clickable 2D Array")

    # initializes maze used in findpath.py
    maze = [
        [-2, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 'm', 'm', 1, 'm', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 1, 'm', 'm', 'm', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 1, 1, 1, 'm', 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 1, 1, 1, 'm', 'm', 1, 'g', 'g', 'g', 1, 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g', 1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
        [-2, 1, 'm', 'm', 'm', 'm', 'm', 1, 'g', 1, 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 1, 'g', 'g', 'g', 1, 'g',1, -2, -2, -2, -2, -2, -2, -2, -2, -2],
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
        [1, 1, 1, 0, 0, 1, 1, 1, 'o', 1, 1, 1, 1, 1, 1, 1, 1, 'h', 'h', 1, 0, 's', 's', 's', 1, 'o', 'o', 'o', 'o', 'o', 'o', 'o', 1, -2, -2, -2],
        [-2, -2, 1, 0, 0, 'o', 'o', 'o', 'o', 'o', 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 0, 1, 's', 's', 1, 'o', 'o', 1, 'o', 'o', 'o', 'o', 1, -2, -2, -2],
        [-2, -2, 1, 0, 0, 1, 1, 1, 1, 1, 1, 'p', 1, 1, 1, 'p', 1, 1, 1, 1, 0, 1, 1, 's', 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2],
        [-2, -2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 's', 's', 's', 's', 's', 's', 's', 's', 's', 1, -2, -2, -2],
        [-2, -2, 1, 'i', 1, 1, 1, 1, 1, 1, 'p', 'p', 'p', 'p', 'p', 'p', 1, 1, 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1, 's', 1, 's', 1, 1, -2, -2, -2],
        [-2, -2, 1, 'i', 1, 1, 'p', 'p', 'p', 1, 1, 1, 'p', 'p', 1, 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 1, 1, 's', 's', 's', 's', 1, -2, -2, -2],
        [-2, -2, 1, 'i', 'i', 1, 1, 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 1, 'p', 1, 's', 1, 'd', 'd', 1, 's', 's', 's', 's', 1, -2, -2, -2],
        [-2, -2, 1, 'i', 'i', 1, 'p', 'p', 'p', 1, 'p', 'p', 'p', 'p', 'p', 1, 'p', 'p', 1, 'p', 1, 'p', 1, 's', 1, 'd', 'd', 'd', 's', 's', 1, 's', 1, -2, -2, -2],
        [-2, -2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -2, -2, -2] ]

    # initializes necessary variables
    rows = len(maze)
    columns = len(maze[0])
    click_count = 0
    destinations = 0

    # sets up user input for what algorithm user wants and how many destinations
    algo_choice = input("Choose algorithm - 0 for A*, 1 for Dijkstra (note: anything else will be A*): ")
    if algo_choice == '0':
        print("You chose A* algorithm.")
    elif algo_choice == '1':
        print("You chose Dijkstra algorithm.")
    else:
        print("Invalid choice. Defaulting to A* algorithm.")
    while destinations < 1 or destinations > 10:
        destinations = int(input("Enter the number of destinations: "))
        if destinations < 1 or destinations >10:
            print ("Please select a number between 1 and 10")
    print(f"You chose to select {destinations} destinations.")

    # initializing variables
    destinations_string = None
    start = None

    # calls the grid creation function
    grid = create_grid(root, rows, columns, destinations)

    # used for the gui creating loop for the clickable 2d array
    root.mainloop()

    # calls the write to file function after everything is performed
    write_to_file(algo_choice, start, destinations_string)

import sys  as file

"""
This code implements the Iterative Deepening Depth-First Search (IDDFS) algorithm to solve a maze.
IDDFS is a graph traversal algorithm that explores the search space incrementally, limiting the depth of exploration
until a solution is found. It is employed in this context to navigate through a maze represented as a 2D grid.

Key Functions:
- `explore_maze_depth_limited`: Performs Depth-First Search (DFS) with a limited depth to explore the maze.
- `iterative_deepening_dfs`: Iteratively increases the maximum depth of the search until a solution is found or a limit is reached.
- `solve_maze_from_file`: Main function to solve the maze using IDDFS, reading the maze from an input file and writing the result to an output file.

Algorithm Overview:
1. Initialize the starting node and a stack with the initial state.
2. Employ DFS with a limited depth, updating the path and exploring valid neighbors.
3. Prune search paths based on the Manhattan distance heuristic to improve efficiency.
4. Incrementally increase the depth until a solution is found or a predefined limit is reached.

Usage:
- Run the script with command-line arguments: python Project2.py input_file output_file
- The input file contains maze details, and the output file stores the solution path.

Example Input Format:
3 4
B-S R-E B-SE B-SW
R-E B-E R-S R-S
R-N R-NE B-N O

Example Output:
1S 1E 2E 1S
"""


class MazeNode:
    def __init__(self, row, col, explored, path, depth):
        self.row, self.col, self.explored, self.path, self.depth = row, col, explored, path, depth

"""
A dictionary representing possible movement directions and their corresponding changes in row and column.

Directions:
- "N": Move North (Decrease the row by 1)
- "NE": Move Northeast (Decrease the row by 1, increase the column by 1)
- "NW": Move Northwest (Decrease the row by 1, decrease the column by 1)
- "S": Move South (Increase the row by 1)
- "SE": Move Southeast (Increase the row by 1, increase the column by 1)
- "SW": Move Southwest (Increase the row by 1, decrease the column by 1)
- "E": Move East (Increase the column by 1)
- "W": Move West (Decrease the column by 1)
- "O": Origin (No movement, both row and column changes are 0)

Parameters:
- direction (str): The direction for which the movement is requested.

Returns:
- tuple: A tuple representing the changes in row and column associated with the given direction.
          For example, for direction "NE", the tuple is (-1, 1), indicating a decrease in row by 1 and an increase in column by 1.
          For direction "O" (Origin), the tuple is (0, 0), indicating no movement.
"""
directions = {
    "N": (-1, 0),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "S": (1, 0),
    "SE": (1, 1),
    "SW": (1, -1),
    "E": (0, 1),
    "W": (0, -1),
    "O": (0, 0),
}

def get_next_position(direction, row, col):
    """
    Get the next position in the specified direction from the current position.

    Parameters:
        direction (str): The direction to move (N, NE, NW, S, SE, SW, E, W).
        row (int): Current row position.
        col (int): Current column position.

    Returns:
        Tuple[int, int]: The new row and column positions after the move.

    Example:
        row, col = 1, 2  # Example starting position
        next_row = row + di  # 1 + 1 = 2
        next_col = col + dj  # 2 + 1 = 3
         if we start at the position (1, 2) and move Southeast (SE), we will end up at the position (2, 3).

    """
    direction = direction.upper()  # Ensure the direction is in uppercase
    di, dj = directions[direction]  # Get the change in row and column based on the direction
    return row + di, col + dj

def is_valid_bound(row, col, final_rows, final_cols):
    """
    Check if the specified position is within the bounds of the grid.

    Parameters:
        - row (int): The row index of the position.
        - col (int): The column index of the position.
        - final_rows (int): The total number of rows in the grid.
        - final_cols (int): The total number of columns in the grid.

    Returns:
        - bool: True if the position is within bounds, False otherwise.

    Explanation:
    The function checks whether the given row and column indices fall within the
    valid range of the grid. It returns True if the position is within bounds and
    False otherwise.

    Example:
    - If final_rows = 3 and final_cols = 4, the function returns True for
      (row=1, col=2) since it is within the bounds of a 3x4 grid.
    - If final_rows = 3 and final_cols = 4, the function returns False for
      (row=4, col=2) since it is outside the valid row range.
    """
    return 0 <= row < final_rows and 0 <= col < final_cols


def manhattan_distance(row, col, target_row, target_col):
    """
    Calculate the Manhattan distance between two positions in a grid.

    Parameters:
        row (int): The row index of the first position.
        col (int): The column index of the first position.
        target_row (int): The row index of the target position.
        target_col (int): The column index of the target position.

    Returns:
        int: The Manhattan distance between the two positions.

    Additional Notes:
        The Manhattan distance is used in the search algorithm to estimate the remaining
        distance from the current position to the target position. It helps prune the search
        space by considering only paths that are likely to lead to a solution within the
        specified depth limit.

    Example:
        # Example positions
        row, col = 1, 2  # Current position (let's assume)
        target_row, target_col = 2, 3   (let's assume)
        distance = abs(2 - 1) + abs(3 - 2)  # Result: 1 + 1 = 2


    """
    return abs(target_row - row) + abs(target_col - col)


# Depth-First Search (DFS) function to explore the maze
def explore_maze_depth_limited(graph, final_rows, final_cols, max_depth, target_row, target_col):
    """
    Explore the maze using Depth-First Search (DFS) with a limited depth.

    Parameters:
    - graph (List[List[str]]): The maze represented as a 2D grid.
    - final_rows (int): The number of rows in the maze.
    - final_cols (int): The number of columns in the maze.
    - max_depth (int): The maximum depth to explore during the search.
    - target_row (int): The target row representing the destination cell.
    - target_col (int): The target column representing the destination cell.

    Returns:
    - str or None: If a path to the destination is found within the maximum depth, returns a string
      representing the path. Otherwise, returns None.

    Algorithm:
    - The function uses a depth-first search strategy to explore the maze.
    - The search is limited by the specified maximum depth.
    - The algorithm keeps track of the path taken and the explored cells to avoid revisiting the same cells.
    - Pruning is applied based on the Manhattan distance heuristic to improve efficiency.

    Example:

        First Iteration (Depth = 1):
            Current Node: (0, 0) with direction 'S', color 'B', explored set ((0, 0)), path [], depth 1.
            Explores in the 'S' direction, reaches (1, 0), updates path and explored set.
            Prunes based on Manhattan distance heuristic.
            Stack: [MazeNode(1, 0, {(0, 0), (1, 0)}, ['1S'], 2)]
        similarly for 2nd iterartion Stack: [MazeNode(1, 1, {(0, 0), (1, 0), (1, 1)}, ['1S', '2E'], 3)]
        fpr 3rd iteration Stack: [MazeNode(1, 2, {(0, 0), (1, 0), (1, 1), (1, 2)}, ['1S', '2E', '3E'], 4)]
    """

    # Initialize the stack with the starting node
    stack = [MazeNode(0, 0, set((0, 0)), [], 1)]

    while stack:
        current = stack.pop()  # Pop the current node from the stack
        row, col = current.row, current.col
        cur_dir = graph[row][col][2:]  # Extract the direction from the current cell and [['B-S', 'R-E', 'B-SE', 'B-SW'],  then cur_dir= "S"
        cur_color = graph[row][col][:1]  # Extract the color from the current cell and cur_dir="B" for (0,0)

        for count in range(1, max_depth + 1):
            # Move in the current direction
            next_row, next_col = get_next_position(cur_dir, row, col)
            next_pair = (next_row, next_col)  # Create a pair representing the next cell (2,0)

            # Break if we are out of bounds
            if not is_valid_bound(next_row, next_col, final_rows, final_cols):
                break

            next_color = graph[next_row][next_col][:1]  # Extract the color from the next cell

            # Return the final path if the target is reached
            if next_row == target_row and next_col == target_col:
                final_path = list(current.path)
                final_path.append(f"{count}{cur_dir}")
                return ' '.join(final_path)

            # Explore the next cell if conditions are met
            if next_color != cur_color and next_pair not in current.explored and current.depth < max_depth:
                next_explored = set(current.explored) # next_explored : {0,(1,0),(1,1)}.. etc..
                next_explored.add(next_pair)
                next_path = list(current.path) # next_path:['1S','1E']
                next_path.append(f"{count}{cur_dir}") # the  example value in next_path ['1S'] and it will keep increment for same directon and append next direction [2S,2N..]
                next_node = MazeNode(next_row, next_col, next_explored, next_path, current.depth + 1)

                # search based on Manhattan distance heuristic
                if manhattan_distance(next_row, next_col, target_row, target_col) <= max_depth - count:
                    stack.append(next_node)

            row, col = next_row, next_col

    return None  # Return None if the depth exceeds the maximum depth
# Function to Perform Iterative Deepening Depth-First Search (IDDFS)
def iterative_deepening_dfs(graph, rows, cols):
    """
    Perform Iterative Deepening Depth-First Search (IDDFS) to explore the maze incrementally.

    Parameters:
    - graph (List[List[str]]): The maze represented as a 2D grid.
    - rows (int): The number of rows in the maze.
    - cols (int): The number of columns in the maze.

    Returns:
    - str or None: If a solution path is found, returns a string representing the path. Otherwise, returns None.

    Algorithm:
    - The function incrementally increases the maximum depth of the search until a solution
        is found or a predefined limit is reached.
    - Calls the DFS function with the current maximum depth to explore the maze.
    - Returns the result if a solution is found within the depth limit.
    """
    max_depth = 1  # Initialize the maximum depth for the search
    max_depth_limit = rows * cols  # Set a reasonable limit for the maximum depth to avoid infinite looping and max depth_lime for 3, 4 = 12
    target_row, target_col = rows - 1, cols - 1 # target_col: 3 target_row:2 from above assumption

    # Continue the search until the maximum depth reaches the limit
    while max_depth <= max_depth_limit:
        # Call the depth-limited exploration function
        result = explore_maze_depth_limited(graph, rows, cols, max_depth, target_row, target_col)
        if result: # Check if a solution path is found within the current depth limit
            return result  # Return the result if a solution is found
        max_depth += 1  # Increment the maximum depth for the next iteration

    return "No solution found within the depth limit."


# Main function to solve the maze
def solve_maze_from_file(graph, rows, cols):
    """
    Solve the maze using Iterative Deepening Depth-First Search (IDDFS).

    Parameters:
    - graph (List[List[str]]): The maze represented as a 2D grid.
    - rows (int): The number of rows in the maze.
    - cols (int): The number of columns in the maze.

    Returns:
    - str or None: If a solution path is found, returns a string representing the path. Otherwise, returns None.
    """

    return iterative_deepening_dfs(graph, rows, cols)


def main():
    """
    Main entry point for the maze-solving program.

    Reads the maze from an input file, solves it, and writes the result to an output file.

    Command-line arguments:
    - sys.argv[1]: Input file containing the maze.
    - sys.argv[2]: Output file to write the result.
    """

    # Check if the correct number of command-line arguments is provided
    if len(file.argv) != 3:
        print("Usage: python script.py input_file output_file")
        file.exit(1)

    input_file = file.argv[1]  # Input file containing the maze
    output_file = file.argv[2]  # Output file to write the result

    #a try-except block to handle potential exceptions during file operations

    try:
        # Open the input file for reading
        with open(input_file, "r") as f:
            rows, cols = [int(i) for i in f.readline().split()]   # Read the first line to get the number of rows and columns // rows: 3cols: 4
            graph = [f.readline().split() for _ in range(rows)] # Read the maze grid from the remaining lines and graph=  [['B-S', 'R-E', 'B-SE', 'B-SW'], ['R-E', 'B-E', 'R-S', 'R-S'], ['R-N', 'R-NE', 'B-N', 'O']]

        result = solve_maze_from_file(graph, rows, cols) # Call the solve_maze_from_file function to find a solution path ( and result is 1S 1E 2E 1S)

        with open(output_file, 'w') as out: # Open the output file for writing
            out.write(result)

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except ValueError:
        print("Error: Invalid maze format in the input file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()



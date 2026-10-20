import matplotlib as mp 
import matplotlib.pyplot as plt 
import numpy as np
import random 
import cv2

# Load and process maze image
maze = cv2.imread("maze.png")
if maze is None:
    raise FileNotFoundError("Could not find maze.png")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# White pixels are paths; black pixels are walls
walkable = gray > 127
height, width = walkable.shape


def find_endpoints(walkable):
    h, w = walkable.shape
    openings = []

    for x in range(w):
        if walkable[0, x]:
            openings.append((0, x))
        if walkable[h - 1, x]:
            openings.append((h - 1, x))

    for y in range(1, h - 1):
        if walkable[y, 0]:
            openings.append((y, 0))
        if walkable[y, w - 1]:
            openings.append((y, w - 1))

    openings = list(dict.fromkeys(openings))

    if len(openings) < 2:
        raise ValueError(
            "Could not detect two border openings. "
            "Set start and end manually."
        )

    return openings[0], openings[-1]


start, end = find_endpoints(walkable)

# Directions: down, right, up, left
DIRECTIONS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
]


chosen_algorithm = input("Choose a maze-solving algorithm: 1.Las Vegas 2.Backtracking: ")
if chosen_algorithm == "1":
    las_vegas_path = las_vegas(walkable, start, end)
    save_solution(image, las_vegas_path, "maze_las_vegas.png")
elif: chosen_algorithm === "2":
    backtracking_path = backtracking(walkable, start, end)
    save_solution(image, backtracking_path, "maze_backtracking.png")
else:
    print("Invalid choice. Please pick from the chosen algorithm las vegas or backtracking.")



# Backtracking

def backtracking(walkable, start, end):
    """Solve using a fixed direction order."""
    h, w = walkable.shape
    visited = np.zeros((h, w), dtype=bool)
    path = []

    def dfs(y, x):
        if not (0 <= y < h and 0 <= x < w):
            return False

        if not walkable[y, x] or visited[y, x]:
            return False

        visited[y, x] = True
        path.append((y, x))

        if (y, x) == end:
            return True

        # Always use the same order
        for dy, dx in DIRECTIONS:
            if dfs(y + dy, x + dx):
                return True

        # Dead end: undo the current path choice
        path.pop()
        return False

    if dfs(*start):
        return path

    return None





# def las_vegas(maze):
#     attempts = 200

def las_vegas(walkable, start, end):
    h, w = walkable.shape
    visited = np.zeros((h, w), dtype=bool)
    path = []

    def dfs(y, x):
        if not (0 <= y < h and 0 <= x < w):
            return False

        if not walkable[y, x] or visited[y, x]:
            return False

        visited[y, x] = True
        path.append((y, x))

        if (y, x) == end:
            return True

        # Randomize direction order
        directions = DIRECTIONS.copy()
        random.shuffle(directions)

        for dy, dx in directions:
            if dfs(y + dy, x + dx):
                return True

        # Dead end: undo the current path choice
        path.pop()
        return False

    if dfs(*start):
        return path

    return None


# ---------------------------------
# 4. Draw and save each solution
# ---------------------------------

def save_solution(original, path, filename):
    if path is None:
        print(f"No solution found for {filename}")
        return

    result = original.copy()

    # Draw the solution in red
    for y, x in path:
        result[y, x] = (0, 0, 255)

    cv2.imwrite(filename, result)
    print(f"Saved: {filename}")
    print(f"Path length: {len(path)} pixels")



# # When applying a Las Vegas approach, the end conditions are either you found
# # the exit (successful) or you have completed 200 steps without finding the exit (unsuccessful).
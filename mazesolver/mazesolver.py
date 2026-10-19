import matplotlib as mp 
import matplotlib.pyplot as plt 
import numpy as np 

# Load the maze image
maze = plt.imread("maze.png")

# Convert the image to grayscale if it has RGB/RGBA channels
if maze.ndim == 3:
    maze = maze[:, :, :3].mean(axis=2)

# Convert pixels into a binary maze:
# 1 = wall (black), 0 = path (white)
maze = (maze < 0.5).astype(int)

# Display the maze in the terminal
for row in maze:
    print("".join("██" if pixel else "  " for pixel in row))


chosen_algorithm = input("How would you like to solve the maze. Pick Las Vegas or Backtracking: ")
if chosen_algorithm is "las vegas":
    las_vegas()
elif: chosen_algorithm is "backtracking":
    backtracking()
else:
    print("Wrong option chosen. Please pick from the chosen algorithm las vegas or backtracking.")



def backtracking():



def las_vegas():
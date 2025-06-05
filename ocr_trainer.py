import tkinter as tk
from datetime import datetime
import numpy as np
import pickle
import pandas as pd

'''
Collect trainng data by asking the user to draw
the digits 0 to 9 and storing a representation of them
in a pandas dataframe.
'''

# Current target digit being drawn
target = 0

# Total samples colledcted
count = 0

# Grid for drawing
grid = np.zeros((100,100))

# List of all samples
data = []

# Convert the grid into a 10x10 grid by counting how many
# pixels are in each subgrid.  Saved as a dictionary with keys
# b##.  Also store the target digit.
def process_grid(grid, target):
    block = 0
    processed = dict()
    for i in range(10):
        for j in range(10):
            processed[f"b{block}"]= np.sum(grid[i*10:(i+1)*10,j*10:(j+1)*10])
            block += 1
    processed["target"] = target
    return processed

# Clear the drawing surface
def clear():
    global grid
    grid = np.zeros((100,100))
    canvas.delete("all")

# Submit a sample.  
def submit():
    global target, count, grid
    # Process the drawing to the 10x10 format and append
    # to the list
    processed = process_grid(grid, target)
    data.append(processed)

    # Save the current samples as a pandas dataframe
    df = pd.DataFrame(data)
    with open("ocr.dat", "wb") as f:
        pickle.dump(df, f)

    # Update the prompt to request a new number
    target = (target + 1) % 10
    count += 1

    # Clear the grid
    grid = np.zeros((100,100))
    canvas.delete("all")
    draw_label.config(text=f"Draw: {target}")
    count_label.config(text=f"Count: {count}")

# Draw when the mouse moves over the grid
def on_drag(event):
    global grid
    x = event.x
    y = event.y
    if (x >= 1 and x <= 100) and (y >= 1 and y <= 100):
        grid[x-1,y-1] = 1
        canvas.create_oval(x, y, x+1, y+1, fill="red", outline="red")

# Load the current samplee data
with open("ocr.dat", "rb") as f:
    df = pickle.load(f)

    # Convert the pandas dataframe into a list of
    # records (dictionaries)
    data = df.to_dict(orient="records")
    count = len(data)
    target = 0

# GUI Definition
root = tk.Tk()
root.title("OCR Trainer")
root.minsize(300,300)
root.maxsize(300,300)

tk.Label(root, text="OCR Trainer").pack()
draw_label = tk.Label(root, text=f"Draw: {target}")
draw_label.pack()

canvas = tk.Canvas(root, width=100, height=100, bg="white")
canvas.pack(padx=10, pady=10)
canvas.bind("<B1-Motion>", on_drag)

tk.Button(root, text="Clear", command=clear).pack()
tk.Button(root, text="Submit", command=submit).pack()
count_label = tk.Label(root, text=f"Count: {count}")
count_label.pack()

root.mainloop()
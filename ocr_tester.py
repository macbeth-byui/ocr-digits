import tkinter as tk
import numpy as np
import pickle
import pandas as pd

'''
Create a GUI tester that allows the user to draw a digit
and then the value is predicted using the current model (ocr.mdl)
'''

# Grid for drawing
grid = np.zeros((100,100))

# Predicted Value
prediction = None

# Convert the grid into a 10x10 grid by counting how many
# pixels are in each subgrid.  Saved as a dictionary with keys
# b##
def process_grid(grid):
    block = 0
    processed = dict()
    for i in range(10):
        for j in range(10):
            # Filtered Sum
            processed[f"b{block}"]= np.sum(grid[i*10:(i+1)*10,j*10:(j+1)*10])
            block += 1
    return processed

# Clear the drawing space
def clear():
    global grid, prediction
    grid = np.zeros((100,100))
    canvas.delete("all")
    prediction = None
    prediction_label.config(text=f"Prediction: {prediction}")

# Run the current drawing through the model to 
# arrive at a prediction
def test():
    global grid, prediction
    # Convert grid into the 10x10 format
    # and store as a pandas data frame for
    # consumption by the model prediction
    processed = [process_grid(grid)]
    sample = pd.DataFrame(processed)
    prediction = model.predict(sample)
    prediction_label.config(text=f"Prediction: {prediction}")

# Draw when the mouse moves over the grid
def on_drag(event):
    global grid
    x = event.x
    y = event.y
    if (x >= 1 and x <= 100) and (y >= 1 and y <= 100):
        grid[x-1,y-1] = 1
        canvas.create_oval(x, y, x+1, y+1, fill="red", outline="red")

# Open the model
with open("ocr.mdl","rb") as f:
    model = pickle.load(f)

# GUI Definition
root = tk.Tk()
root.title("OCR Tester")
root.minsize(300,300)
root.maxsize(300,300)

tk.Label(root, text="OCR Tester").pack()
prediction_label = tk.Label(root, text=f"Prediction: {prediction}")
prediction_label.pack()

canvas = tk.Canvas(root, width=100, height=100, bg="white")
canvas.pack(padx=10, pady=10)
canvas.bind("<B1-Motion>", on_drag)

tk.Button(root, text="Clear", command=clear).pack()
tk.Button(root, text="Test", command=test).pack()

root.mainloop()
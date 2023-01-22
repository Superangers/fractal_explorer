# Imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msgbox

from fractions import Fraction
import time

import render_core as RC

# =========================================
# Variables
paramsDefaultValues = {"pos": [-0.68, 0.0], "scale": 5.4, "res": [1000, 1000], "maxIter": 80, "C": (0.0, 0.0)}
params = paramsDefaultValues.copy()
moveScale = .01
bgColor = "#8a5f5f"

# ==========================================================================
# Define Functions
def reduceRatio(ratio):
    ratio = (Fraction(ratio[0], ratio[1]).numerator, Fraction(ratio[0], ratio[1]) )
    if ratio[0] > ratio[1]:
        return ( (ratio[0] - ratio[1] )+1, 1)
    else:
        return ( (ratio[1] - ratio[0])+1, ratio[0] )

def getBounds(position: tuple=(0, 0), ratio: tuple=(1, 1), scale: float=1):
    ratio = reduceRatio(ratio)
    return  ( ( (-ratio[0]/2)*scale + position[0], (-ratio[1]/2)*scale + position[1] ),
              ( ( ratio[0]/2)*scale + position[0], ( ratio[1]/2)*scale + position[1]) )

#=============================================================
# Def OptionsWindow buttons functions
# - Movement
def updatePositionText():
  actualPosLabel.config(text = "Actual position:\nx="+str(params["pos"][0])+"\ny="+str(params["pos"][1]))

def upButton():
    global params
    params["pos"][1] -= params["scale"] * moveScale
    updatePositionText()

def downButton():
    global params
    params["pos"][1] += params["scale"] * moveScale
    updatePositionText()

def leftButton():
    global params
    params["pos"][0] -= params["scale"] * moveScale
    updatePositionText()

def rightButton():
    global params
    params["pos"][0] += params["scale"] * moveScale
    updatePositionText()

# - Set position from entries
def setManualPos():
    global params
    try:
        x = float(manualPosXVar.get())
    except ValueError:
        msgbox.showerror("Set Position: Value Error", "X is not a number!\nPosition must be a float with no letter/special character")
        return
    try:
        y = float(manualPosYVar.get())
    except ValueError:
        msgbox.showerror("Set Position: Value Error", "Y is not a number!\nPosition must be a float with no letter/special character")
        return
    
    params["pos"] = (x, y)
    updatePositionText()

# - Set scale from slider
def setScaleValue(event):
    global params
    params["scale"] = scaleSlider.get()
    scaleLabel.config(text="Set scale:\nActual value: "+str(scaleSlider.get()))

# - Set scale from entry
def setScaleManually():
    global params
    try:
        scale = float(manualScaleVar.get())
    except ValueError:
        msgbox.showerror("Set scale: Value Error", "Value is not a number!\nPosition must be a float with no letter/special character")
        return
    scaleSlider.set(scale)
    scaleLabel.config(text="Set scale:\nActual value: "+str(scale))
    params["scale"] = scale

# - Set max iterations from slider
def setMaxIterValue(event):
    global params
    params["maxIter"] = maxIterSlider.get()
    maxIterLabel.config(text="Set max iterations:\n(high = slower but more detailed)\nActual value: "+str(maxIterSlider.get()))

# - Set max iterations from entry
def setMaxIterManually():
    global params
    try:
        maxIter = float(manualMaxIterVar.get())
    except ValueError:
        msgbox.showerror("Set max iteration: Value Error", "Value is not a number!\nPosition must be a float with no letter/special character")
        return
    maxIterSlider.set(maxIter)
    maxIterLabel.config(text="Set max iterations:\n(high = slower but more detailed)\nActual value: "+str(maxIter))
    params["maxIter"] = maxIter

# 
def onFractalsChanged(event):
    print("fractal changed to "+fractalsMenu.get())
    if fractalsMenu.get() == "julia set":
        juliaValuesFrame.grid()
    else:
        juliaValuesFrame.grid_remove()

# - Render
def renderButton():
    global params, scaleSlider
    # Set params

    renderWindow = tk.Toplevel()

    renderWindow.geometry("500x500")
    renderWindow.resizable(width=False, height=False)

    renderCanvas = tk.Canvas(renderWindow, width=1000, height=1000)
    renderCanvas.pack()
    params["C"] = (juliaValue1Slider.get(), juliaValue2Slider.get())
    
    # Render image
    start = time.time()
    # - Best bounds: (-4.9, -4.2),(.7, 1.4)
    renderImage = RC.render(params, fractalsMenu.get())
    end = time.time()

    # Set render time in title
    renderWindow.title("Fractal Explorer - Render: "+str(round(end-start, 3))+" seconds")

    renderCanvas.create_image(0, 0, image=renderImage)

    renderWindow.mainloop()

# ===================================================================================
# Init Option Window
optionsWindow = tk.Tk()
optionsWindow.title("Fractal Explorer - Options")
optionsWindow.geometry("400x500")
optionsWindow.minsize(400, 500)
optionsWindow.config(bg=bgColor)

# --------------------------------------------
# RIGHT COLUMN --------------------------------
rightColumnFrame = tk.Frame(optionsWindow, bg=bgColor)
rightColumnFrame.grid(row=0, column=1, rowspan=3, sticky="N")

# Chose fractal scrolling menu
# - Frame
fractalsMenuFrame = tk.Frame(rightColumnFrame)
fractalsMenuFrame.grid(row=0, column=0, pady=10)

# - Label
fractalsMenuLabel = tk.Label(fractalsMenuFrame, text="Chose the fractal")
fractalsMenuLabel.grid(row=0, column=0)
# - Get fractals name
fractalsName = []
for name, infos in RC.fractalsInfos.items():
    fractalsName.append(name)
# - Combobox (tkinter's scrolling menu)
# - - string var for trace
currentFractal = tk.StringVar(value="mandelbrot")
currentFractal.trace("w", onFractalsChanged)

fractalsMenu = ttk.Combobox(fractalsMenuFrame, values=fractalsName, state="readonly", width=14)
fractalsMenu.bind("<<ComboboxSelected>>", onFractalsChanged)
fractalsMenu.current(0)
fractalsMenu.grid(row=1, column=0)

# 
# - Render Button Frame
renderFrame = tk.Frame(rightColumnFrame, background="#8a5f5f")
renderFrame.grid(row=1, column=0)

# - Render Button
renderButton = tk.Button(renderFrame, text="Render!", command=renderButton, width=12, height=2)
renderButton.grid(row=0, column=0)

#
# - Julia set values
juliaValuesFrame = tk.Frame(rightColumnFrame, bg=bgColor)
juliaValuesFrame.grid(row=2, column=0, rowspan=2)
# - - Values label
juliaValuesLabel = tk.Label(juliaValuesFrame, text="Set Julia set Values", bg=bgColor)
juliaValuesLabel.grid(row=0, column=0)

# - - Value1 Label
juliaValue1Label = tk.Label(juliaValuesFrame, text="Value 1:", bg=bgColor)
juliaValue1Label.grid(row=1, column=0)
# - - Value1 slider
juliaValue1Slider = tk.Scale(juliaValuesFrame, from_=-2, to=2, resolution=-1, sliderlength=10, length=140, bg=bgColor, orient="horizontal")
juliaValue1Slider.grid(row=2, column=0)

# - - Value2 Label
juliaValue2Label = tk.Label(juliaValuesFrame, text="Value 2:", bg=bgColor)
juliaValue2Label.grid(row=3, column=0)
# - - Value2 slider
juliaValue2Slider = tk.Scale(juliaValuesFrame, from_=-2, to=2, resolution=-1, sliderlength=10, length=140, bg=bgColor, orient="horizontal")
juliaValue2Slider.grid(row=4, column=0)

# Remove Julia Values from grid
juliaValuesFrame.grid_remove()

# --------------------------------
# Movement Buttons  ↑ ← ↓ →
# - Buttons Frame
movementFrame = tk.Frame(optionsWindow, bg=bgColor)
movementFrame.grid(row=0, column=0)
# - Infos Label
mvtButtonsLabel = tk.Label(movementFrame, text="Move the fractal", bg=bgColor)
mvtButtonsLabel.grid(row=0, column=0)
# - Actual position Label
actualPosLabel = tk.Label(movementFrame, bg=bgColor)
actualPosLabel.grid(row=1, column=0)
updatePositionText()

# - Buttons
# - - Buttons frame
mvtButtonsFrame = tk.Frame(movementFrame,bg=bgColor)
mvtButtonsFrame.grid(row=2, column=0)

# up
upButton = tk.Button(mvtButtonsFrame, text=" up ", command=upButton, width=4, height=2)
upButton.grid(row=1, column=1)
# left
leftButton = tk.Button(mvtButtonsFrame, text="left", command=leftButton, width=4, height=2)
leftButton.grid(row=2, column=0)
# down
downButton = tk.Button(mvtButtonsFrame, text="down", command=downButton, width=4, height=2)
downButton.grid(row=2, column=1)
#right
rightButton = tk.Button(mvtButtonsFrame, text="right", command=rightButton, width=4, height=2)
rightButton.grid(row=2, column=2)

# ----------------------------------------
# Set position manually entries + button
# - Frame
manualPosFrame = tk.Frame(optionsWindow, bg=bgColor)
manualPosFrame.grid(row=1, column=0)

# - Infos Label
manualPosLabel = tk.Label(manualPosFrame, text="Set position manually\n! Only floats are allowed !", bg=bgColor)
manualPosLabel.grid(row=0, column=0)

# - SubLabel frame
manualPosSubFrame = tk.Frame(manualPosFrame, bg=bgColor)
manualPosSubFrame.grid(row=1, column=0)

# - Entries
# Entries frame
manualPosEntriesFrame = tk.Frame(manualPosSubFrame, bg=bgColor)
manualPosEntriesFrame.grid(row=0, column=0)
# - - X Entry
# Ifno label
manualPosXLabel = tk.Label(manualPosEntriesFrame, text="X:", bg=bgColor)
manualPosXLabel.grid(row=0, column=0)
# Entry
manualPosXVar = tk.StringVar(value="0")
manualPosXEntry = tk.Entry(manualPosEntriesFrame, textvariable=manualPosXVar, width=14)
manualPosXEntry.grid(row=0, column=1)

# - - Y Entry
# Info label
manualPosYLabel = tk.Label(manualPosEntriesFrame, text="Y:", bg=bgColor)
manualPosYLabel.grid(row=1, column=0)
# Entry
manualPosYVar = tk.StringVar(value="0")
manualPosYEntry = tk.Entry(manualPosEntriesFrame, textvariable=manualPosYVar, width=14)
manualPosYEntry.grid(row=1, column=1)
# ---
# Set position button
setManualPosButton = tk.Button(manualPosSubFrame, text="Set Position", command=setManualPos, height=2)
setManualPosButton.grid(row=0, column=1, padx=5)

# ----------------------------------------
# Scale slider
# - Frame
scaleSliderFrame = tk.Frame(optionsWindow, bg=bgColor)
scaleSliderFrame.grid(row=2, column=0, pady=10)
# - Label
scaleLabel = tk.Label(scaleSliderFrame, text="Set fractal scale\nActual value: "+str(paramsDefaultValues["scale"]), bg=bgColor)
scaleLabel.grid(row=0, column=0)
# - Slider
scaleSlider = tk.Scale(scaleSliderFrame, from_=0, to=6, resolution=-1, orient="horizontal", sliderlength=10, length=200, bg=bgColor)
scaleSlider.bind("<ButtonRelease-1>", setScaleValue)
scaleSlider.set(paramsDefaultValues["scale"])
scaleSlider.grid(row=1, column=0, padx=10)

# - Entry frame
scaleEntryFrame = tk.Frame(scaleSliderFrame, bg=bgColor)
scaleEntryFrame.grid(row=2, column=0, pady=4)
# - Label
scaleEntryLabel = tk.Label(scaleEntryFrame, text="Set manually:", bg=bgColor)
scaleEntryLabel.grid(row=0, column=0)
# - Entry
manualScaleVar = tk.StringVar(value=str(paramsDefaultValues["scale"]))
scaleEntry = tk.Entry(scaleEntryFrame, textvariable=manualScaleVar)
scaleEntry.grid(row=0, column=1)
# - Button
scaleEntryButton = tk.Button(scaleEntryFrame, text="Set", command=setScaleManually)
scaleEntryButton.grid(row=0, column=2, padx=4)

# -----------------------------------------
# Max iterations slider
# - Frame
maxIterSliderFrame = tk.Frame(optionsWindow, bg=bgColor, pady=10)
maxIterSliderFrame.grid(row=3, column=0)
# - Label
maxIterLabel = tk.Label(maxIterSliderFrame, text="Set max iterations:\n(high = slower but more detailed)\nActual value: "
                                                                                                    +str(paramsDefaultValues["maxIter"]), bg=bgColor)
maxIterLabel.grid(row=0, column=0)
# - Slider
maxIterSlider = tk.Scale(maxIterSliderFrame, from_=1, to=1000, resolution=-1, orient="horizontal", sliderlength=10, length=200, bg=bgColor)
maxIterSlider.bind("<ButtonRelease-1>", setMaxIterValue)
maxIterSlider.set(paramsDefaultValues["maxIter"])
maxIterSlider.grid(row=1, column=0, padx=10)

# - Entry frame
maxIterEntryFrame = tk.Frame(maxIterSliderFrame, bg=bgColor)
maxIterEntryFrame.grid(row=2, column=0, pady=4)
# - Label
maxIterEntryLabel = tk.Label(maxIterEntryFrame, text="Set manually:", bg=bgColor)
maxIterEntryLabel.grid(row=0, column=0)
# - Entry
manualMaxIterVar = tk.StringVar(value=str(paramsDefaultValues["maxIter"]))
maxIterEntry = tk.Entry(maxIterEntryFrame, textvariable=manualMaxIterVar)
maxIterEntry.grid(row=0, column=1)
# - Button
maxIterEntryButton = tk.Button(maxIterEntryFrame, text="Set", command=setMaxIterManually)
maxIterEntryButton.grid(row=0, column=2, padx=4)


# -----------------------------
#afficher la fenetre
optionsWindow.mainloop()


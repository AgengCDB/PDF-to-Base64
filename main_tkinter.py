import pandas as pd
import os
os.system("title Hello")
# import re

import tkinter as tk
from tkinter import ttk, filedialog, TOP, Entry, Label, StringVar
import tkinter.scrolledtext as tkscrolled
# import base64
import threading
import random

from tkinterdnd2 import *


import base64
from myvar import strIconPNG

# COLOR
COL_GREEN = "#7DC343"
COL_DARK_GREEN = "#4C7B24"
COL_ORANGE = "#EC722E"
COL_DARK_ORANGE = "#B34C1C"
COL_BLUE = "#64A2D8"
COL_DARK_BLUE = "#3D6DAB"
COL_YELLOW = "#EED842"
COL_DARK_YELLOW = "#B7AD2D"

colors_light = [
    "#7DC343", "#EC722E", "#64A2D8", "#EED842"
]
random_color = random.choice(colors_light)

root = TkinterDnD.Tk()
root.geometry("350x100")
root.title("")

root.configure(bg=random_color)

# Decode the base64 data
icon_data = base64.b64decode(strIconPNG())

# Set the icon
icon_photo = tk.PhotoImage(data=icon_data)
root.iconphoto(True, icon_photo)

# ==================================================================================
# start all
# ==================================================================================

# ==================================================================================
# start frame input
# ==================================================================================

f_input = tk.Frame(root)
f_input.pack(padx=10, pady=10, side=tk.TOP, expand=True, fill=tk.BOTH)
f_input.configure()

nameVar = tk.StringVar()

lab1 = tk.Label(f_input, text="Drag and drop file in the entry box")
lab1.pack(side=tk.TOP, padx=10, pady=10, fill="x")

# start entry widget

entryWidget = tk.Entry(f_input, 
                    state='readonly')
entryWidget.pack(side=tk.TOP, padx=10, pady=(0, 10), fill="both")

paths = []

def get_path(event):
    # pathLabel.configure(text = event.data)
    global paths
    paths = root.tk.splitlist(event.data)
    lab_input.configure(text="\n".join(paths), justify="left")

entryWidget.drop_target_register(DND_ALL)
entryWidget.dnd_bind("<<Drop>>", get_path)

# end entry widget

lab_input = tk.Label(f_input, text="Input file")
lab_input.pack(side=TOP, padx=10, pady=10, fill="both")

# ==================================================================================
# start frame button
# ==================================================================================

f_button = tk.Frame(f_input)
f_button.pack(padx=10, pady=(0, 10), expand=True)
f_button.configure()



    


root.mainloop()
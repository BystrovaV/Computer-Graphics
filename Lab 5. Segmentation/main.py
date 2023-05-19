import tkinter as tk
from MainFrame import MainFrame
import matplotlib
import KirusBack
import Segmentation
matplotlib.use('TkAgg')

window = tk.Tk()
window.title("Отсечение отрезков")

step_frame_results = MainFrame()
step_frame = step_frame_results.root_frame
step_frame.pack()

tk.mainloop()
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkHelper import *


import clientf.tk_frames.upload_page as upload_page


def main(frame, func_dict, logged, top, *args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)

    global _top1, _w1
    _top1 = root
    _w1 = upload_page.upload_win(frame, func_dict, logged, _top1)
    root.mainloop()

# MAP
def apartments_map(entry, map_lunch, func_dict):
    win = win_creator(root, 4, 4, 1, 1, "Map", 700, 700)
    frame = Frame(win)

    win.grid_columnconfigure(0, weight=1)
    win.grid_rowconfigure(0, weight=1)

    frame.grid(row=0, column=0, sticky=N+S+E+W)

    # map
    path = "pics/map.png"
    mpath = os.path.abspath(path)


    cvs_lst = []

    # add image on top
    canvas = tk.Canvas(frame)
    canvas.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
    canvas.configure(background="#f0ece9")
    canvas.configure(borderwidth="2")
    canvas.configure(insertbackground="black")
    canvas.configure(relief='groove')

    im = tk.PhotoImage(master=canvas, file=mpath)
    canvas.create_image(0, 0, image=im, anchor=NW)
    canvas.image = im

    canvas.bind("<Button-1>", lambda event, entry=entry, map_lunch=map_lunch: print_coords(event, get_x_y(canvas, event)[0], get_x_y(canvas, event)[1], entry, map_lunch, canvas))

    # confirm button
    btn_ok = Button(win, text="OK", command=win.destroy, font=def_font)
    btn_ok.grid(row=4, column=0)

def get_x_y(canvas, event):
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    return x, y


def print_coords(event, x, y, entry, map_lunch, canvas):
    # delete old text
    canvas.delete("text")
    # add new text
    canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="red", tags="text")

    value = "(%d, %d)" % (x, y)
    entry.delete(0, END)
    entry.insert(0, value)
    event.widget.config(bg="black")
    map_lunch.config(text="Map %s" % value)





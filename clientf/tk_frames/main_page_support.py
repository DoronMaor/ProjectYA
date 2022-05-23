import os
import tkinter as tk
from tkHelper import *

import clientf.tk_frames.main_page as main_page

def main(frame, logged, func_dict, mes, mes2, *args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    # check if window is already exists and if so, destroy it
    _w1 = main_page.root(frame, logged, func_dict, _top1)

    # bind function to close window
    root.protocol("WM_DELETE_WINDOW", lambda: func_dict["on_close"](root))

    if mes:
        pop_up(_top1, mes)
    if mes2:
        pop_up(_top1, mes2)

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

    att_file = func_dict["get_attractions"]()

    if att_file is not None and att_file[0] is not None:
        fill_map(func_dict, canvas, att_file)

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



def fill_map(func_dict, canvas, att_file, *args):
    # clear the canvas shapes
    canvas.delete("del")

    for line in att_file:
        # each line is like this: NAME=(x,y)
        name = line.split("=")[0]
        coords = line.split("=")[1].split(",")
        #remove the \n
        coords[1] = coords[1][:-1]
        # remove the brackets
        coords[0] = coords[0][1:]
        coords[1] = coords[1][:-1]
        # convert to int
        x = int(coords[0])
        y = int(coords[1])
        # add the shape
        #canvas.create_rectangle(x-10, y-10, x+10, y+10, fill="purple", tags="del")
        # add the text
        #canvas.create_text(x+15, y+40, text=name, tags="del")

        canvas.create_rectangle(x - 5 + 15, y + 20, x + 155, y + 25 + 15, fill="white", tag="del")
        canvas.create_text(x + 15, y + 20, text=name, font=def_font, anchor=NW, tag="del")
        canvas.create_rectangle(x, y, x + 17, y + 17, fill="purple", tag="del")






    """
    apartments = func_dict["get_all_apartments"]()
    for apartment in apartments:
        if apartment.is_available_here(date):
            col = "#00ff00"
        else:
            col = "#ff0000"
        x, y = apartment.area
        if x is not None and y is not None:
            canvas.create_rectangle(x-5+15, y+25, x+125, y+20+15, fill="white", tag="del")
            canvas.create_text(x+15, y+20, text="{} - {}".format(apartment.name, apartment.id), font=def_font, anchor=NW, tag="del")
            canvas.create_rectangle(x, y, x + 17, y + 17, fill=col, tag="del")
    """
    return True









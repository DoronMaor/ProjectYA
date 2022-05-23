import datetime

from tkHelper import *
import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import clientf.tk_frames.admin_page as admin_page

def main(frame, func_dict, logged_user, top, *args):
    '''Main entry point for the application.'''
    global root
    root = top
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    _w1 = admin_page.win_admin(frame, func_dict, logged_user, _top1)
    root.mainloop()


def generate_txt_apartments(func_dict, txt_place, *args):
    """
    Generate txt file with all of the apartments and stats.
    The File looks like this:
    ####
    APARTMENTS REPORT
    ####
    --- [apartment's name] ---
    * [apartment's id]
    * [apartment's number of rooms]
    * [apartment's number of guests]
    * [apartment's area]
    * [apartment's description]
    * [apartment's rating]
    * [apartment's owner's id]
    * = STATS =
    * [apartment's number of lifetime reservations]
    * [apartment's number of lifetime guests]
    * [apartment's past reservation to reviews]
    * [total money made]
    --- [apartment's name] ---
    .
    .
    .
    """

    file_path = "temps/gen_apartments.txt"
    full_path = os.path.abspath(file_path)

    file = open(full_path, "w")
    file.write("####\nAPARTMENTS REPORT\n####\n")
    for apartment in func_dict["get_all_apartments"]():
        file.write("\n")
        file.write("--- [{}] ---\n".format(apartment.name))
        file.write("* ID: {}\n".format(apartment.id))
        file.write("* Number of rooms: {}\n".format(apartment.number_of_rooms))
        file.write("* Number of guests: {}\n".format(apartment.number_of_beds))
        file.write("* Area: {}\n".format(str(apartment.area)))
        file.write("* Description: {}\n".format(apartment.description))
        file.write("* Rating: {}\n".format(apartment.star_rating))
        file.write("* Owner's ID: {}\n".format(apartment.owner))
        file.write("== STATS ==\n")
        file.write("* Life time reservations: {}\n".format(apartment.get_number_of_reservations()))
        file.write("* Life time guests:{}\n".format(apartment.get_number_of_guests()))
        file.write("* Past reservations to reviews ratio:[{}]\n".format(apartment.get_reservations_reviews_ratio()))######
        file.write("* Total money made:{} ILS \n".format(apartment.get_total_money()))
        file.write("--- [{}] ---\n".format(apartment.name))
        file.write("\n")
    file.write("####\nAPARTMENTS REPORT END\n####\n")
    file.write("Available on: {}".format(full_path))
    file.close()

    # insert the txt file into the text widget
    txt_place.delete(1.0, END)
    txt_place.insert(END, open(full_path, "r").read())
    return True


def generate_txt_popular_dates(func_dict, txt_place, *args):
    """
    Generate txt file with all of the popular dates.
    The File looks like this:
    ####
    POPULAR DATES REPORT
    ####
    --- [apartment's name] ---
    * [apartment's id]
    * [6 most popular dates]
    --- [apartment's name] ---
    .
    .
    .

    ###
    Global Stats
    ####
    * [6 most popular dates]
    * [The date with the most reservations]
    * [The date with the most guests]
    """
    file_path = "temps/gen_populardates.txt"
    full_path = os.path.abspath(file_path)

    file = open(full_path, "w")
    file.write("####\nPOPULAR DATES REPORT\n####\n")
    for apartment in func_dict["get_all_apartments"]():
        file.write("\n")
        file.write("--- [{}] ---\n".format(apartment.name))
        file.write("* ID: [{}]\n".format(apartment.id))
        file.write("* Popular dates: [{}]\n".format(apartment.get_6_most_popular_reservation_dates()))
        file.write("--- [{}] ---\n".format(apartment.name))
        file.write("\n")

    file.write("###"
               "\nGLOBAL STATS"
               "\n####"
               )
    file.write("\n* Popular dates: [{}]\n".format(func_dict["get_popular_dates"]()))
    file.write("* Date with the most reservations: [{}]\n".format(func_dict["get_most_reservations"]()))
    file.write("* Date with the most guests: [{}]\n".format(func_dict["get_most_guests"]()))

    file.write("####\nPOPULAR DATES REPORT END\n####\n")
    file.write("Available on: {}".format(full_path))
    file.close()


    # insert the txt file into the text widget
    txt_place.delete(1.0, END)
    txt_place.insert(END, open(full_path, "r").read())
    return True


def generate_money_report(func_dict, txt_place, *args):
    """
    Generate txt file with all of the money made each month.
    The File looks like this:
    ####
    MONEY REPORT
    ####
    --- [apartment's name] ---
    * [apartment's id]
    * [money made each month]
    --- [apartment's name] ---
    .
    .
    .
    """
    file_path = "temps/gen_money.txt"
    full_path = os.path.abspath(file_path)

    file = open(full_path, "w")
    file.write("####\nMONEY REPORT\n####\n")
    for apartment in func_dict["get_all_apartments"]():
        file.write("\n")
        file.write("--- [{}] ---\n".format(apartment.name))
        file.write("* ID: {}\n".format(apartment.id))
        mon = dict_to_string(apartment.get_money_made_each_month())
        file.write("* Money made each month: {}\n".format(mon if mon else "No money made"))
        file.write("--- [{}] ---\n".format(apartment.name))
        file.write("\n")

    file.write("####\nMONEY REPORT END\n####\n")
    file.write("Available on: {}".format(full_path))
    file.close()

    # insert the txt file into the text widget
    txt_place.delete(1.0, END)
    txt_place.insert(END, open(full_path, "r").read())


def dict_to_string(dict):
    """
    Convert a dictionary to a string.
    """
    string = ""
    for key in dict:
        string += "{}: {}".format(key, dict[key]) + " |"
    return string



# MAP
def apartments_map(func_dict, *args):
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
    canvas.configure(background="#d9d9d9")
    canvas.configure(borderwidth="2")
    canvas.configure(insertbackground="black")
    canvas.configure(relief='groove')

    im = tk.PhotoImage(master=canvas, file=mpath)
    canvas.create_image(0, 0, image=im, anchor=NW)
    canvas.image = im

    fill_map(func_dict, canvas, datetime.date.today())

    date_entry = Entry(win)
    date_entry.grid(row=1, column=0, sticky=N+S+E+W)
    date_entry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))


    # confirm button
    btn_ok = Button(win, text="OK", command=lambda: fill_map(func_dict, canvas, date_entry.get()), font=def_font)
    btn_ok.grid(row=4, column=0)


def fill_map(func_dict, canvas, date, *args):
    # clear the canvas shapes
    canvas.delete("del")

    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except:
        date = date


    apartments = func_dict["get_all_apartments"]()
    for apartment in apartments:
        if apartment.is_available_here(date):
            col = "#00ff00"
        else:
            col = "#ff0000"
        x, y = apartment.area
        if x is not None and y is not None:
            canvas.create_rectangle(x - 5 + 15, y + 20, x + 155, y + 25 + 15, fill="white", tag="del")
            canvas.create_text(x + 15, y + 20, text="{} - {}".format(apartment.name, apartment.id), font=def_font, anchor=NW, tag="del")
            canvas.create_rectangle(x, y, x + 17, y + 17, fill=col, tag="del")

    return True


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


def set_attractions(func_dict, file_path, top, *args):
    try:
        # open file
        file = open(file_path, "r")
        # read file
        lines = file.readlines()
        # close file
        file.close()
    except:
        pop_up(top, "File not found!")
        return
    # create list
    attractions = []
    # add lines to list
    for line in lines:
        attractions.append(line.strip())
    # return list
    # send attractions to the server
    try:
        func_dict["set_attractions"](attractions, top)
        return True
    except:
        pop_up(top, "Couldn't set attractions!")
        return
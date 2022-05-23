#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 7.3
#  in conjunction with Tcl version 8.6
#    May 03, 2022 04:16:55 PM +0300  platform: Windows NT
#    May 03, 2022 04:43:01 PM +0300  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

import clientf.tk_frames.rating_page as rating_page

def main(apartment_id, frame, func_dict, top, *args):
    '''Main entry point for the application.'''
    global root
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    # Creates a toplevel widget.
    global _top1, _w1
    _top1 = root
    # _w1 = rating_page.Toplevel1(_top1)
    _w1 = rating_page.win_lvl(apartment_id, frame, func_dict, _top1)
    root.mainloop()


def update_rating_canvas(rating_scale, score_canvas):
    '''Updates the canvas with the new rating.'''
    score_canvas.delete('all')

    x = score_canvas.winfo_width() / 2
    y = score_canvas.winfo_height() / 3
    green = '#00ff00'
    red = '#ff0000'
    yellow = '#ffff00'
    orange = '#ffa500'
    black = '#000000'
    col_list = [black, red, orange, yellow, green]
    index = int(rating_scale.get()) if int(rating_scale.get()) < len(col_list) else len(col_list) - 1
    score_canvas.create_text(x, y, text=str(rating_scale.get()), fill=col_list[index], font=('Verdana', 36, 'bold'))

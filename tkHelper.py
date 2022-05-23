from tkinter import *


def pop_up(root, message):
    """
    Creates a popup window with the message.
    """

    win = win_creator(root, 3, 7, 3, 8)
    win.wm_attributes("-topmost", 1)

    txt = Label(win, text=message, font=def_font, bg=bg_color, fg=txt_color)
    txt.pack(fill="both", expand="YES")
    btn = Button(win, text="OK", command=win.destroy, font=def_font)
    btn.pack(side=LEFT, expand="YES", fill="both")


def popup_function(root, message, function, function_txt):
    """
    Creates a popup window with the message.
    """

    win = win_creator(root, 3, 7, 3, 8)
    win.wm_attributes("-topmost", 1)

    txt = Label(win, text=message, font=def_font, bg=bg_color, fg=txt_color)
    txt.pack(fill="both", expand="YES")
    btn = Button(win, text=function_txt, command=lambda : (win.destroy(), function(), ), font=def_font)
    btn.pack(side=LEFT, expand="YES", fill="both")


def win_creator(root, minx, miny, maxx, maxy, title="Window", xx=None, yy=None):
    """
    Simplifies the creation of windows - min x,y and max x,y.
    """
    if xx is None and yy is None:
        x = root.winfo_screenwidth()
        y = root.winfo_screenheight()
        win = Toplevel(root)
        win.minsize(int(x / minx), int(y / miny))
        win.maxsize(int(x / maxx), int(y / maxy))
    else:
        win = Toplevel(root)
        win.minsize(xx, yy)
        win.maxsize(xx, yy)


    win.title = title
    return win

def root_window():
    """
    The function creates the root window.
    """
    root = Tk()
    x = root.winfo_screenwidth()
    y = root.winfo_screenheight()
    root.minsize(int(x / 2), int(y / 2))
    root.maxsize(int(x / 2), int(y / 2))
    root.title("Client")

    return root


# region fonts and colors
def_font = "Calibri"
txt_color = "#F6F7EB"
bg_color = "#393E41"
top_color = "#3F88C5"
color1 = "#E94F37"
color2 = "#44BBA4"
color3 = "#FEA63C"
color4 = "#76B0D9"
color5 = "#FCC717"
color6 = "#B48EAD"
color7 = "#88B7E0"
color8 = "#E17055"
color9 = "#5FACF3"
color10 = "#F0A3A3"
# endregion

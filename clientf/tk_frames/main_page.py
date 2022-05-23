#! /usr/bin/env python
import tkinter as tk
import clientf.tk_frames.main_page_support as mps

class root:
    def __init__(self, frame, logged, func_dict, top=None, **kw):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        title_font = ("Verdana", 16, 'bold')
        def_font = ("Verdana", 12,)
        but_font = ("Arial Black", 11)


        top.geometry("1160x760+411+110")
        top.minsize(120, 1)
        top.maxsize(3604, 1061)
        top.resizable(1,  1)
        top.title("TempHouse")
        top.configure(background="#FFFAFA")

        self.top = top

        self.frame_top = tk.Frame(self.top)
        self.frame_top.place(relx=0.0, rely=0.0, relheight=0.1, relwidth=1.0)
        self.frame_top.configure(relief='groove')
        self.frame_top.configure(borderwidth="2")
        self.frame_top.configure(relief="groove")
        self.frame_top.configure(background="#d9d9d9")


        self.btn_login = tk.Button(self.frame_top)
        self.btn_login.place(relx=0.0, rely=0.0, height=76, width=167)
        self.btn_login.configure(activebackground="#ececec")
        self.btn_login.configure(activeforeground="#000000")
        self.btn_login.configure(background="#de549a")
        self.btn_login.configure(compound='left')
        self.btn_login.configure(cursor="fleur")
        self.btn_login.configure(disabledforeground="#a3a3a3")
        self.btn_login.configure(foreground="#000000")
        self.btn_login.configure(highlightbackground="#d9d9d9")
        self.btn_login.configure(highlightcolor="black")
        self.btn_login.configure(pady="0")
        self.btn_login.configure(relief="solid")
        self.btn_login.configure(font=but_font)
        if not logged:
           self.btn_login.configure(text='''Login/Signup'''
                                    ,command=lambda: func_dict.get("login_window")(self.top))
        else:
            self.btn_login.configure(text='''Logout'''
                                     , command=lambda: func_dict.get("login_window")(self.top))


        self.btn_profile = tk.Button(self.frame_top)
        self.btn_profile.place(relx=0.853, rely=0.0, height=76, width=188)
        self.btn_profile.configure(activebackground="#ececec")
        self.btn_profile.configure(activeforeground="#000000")
        self.btn_profile.configure(background="#de549a")
        self.btn_profile.configure(compound='left')
        self.btn_profile.configure(disabledforeground="#a3a3a3")
        self.btn_profile.configure(foreground="#000000")
        self.btn_profile.configure(highlightbackground="#d9d9d9")
        self.btn_profile.configure(highlightcolor="black")
        self.btn_profile.configure(pady="0")
        self.btn_profile.configure(relief="solid")
        self.btn_profile.configure(font=but_font)
        self.btn_profile.configure(text='''Profile''')
        self.btn_profile.configure(command=lambda: func_dict.get("profile_window")(self.frame_top, self.top))

        self.Label1 = tk.Label(self.frame_top)
        self.Label1.place(relx=0.138, rely=0.0, height=76, width=841)
        self.Label1.configure(anchor='center')
        self.Label1.configure(background="#eaddda")
        self.Label1.configure(compound='center')
        self.Label1.configure(cursor="fleur")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(relief="groove")
        self.Label1.configure(font=title_font)
        self.Label1.configure(text='''TempHouse''')

        self.frame2 = tk.Frame(self.top)
        self.frame2.place(relx=0.0, rely=0.092, relheight=0.401, relwidth=1.005)
        self.frame2.configure(relief='groove')
        self.frame2.configure(borderwidth="2")
        self.frame2.configure(relief="groove")
        self.frame2.configure(background="#d9d9d9")

        self.Label2 = tk.Label(self.frame2, wraplength=1140, justify='left')
        self.Label2.place(relx=0.0, rely=0.0, height=305, width=1166)
        self.Label2.configure(anchor='nw')
        self.Label2.configure(background="#f0ece9")
        self.Label2.configure(compound='left')
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(font=def_font)
        self.Label2.configure(text='''How are we? 435 345 435 235 2345 545624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546624 624 6254 62546 2546 256 2546 2546 25465 ff''')

        self.order_frame = tk.Frame(self.top)
        self.order_frame.place(relx=0.0, rely=0.487, relheight=0.521
                , relwidth=1.003)
        self.order_frame.configure(relief='groove')
        self.order_frame.configure(borderwidth="2")
        self.order_frame.configure(relief="groove")
        self.order_frame.configure(background="#f0ece9")

        self.price_lbl = tk.Label(self.order_frame)
        self.price_lbl.place(relx=0.0, rely=0.126, height=59, width=1163)
        self.price_lbl.configure(anchor='w')
        self.price_lbl.configure(background="#f0ece9")
        self.price_lbl.configure(compound='left')
        self.price_lbl.configure(cursor="fleur")
        self.price_lbl.configure(disabledforeground="#a3a3a3")
        self.price_lbl.configure(foreground="#000000")
        self.price_lbl.configure(font=def_font)
        self.price_lbl.configure(text='''Maximum price per day [ILS]:''')

        self.price_entry = tk.Entry(self.order_frame)
        self.price_entry.place(relx=0.24, rely=0.177, height=30, relwidth=0.06)
        self.price_entry.configure(background="white")
        self.price_entry.configure(cursor="fleur")
        self.price_entry.configure(disabledforeground="#a3a3a3")
        self.price_entry.configure(font=def_font)
        self.price_entry.configure(foreground="#000000")
        self.price_entry.configure(insertbackground="black")

        self.checkin_lbl = tk.Label(self.order_frame)
        self.checkin_lbl.place(relx=0.0, rely=0.278, height=69, width=1163)
        self.checkin_lbl.configure(anchor='w')
        self.checkin_lbl.configure(background="#ebddda")
        self.checkin_lbl.configure(compound='left')
        self.checkin_lbl.configure(disabledforeground="#a3a3a3")
        self.checkin_lbl.configure(foreground="#000000")
        self.checkin_lbl.configure(font=def_font)
        self.checkin_lbl.configure(text='''Check-in date [yyyy-mm-dd]:''')

        self.sdate_entry = tk.Entry(self.order_frame)
        self.sdate_entry.place(relx=0.24, rely=0.303, height=40, relwidth=0.141)

        self.sdate_entry.configure(background="white")
        self.sdate_entry.configure(disabledforeground="#a3a3a3")
        self.sdate_entry.configure(font=def_font)
        self.sdate_entry.configure(foreground="#000000")
        self.sdate_entry.configure(insertbackground="black")

        self.Label4 = tk.Label(self.order_frame)
        self.Label4.place(relx=0.0, rely=0.0, height=56, width=1173)
        self.Label4.configure(anchor='center')
        self.Label4.configure(background="#f8d5c1")
        self.Label4.configure(compound='left')
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(font=title_font)
        self.Label4.configure(text='''Order''')

        self.checkout_lbl = tk.Label(self.order_frame)
        self.checkout_lbl.place(relx=0.396, rely=0.303, height=41, width=700)
        self.checkout_lbl.configure(activebackground="#f9f9f9")
        self.checkout_lbl.configure(activeforeground="black")
        self.checkout_lbl.configure(anchor='w')
        self.checkout_lbl.configure(background="#ebddda")
        self.checkout_lbl.configure(compound='left')
        self.checkout_lbl.configure(cursor="fleur")
        self.checkout_lbl.configure(disabledforeground="#a3a3a3")
        self.checkout_lbl.configure(foreground="#000000")
        self.checkout_lbl.configure(highlightbackground="#d9d9d9")
        self.checkout_lbl.configure(highlightcolor="black")
        self.checkout_lbl.configure(font=def_font)
        self.checkout_lbl.configure(text='''Check-out date [yyyy-mm-dd]:''')

        self.edate_entry = tk.Entry(self.order_frame)
        self.edate_entry.place(relx=0.645, rely=0.303, height=40, relwidth=0.141)

        self.edate_entry.configure(background="white")
        self.edate_entry.configure(cursor="fleur")
        self.edate_entry.configure(disabledforeground="#a3a3a3")
        self.edate_entry.configure(font="TkFixedFont")
        self.edate_entry.configure(foreground="#000000")
        self.edate_entry.configure(highlightbackground="#d9d9d9")
        self.edate_entry.configure(highlightcolor="black")
        self.edate_entry.configure(insertbackground="black")
        self.edate_entry.configure(selectbackground="blue")
        self.edate_entry.configure(font=def_font)
        self.edate_entry.configure(selectforeground="white")

        self.people_lbl = tk.Label(self.order_frame)
        self.people_lbl.place(relx=0.0, rely=0.429, height=69, width=1163)
        self.people_lbl.configure(activebackground="#f9f9f9")
        self.people_lbl.configure(activeforeground="black")
        self.people_lbl.configure(anchor='w')
        self.people_lbl.configure(background="#f0ece9")
        self.people_lbl.configure(compound='left')
        self.people_lbl.configure(disabledforeground="#a3a3a3")
        self.people_lbl.configure(foreground="#000000")
        self.people_lbl.configure(highlightbackground="#d9d9d9")
        self.people_lbl.configure(highlightcolor="black")
        self.people_lbl.configure(font=def_font)
        self.people_lbl.configure(text='''Number of visitors:''')

        self.people_entry = tk.Entry(self.order_frame)
        self.people_entry.place(relx=0.24, rely=0.48, height=30, relwidth=0.06)
        self.people_entry.configure(background="white")
        self.people_entry.configure(disabledforeground="#a3a3a3")
        self.people_entry.configure(font="TkFixedFont")
        self.people_entry.configure(foreground="#000000")
        self.people_entry.configure(highlightbackground="#d9d9d9")
        self.people_entry.configure(highlightcolor="black")
        self.people_entry.configure(insertbackground="black")
        self.people_entry.configure(selectbackground="blue")
        self.people_entry.configure(font=def_font)
        self.people_entry.configure(selectforeground="white")

        self.place_entry = tk.Entry(self.order_frame)
        self.map_lunch = tk.Button(self.order_frame)
        self.map_lunch.place(relx=-0.009, rely=0.581, height=84, width=1177)
        self.map_lunch.configure(activebackground="#ececec")
        self.map_lunch.configure(activeforeground="#000000")
        self.map_lunch.configure(background="#ebddda")
        self.map_lunch.configure(compound='left')
        self.map_lunch.configure(disabledforeground="#a3a3a3")
        self.map_lunch.configure(foreground="#000000")
        self.map_lunch.configure(highlightbackground="#d9d9d9")
        self.map_lunch.configure(highlightcolor="black")
        self.map_lunch.configure(pady="0")
        self.map_lunch.configure(font=but_font)
        self.map_lunch.configure(text='''Map''')
        self.map_lunch.configure(command=lambda: mps.apartments_map(self.place_entry, self.map_lunch, func_dict))

        self.btn_search = tk.Button(self.order_frame)
        self.btn_search.place(relx=0.0, rely=0.783, height=84, width=1167)
        self.btn_search.configure(activebackground="#ececec")
        self.btn_search.configure(activeforeground="#000000")
        self.btn_search.configure(background="#244244")
        self.btn_search.configure(compound='left')
        self.btn_search.configure(disabledforeground="#a3a3a3")
        self.btn_search.configure(foreground="#ffffff")
        self.btn_search.configure(highlightbackground="#d9d9d9")
        self.btn_search.configure(highlightcolor="#ffffff")
        self.btn_search.configure(pady="0")
        self.btn_search.configure(font=but_font)
        self.btn_search.configure(text='''Find It!''')
        # run search_server function from the client
        self.btn_search.configure(command=lambda: func_dict.get("search_server")(self.price_entry.get(), self.sdate_entry.get(),
                                                      self.edate_entry.get(),
                                                      self.place_entry.get(),
                                                      self.people_entry.get(), self.frame2, self.top))

def start_up(frame, logged, func_dict, mes=None, mes2=None):
    mps.main(frame, logged, func_dict, mes, mes2)






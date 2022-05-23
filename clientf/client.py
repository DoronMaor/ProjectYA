import os
import time
from socket import *
import pickle
import Apartment
from tkHelper import *
import datetime
import _thread
import clientf.tk_frames.main_page as m_page
import clientf.tk_frames.apartments as apt_page
import clientf.tk_frames.order_page as order_page
import clientf.tk_frames.profile_page as profile_page
import clientf.tk_frames.login_page as login_page
import clientf.tk_frames.rating_page as rating_page
import clientf.tk_frames.admin_page as admin_page
import clientf.tk_frames.search_page as search_page
import clientf.tk_frames.upload_page as upload_page


def main_screen(frame=None, win=None, mes=None):
    # Main screen
    global logged_user, today
    if win:
        win.destroy()

    if today != datetime.date.today():
        mes2 = "Admin has changed the date to " + str(today) + "!"
    else:
        mes2=None

    p = m_page.start_up(frame, logged_user, func_dict, mes, mes2)


def search_server(price, sdate, edate, place, people, frame=None, top=None):
    """
    Sends the search request to the server.
    """
    global search_details
    price = 101 if price == "" else int(price)
    sdate = datetime.date.fromisoformat("2022-01-01") if not sdate else datetime.date.fromisoformat(sdate)
    edate = datetime.date.fromisoformat("2023-01-01") if not edate else datetime.date.fromisoformat(edate)
    place = "(1,1)" if place == "" else place.replace(" ", "")
    people = 1 if people == "" else int(people)

    search_details = [sdate, edate, people]

    # sending the request to the server
    client_socket.send(pickle.dumps(("search", price, sdate, edate, place, people)))

    # receiving the response from the server
    while True:
        try:
            data = client_socket.recv(1024*16)
            data = pickle.loads(data)
        except:
            return
        if data[0] == "search_results":
            break
    houses = data[1]

    # if the response is empty, the server did not find any houses
    if not houses:
        pop_up(frame, "No houses found!")
    else:
        # if the response is not empty, the server found some houses
        search_apartments_window(houses, place, frame, top)


def search_apartments_window(houses, area, frame=None, win=None):
    p = apt_page.start_up(frame, logged_user, func_dict, houses, area, None, win)


def get_pics(ap_id):
    """
    Sends the request to the server to get the pictures of the apartment
    """
    th = "temps/%d.png" % ap_id
    error_path = "pics/error.png"
    client_socket.send(pickle.dumps(("get_pics", ap_id)))
    full_path = os.path.abspath(th)
    error_path = os.path.abspath(error_path)

    if os.path.exists(th):
        return (full_path, error_path)

    while True:
        try:
            data = client_socket.recv(902 * 15)
            data = pickle.loads(data)
            if data[0] == "pics":
                break
        except:
            pass
    try:
        with open(th, "wb") as f:
            for d in data[1]:
                f.write(d)
    except:
        pass

    return (full_path, error_path)


def connect_to_server():
    """
    Connects to the server.
    """
    global today

    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 7777))
    # receiving the response from the server
    s.send(pickle.dumps(("get_date", None)))
    while True:
        try:
            data = s.recv(902 * 15)
            data = pickle.loads(data)
        except:
            return
        if data[0] == "date":
            break
    today = data[1]
    return s


def profile_window(frame=None, win=None, mes=None):
    """
    Opens the profile window.
    """
    if logged_user is None:
        pop_up(frame, "You must be logged in to view your profile!")
        return
    if logged_user:
        silent_login(log_username ,log_pass)

    p = profile_page.start_up(frame, logged_user, func_dict, mes)


def home_button(frame, top=None):
    """
    Function that creates the home button
    :param frame: frame where the button will be placed
    :param logged: if the user is logged in or not
    :return: None
    """
    btn_home = Button(frame, text="Home",
                      command=lambda: main_screen(frame, top), font=def_font)
    btn_home.pack(side=LEFT, expand="YES", fill="both")


def book_window(frame, top, s_apartment, houses):
    global search_details, func_dict
    s_apartment = find_house_by_name(s_apartment, houses)
    search_details.append(s_apartment)
    days = (search_details[1] - search_details[0]).days
    cur_time = datetime.datetime.now()
    client_socket.send(pickle.dumps(("start_rent", s_apartment.id, cur_time)))
    b = order_page.start_up(s_apartment, search_details, days, func_dict, logged_user, client_socket)


def listen_to_afk(s_apartment, button, top):
    while True:
        try:
            data = client_socket.recv(21000)
            data = pickle.loads(data)
            time.sleep(0.1)
            if data[0] == "afk_rent":
                button.config(state="disabled")
                afk_window(top, s_apartment)
                break
            elif data[0] == "pics":
                pass
            elif data[0] == None:
                break
            elif data[0] == "end":
                break
        except:
            break


def afk_window(top, s_apartment):
    global search_details, func_dict
    if logged_user is None:
        pop_up(top, "You have been afk for too long. Your reservation for %s has been canceled. " % s_apartment.name)
    else:
        popup_function(top, "You have been afk for too long. Your reservation for %s has been canceled. "
                            "\n In the meantime, please rate the apartments you have visited them in the past." % s_apartment.name, profile_window, "Profile")


def book_room(s_apartment, reservation, top):
    client_socket.send(pickle.dumps(("book", s_apartment.id, reservation, logged_user.id if logged_user else None)))
    frame = Frame(top, bg=bg_color)
    frame.pack(fill="both", expand="YES")
    txt = Label(frame, text="Your booking has been sent to the server. Please hold on to this page", font=def_font,
                bg=bg_color, fg=txt_color)
    txt.pack(fill="both", expand="YES")
    while True:
        print(1)
        time.sleep(0.25)
        response = client_socket.recv(1024 * 10)
        print(2)
        response = pickle.loads(response)
        try:
            print(response)
            if response[0] == "booked" or response[0] == "not_booked":
                print(5)
                break
        except:
            print(4)

    txt.destroy()
    if response[0] == "booked":
        txt = Label(top, text="Your room has been booked!", font=def_font, bg=bg_color, fg=txt_color)
        txt.pack(fill="both", expand="YES")
    else:
        txt = Label(top, text="An error occurred. Please try again.", font=def_font, bg=bg_color, fg=txt_color)
        txt.pack(fill="both", expand="YES")

    txt.pack(fill="both", expand="YES")
    btn_ok = Button(top, text="OK", command=top.destroy, font=def_font)
    btn_ok.pack(side=LEFT, expand="YES", fill="both")


def find_house_by_name(name, houses):
    """
    Finds a house by its name.
    """

    for house in houses:
        if house.name == name:
            return house


def login_window(top):
    """
    Opens the login window.
    """
    global logged_user

    if logged_user is not None:
        logged_user = None
        pop_up(top, "You have been logged out.")
        top.destroy()
        main_screen(None, None, "You have been logged in.")

    else:
        l = login_page.start_up(func_dict, top)


def login_server(username, password, frame, top):
    """
    Logs the user in the server.
    """
    global logged_user, log_username, log_pass
    login_state = False

    # send the username and password to the server
    try:
        client_socket.send(pickle.dumps(("login", username, password)))
    except:
        pop_up(top, "An error occurred. Please try again.")
        frame.destroy()

    # receive the response from the server
    response = ""
    try:
        response = client_socket.recv(4096*5)
        response = pickle.loads(response)
    except:
        pop_up(top, "An error occurred. Please try again.")
        return

    # if the response is "login_success"
    try:
        if response[0] == "login_success":
            logged_user = response[1]
            log_username = username
            log_pass = password
            login_state = True
            frame.destroy()
            top.destroy()
            main_screen(None, None, "You have been logged in.")
        else:
            pop_up(top, "Wrong username or password.")
    except:
        pop_up(top, "An error occurred. Please try again.")


def silent_login(username, password):
    """
    Logs the user in the server.
    """
    global logged_user
    login_state = False

    # send the username and password to the server
    try:
        client_socket.send(pickle.dumps(("login", username, password)))
    except:
        return False

    # receive the response from the server
    response = ""
    try:
        response = client_socket.recv(4069)
        response = pickle.loads(response)
    except:
        return False

    # if the response is "login_success"
    if response[0] == "login_success":
        logged_user = response[1]
        login_state = True
    else:
        return False


def register_server(username, password, email, id, age, ref_code, frame, top):
    # send the info to the server
    try:
        client_socket.send(pickle.dumps(("register", username, password, email, age, ref_code, id)))
    except:
        pop_up(top, "An error occurred. Please try again.")

    # receive the response from the server
    response = ""
    try:
        response = client_socket.recv(4069)
        response = pickle.loads(response)
    except:
        pop_up(top, "An error occurred. Please try again.")

    # if the response is "register_success"
    if response[0] == "success":
        frame.destroy()
        top.destroy()
        main_screen(None, None, response[1])
    else:
        pop_up(top, response[1])


def get_apartment_by_id(id):
    """
    Sends a request to the server to get an apartment by its id.
    """
    client_socket.send(pickle.dumps(("find_apartment_by_id", id)))
    response = ""
    try:
        response = client_socket.recv(4069)
        response = pickle.loads(response)
    except:
        return None

    return response


def cancel_reservation(user_id, apartment_id, frame, top):
    """
    Sends a request to the server to cancel a reservation.
    """

    apartment_id = apartment_id.split('[')[1].split(']')[0]
    try:
        apartment_id = int(apartment_id)
    except:
        pop_up(top, "An error occurred. Please try again.")
        return

    client_socket.send(pickle.dumps(("cancel_reservation", user_id, apartment_id)))
    response = ""
    try:
        response = client_socket.recv(4069)
        response = pickle.loads(response)
    except:
        return None



    if response[0] == "reserv":
        top.destroy()
        profile_window(None, None, response[1])


def rate_apartment_window(apartment_id ,frame, top, test):
    # is apartment_id contains " [Rated]"
    if " [Rated]" in apartment_id:
        pop_up(top, "You have already rated this apartment.")
        return

    apartment_id = apartment_id.split('[')[1].split(']')[0]

    r = rating_page.start_up(apartment_id, frame, func_dict, top)


def rate_apartment_server(apartment_id, comment, stars, top):
    """
    Sends a request to the server to rate an apartment.
    """
    user_id = logged_user.id

    try:
        apartment_id = int(apartment_id)
    except:
        pop_up(top, "An error occurred. Please try again.")
        return

    dbu_rating = [apartment_id, stars, comment]
    dba_rating = [user_id, stars, comment]

    client_socket.send(pickle.dumps(("rate_apartment", dbu_rating, dba_rating, logged_user)))
    response = ""
    try:
        response = client_socket.recv(4069)
        response = pickle.loads(response)
    except:
        return None

    if response[0] == "rate":
        popup_function(top, "You have successfully rated this apartment.", top.destroy, "OK")
    else:
        pop_up(top, response[1])


def admin_window(frame, top, clicked):
    global logged_user, func_dict
    # if clicked conatins the word "Admin" 2 times
    if clicked.count("Admin") == 2 or clicked == "None"*100:
        if logged_user:
            if logged_user.is_admin:
                a = admin_page.start_up(frame, func_dict, logged_user, top)
            else:
                pop_up(top, "You are not an admin.")
        else:
            pop_up(top, "You are not logged in.")


def get_all_apartments():
    """
    Sends a request to the server to get all apartments.
    """
    client_socket.send(pickle.dumps(("find_apartment_by_id", None)))
    response = ""
    try:
        response = client_socket.recv(4069*1300)
        response = pickle.loads(response)
    except:
        return None

    return response


def set_attractions(attractions_file, top):
    """
    Sends a request to the server to set the attractions.
    """
    if logged_user:
        if not logged_user.is_admin:
            return
        else:
            client_socket.send(pickle.dumps(("set_attractions", attractions_file)))
            response = ""
            try:
                response = client_socket.recv(6069)
                response = pickle.loads(response)
            except:
                return None

            if response[0] == "set":
                pop_up(top, "You have successfully set the attractions.")
                return
            else:
                return response[1]
    else:
        return "You are not logged in."


def get_attractions():
    """
    Sends a request to the server to get the attractions.
    """
    client_socket.send(pickle.dumps(("get_attractions", None)))
    response = ""
    try:
        response = client_socket.recv(4069)
        response = pickle.loads(response)
    except:
        return None

    return response[1]


def search_admin_window(frame, top):
    s = search_page.start_up(frame, func_dict, top)


def get_specific_user_resvs(user_id, past, active):
    """
    Sends a request to the server to get the reservations of a specific user.
    """
    client_socket.send(pickle.dumps(("get_specific_user_resvs", user_id)))
    response = ""
    try:
        response = client_socket.recv(10069)
        response = pickle.loads(response)
    except:
        return None

    if response is None:
        return None

    if response[0] == "res":
        return response[1]

    return None


def upload_apartment_window(frame, top):
    if not logged_user:
        pop_up(top, "You are not logged in.")
        return
    else:
        u = upload_page.start_up(frame, func_dict, logged_user ,top)


def upload_apartment_server(top, entry_name, entry_price, entry_num_rooms, entry_num_beds, entry_images, entry_description, entry_location, entry_owner, entry_rules):
    name = entry_name.get()
    price = entry_price.get()
    num_rooms = entry_num_rooms.get()
    num_beds = entry_num_beds.get()
    im_path = entry_images.get()
    location = entry_location.get()
    owner = entry_owner.get()
    description = entry_description.get("1.0", END)
    rules = entry_rules.get("1.0", END)

    # get image from path
    try:
        with open(im_path, "rb") as f:
            img = f.readlines()
    except:
        pop_up(top, "The image path is not valid.")
        return
    try:
        while True:
            s = client_socket.send(pickle.dumps(("save_image", img)))
            res = pickle.loads(client_socket.recv(4069))
            if res[0] == "saved":
                img_path = res[1]
                break
            else:
                pop_up(top, "The image could not be saved.")
                return
    except:
        pop_up(top, "The image could not be saved.")
        return
    ap = Apartment.Apartment(name, num_rooms, num_beds, price, img_path,description, rules, location, owner)
    pickled_ap = pickle.dumps(ap)
    mes = ['upload', pickled_ap]
    mes = pickle.dumps(mes)
    client_socket.send(mes)
    mes = client_socket.recv(1024)
    mes = pickle.loads(mes)
    if mes[0] == 'upload_success':
        popup_function(top, "Apartment uploaded successfully.", top.destroy, "OK")
    else:
        pop_up(top, "Error, could not add apartment. Please try again")


def get_date():
    return today


def set_date(dat, top):
    global today
    try:
        # turn date into datetime object
        d = datetime.datetime.strptime(dat, '%Y-%m-%d')
    except Exception as e :
        pop_up(top, "Please enter a valid date." + str(e))
        return
    client_socket.send(pickle.dumps(("set_date", d)))
    response = ""
    try:
        response = client_socket.recv(1024)
        response = pickle.loads(response)
    except:
        return None

    if response[0] == "date":
        today = response[1]
        pop_up(top, "Date set successfully.")
        return
    else:
        return response[1]


def on_close(root):
    """
    When the window is closed, send a message to the server to close the connection
    """
    mes = ("close", "")
    mes = pickle.dumps(mes)
    try:
        client_socket.send(mes)
        client_socket.close()
    except:
        pass
    root.destroy()

# --------------------------------------------------


def addd_apartment_window(logged):
    """
    The function creates a window for adding an apartment.
    :param frame:
    :return:
    """
    win = win_creator(root, x, y, 4, 4, 1, 1, "Add apartment")
    frame = Frame(win, bg=bg_color)
    # make the frame take the whole window using pack
    frame.pack(fill="both", expand="YES")

    # Creating a form for the user to add his apartment to the system and sending it to the server using pack
    lbl_title = Label(frame, text="Add apartment", font=def_font, bg=bg_color, fg=txt_color)
    lbl_title.pack(fill="both", expand="YES")
    lbl_name = Label(frame, text="Name", font=def_font, bg=bg_color, fg=txt_color)
    lbl_name.pack(fill="both", expand="YES")
    entry_name = Entry(frame, font=def_font)
    entry_name.pack(fill="both", expand="YES")
    lbl_price = Label(frame, text="Price", font=def_font, bg=bg_color, fg=txt_color)
    lbl_price.pack(fill="both", expand="YES")
    entry_price = Entry(frame, font=def_font)
    entry_price.pack(fill="both", expand="YES")
    lbl_num_rooms = Label(frame, text="Number of rooms", font=def_font, bg=bg_color, fg=txt_color)
    lbl_num_rooms.pack(fill="both", expand="YES")
    entry_num_rooms = Entry(frame, font=def_font)
    entry_num_rooms.pack(fill="both", expand="YES")
    lbl_num_beds = Label(frame, text="Number of beds", font=def_font, bg=bg_color, fg=txt_color)
    lbl_num_beds.pack(fill="both", expand="YES")
    entry_num_beds = Entry(frame, font=def_font)
    entry_num_beds.pack(fill="both", expand="YES")
    lbl_images = Label(frame, text="Images", font=def_font, bg=bg_color, fg=txt_color)
    lbl_images.pack(fill="both", expand="YES")
    entry_images = Entry(frame, font=def_font)
    entry_images.pack(fill="both", expand="YES")
    lbl_description = Label(frame, text="Description", font=def_font, bg=bg_color, fg=txt_color)
    lbl_description.pack(fill="both", expand="YES")
    entry_description = Entry(frame, font=def_font)
    entry_description.pack(fill="both", expand="YES")
    lbl_rules = Label(frame, text="Rules", font=def_font, bg=bg_color, fg=txt_color)
    lbl_rules.pack(fill="both", expand="YES")
    entry_rules = Entry(frame, font=def_font)
    entry_rules.pack(fill="both", expand="YES")

    entry_location = Entry(frame, font=def_font)
    entry_location.insert(0, "(0,0)")
    map_lunch = Button(frame, text="Map", font=def_font, bg=color2, fg=txt_color,
                       command=lambda: (apartments_map(frame, entry_location, map_lunch),
                                        print(entry_location.get())))
    map_lunch.pack(side=LEFT, expand="YES", fill="both")

    lbl_owner = Label(frame, text="Owner", font=def_font, bg=bg_color, fg=txt_color)
    lbl_owner.pack(fill="both", expand="YES")
    entry_owner = Entry(frame, font=def_font)
    entry_owner.insert(0, logged.id)

    # confirm button. When clicked, upload the apartment to the server
    btn_ok = Button(win, text="OK", command=lambda: upload_apartment(win, entry_name, entry_price, entry_num_rooms, entry_num_beds, entry_images, entry_description, entry_location, entry_owner, entry_rules), font=def_font)
    btn_ok.pack(fill="both", expand="YES")
    # cancel
    btn_cancel = Button(win, text="Cancel", command=win.destroy, font=def_font)
    btn_cancel.pack(fill="both", expand="YES")


"""
# Tkinter
root = root_window()
x = root.winfo_screenwidth()
y = root.winfo_screenheight()

# current session
logged_user = None
search_details = ["check-in", "check-out", "guests", "apartment"]

# sockets
client_socket = connect_to_server()
buffer_size = 1024

client_start_window()

root.mainloop()
"""
# current session
logged_user = None
log_username = None
log_pass = None
search_details = ["check-in", "check-out", "guests", "apartment"]
today = datetime.datetime.today().date()

# Tkinter


# sockets
client_socket = connect_to_server()
buffer_size = 2048

func_dict = {
    "main_screen": main_screen,
    "search_server": search_server,
    "login_window": login_window,
    "profile_window": profile_window,
    "get_pics": get_pics,
    "book_window": book_window,
    "book_room": book_room,
    "login_server": login_server,
    "register_server": register_server,
    "get_apartment_by_id": get_apartment_by_id,
    "cancel_reservation": cancel_reservation,
    "rate_apartment_window": rate_apartment_window,
    "rate_apartment_server": rate_apartment_server,
    "admin_window": admin_window,
    "get_all_apartments": get_all_apartments,
    "set_attractions": set_attractions,
    "get_attractions": get_attractions,
    "search_admin_window": search_admin_window,
    "get_specific_user_resvs": get_specific_user_resvs,
    "upload_apartment_window": upload_apartment_window,
    "on_close": on_close,
    "listen_to_afk": listen_to_afk,
    "get_date": get_date,
    "set_date": set_date,
    "upload_apartment_server": upload_apartment_server,
}

main_screen()


# 1160
# 760
import datetime
from socket import *
import select
import pickle
import _thread
from Dbs.db_users import *
from Dbs.db_apartments import *

from Apartment import Apartment


def get_ip():
    """
    Returns machine's IP.
    """
    host_name = gethostname()
    ip = gethostbyname(host_name)
    return "localhost"


def get_free_port(HOST):
    """
    Returns the first free port for a host.
    """
    sock = socket()
    sock.bind((HOST, 0))
    port = sock.getsockname()[1]
    sock.close()
    return 7777 #port


def start_server(HOST, PORT):
    """
       Using Select, the function locates the users that sent a message, ready to receive a message and the
           exceptional ones.
       It handles the send queue for out-going messages.
       It can handle '!exit' messages and disconnecting events.
       """
    global open_client_socket, to_send
    serversock = socket(AF_INET, SOCK_STREAM)
    serversock.bind((HOST, PORT))
    serversock.listen(5)

    # List of sockets that are ready to be read from
    read_sockets = []
    # List of sockets that are ready to be written to
    write_sockets = []
    # List of sockets that are ready to be closed
    exceptional = []
    # The server should handle afk users who are not connected for more than 1 minute.
    # Those users are being added to the dictionary of afk users.
    # If the user is connected, the user is removed from the dictionary..
    # The dictionary is updated every minute.

    _thread.start_new_thread(afk_maintainer, ())

    while True:
        # Get the list sockets which are ready to be read through select
        read_sockets, write_sockets, exceptional = select.select(open_client_socket + [serversock], write_sockets, exceptional)

        for sock in read_sockets:
            # New connection
            if sock == serversock:
                # Handle the new connection
                nsock, addr = serversock.accept()
                open_client_socket.append(nsock)
                # send today
                #sock.send(pickle.dumps(("today", datetime.date.today())))

            # Data from a client
            else:
                # Receive data from the socket
                try:
                    data = pickle.loads(sock.recv(BUFFSIZE))
                    if data:
                        # Add to the list of messages
                        to_send.append((sock, data))
                    if data[0] == "close":
                        sock.close()
                        # Remove from the list of sockets
                        try:
                            open_client_socket.remove(sock)
                        except:
                            pass
                        try:
                            write_sockets.remove(sock)
                        except:
                            pass
                        try:
                            to_send.remove((sock, data))
                        except:
                            pass
                except:
                    pass

        for ex in exceptional:
            open_client_socket.remove(ex)
            ex.close()

        # Send the messages
        if to_send:
            to_send = send_waiting_messages(open_client_socket, to_send)

        # if the user closed the connection, remove it from the list
        for sock in write_sockets:
            if sock not in open_client_socket:
                write_sockets.remove(sock)


def afk_maintainer():
    global open_client_socket, active_apartments, to_send
    # The server should handle afk users who are not connected for more than 1 minute.

    while True:
        global_time = datetime.datetime.now()
        for sock in open_client_socket:
            try:
                if active_rents[sock] is not None:
                    # if bigger than 1 minute
                    t = active_rents[sock][1]
                    t = t + datetime.timedelta(seconds=30)
                    if t <= global_time:
                        to_send.append((sock, ("afk_rent", active_rents[sock][0])))
                        del active_rents[sock]
                        to_send = send_waiting_messages(open_client_socket, to_send)
            except:
                pass


def book_apartment(ap_id, res_lst, user_id):
    """
    Book an apartment.
    """
    try:
        renter = user_id
        email = res_lst[1]
        start_date = res_lst[2]
        end_date = res_lst[3]
        number_of_guests= res_lst[4]
        dba.book_apartment(renter, email, start_date, end_date, number_of_guests, ap_id)
        dbu.add_reservation(ap_id, user_id, res_lst)
    except:
        return "not_booked"
    return "booked"


def send_waiting_messages(open_client_socket, to_send):
    """
    At the end of each loop in the 'start_server' function, this function runs.
    It sends the awaiting messages using pickle to the user.
    """
    for mes in to_send:
        # Send the message to the user
        sock,data = mes
        try:
            print(data)
            if data[0] == 'info':
                apartment = find_apartment_by_id(data[1])
                sock.send(pickle.dumps(apartment))
            elif data[0] == 'search':
                av = find_available_apartments(data)
                sock.send(pickle.dumps(("search_results", av)))
            elif data[0] == 'book':
                #              ap_id  , res lst , user id
                try:
                    active_apartments.remove(data[1])
                except:
                    pass
                try:
                    del active_rents[sock]
                except:
                    pass
                print(1, data)
                mes = book_apartment(data[1], data[2], data[3])
                print(2, data)
                sock.send(pickle.dumps("a"))
                sock.send(pickle.dumps((mes, data[1])))
                print(3, data)
            elif data[0] == 'register':
                mes = register_user(data[1], data[2], data[3], data[4], data[5], data[6]) # name, pass, email, age, ref code, id
                sock.send(pickle.dumps(('success', mes)))
            elif data[0] == 'login':
                # run login function
                user = dbu.login(data[1], data[2])
                print(user)
                if user:
                    sock.send(pickle.dumps(("login_success", user)))
                else:
                    sock.send(pickle.dumps(("login_fail", None)))
            elif data[0] == 'upload':
                # upload apartment
                apartment = data[1]
                dba.add_apartment(apartment)
                sock.send(pickle.dumps(("upload_success", None)))
            elif data[0] == 'get_pics':
                pics = pics_request(data[1])
                sock.send(pickle.dumps(("pics", pics)))
            elif data[0] == 'save_image':
                # save image
                p = save_pic(data[1], data[2])
                sock.send(pickle.dumps(("saved", p)))
            elif data[0] == 'get_users':
                users = dbu.get_all_users()
                sock.send((pickle.dumps(users), None))
            elif data[0] == "find_apartment_by_id":
                apartment = find_apartment_by_id(data[1])
                sock.send(pickle.dumps(apartment))
            elif data[0] == "cancel_reservation":
                m = cancel_reservation(data[1], data[2])
                sock.send(pickle.dumps(("reserv", m)))
            elif data[0] == "rate_apartment":
                m = rate_apartment(data[1], data[2], data[3])
                sock.send(pickle.dumps(("rate", m)))
            elif data[0] == "set_attractions":
                m = set_attractions(data[1])
                sock.send(pickle.dumps((m,)))
            elif data[0] == "get_attractions":
                m, f = get_attractions()
                sock.send(pickle.dumps((m, f)))
            elif data[0] == "get_specific_user_resvs":
                d = get_specific_user_resvs(data[1])
                sock.send(pickle.dumps(("res", d)))
            elif data[0] == "start_rent":
                active_apartments.append(data[1])
                active_rents[sock] = (data[1], data[2])
            elif data[0] == "end_rent":
                active_apartments.remove(data[1])
                del active_rents[sock]
                sock.send(pickle.dumps(("end", data[1])))
            elif data[0] == "afk_rent":
                active_apartments.remove(data[1])
                sock.send(pickle.dumps(("afk_rent", "You have been afk for too long. Your rent has been cancelled.")))
            elif data[0] == "get_date":
                sock.send(pickle.dumps(("date", today)))
            elif data[0] == "set_date":
                change_date(data[1])
                sock.send(pickle.dumps(("date", today)))
            else:
                sock.send(pickle.dumps(None, None))
            to_send.remove((sock, data))
            if sock not in open_client_socket:
                to_send.remove((sock, data))
        except:
            pass

    return to_send


def register_user(name, password, email, age, ref_code, id):
    """
    Register a new user.
    """
    try:
        age = int(age)
    except:
        return "Invalid age. Please enter a number."
    if age < 18:
        return "User is too young! Must be 18 or older."
    elif dbu.get_user_by_id(id):
        return "User Already Exists! Please try again."
    else:
        if ref_code == "SECRETADMINCODE":
            admin = 1
        else:
            admin = 0

        us = User.User(id, name, password, admin, email, age)
        a = dbu.add_user(us)
        if a:
            return "User added successfully!"
        return "User could not be added. Please try again."


def find_available_apartments(requirements):
    """
    Returns a list of all the available apartments.
    """
    price = requirements[1]
    sdate = requirements[2]
    edate = requirements[3]
    place = requirements[4]
    guests = requirements[5]

    available_apartments = []
    apartments = dba.get_all_apartments()
    if apartments is None:
        return None
    for ap in apartments:
        try:
            if ap.is_ok(sdate, edate, guests, price, place):
                if ap.id not in active_apartments:
                    available_apartments.append(ap)
        except:
            pass
    return available_apartments


def find_apartment_by_id(house_id):
    """
    This function is used to find an apartment from file.
    """
    apartments = dba.get_all_apartments()
    if house_id is None:
        return apartments

    if apartments is None:
        return None
    for apartment in apartments:
        if apartment.id == house_id:
            return apartment
    return None


def pics_request(house_id, index=0):
    """
    This function is used to get the picture of an apartment.
    """
    apartment = find_apartment_by_id(house_id)
    if apartment is None:
        return None
    path = apartment.images[index]
    try:
        full_path = apartment.images[index] + "%d.png" % house_id
    except:
        full_path = os.path.join(os.getcwd(), path)
    # read the image and pikcle it
    try:
        with open(full_path, "rb") as image_file:
            image = image_file.readlines()
        return image
    except:
        return None


def save_pic(image, name):
    """
    This function is used to save the picture of an apartment.
    """
    path = "Dbs/images/" + name + ".png"
    path = os.path.abspath(path)
    with open(path, "wb") as f:
        for d in image:
            f.write(d)
    return path



def cancel_reservation(user_id, house_id):
    """
    This function is used to cancel a reservation.
    """
    try:
        u = dbu.cancel_reservation(user_id, house_id)
        if u:
            a = dba.cancel_reservation(user_id, house_id)
            if a:
                return "Reservation cancelled successfully!"
            else:
                return "Reservation could not be cancelled. Please try again."
        else:
            return "Reservation could not be cancelled. Please try again."
    except:
        return "Reservation could not be cancelled. Please try again."


def rate_apartment(dbu_rev, dba_rev, logged):
    """
    This function is used to rate an apartment.
    """
    try:
        u = dbu.add_rating(dbu_rev, logged)
        if u:
            a = dba.add_rating(dba_rev, dbu_rev[0])
            if a:
                return "Rating added successfully!"
            else:
                return "Rating could not be added. Please try again."
        else:
            return "Rating could not be added. Please try again."
    except:
        return "Rating could not be added. Please try again."


def set_attractions(attractions):
    """
    This function is used to set the attractions.
    """
    path = "Dbs/attractions_file.txt"
    with open(path, "w") as f:
        for attraction in attractions:
            f.write(attraction + "\n")
    return "set"


def get_attractions():
    """
    This function is used to get the attractions.
    """
    try:
        path = "Dbs/attractions_file.txt"
        with open(path, "r") as f:
            attractions = f.readlines()
        return "attractions", attractions
    except:
        return "attractions", None


def get_specific_user_resvs(user_id):
    """
    This function is used to get the reservations of a specific user.
    """
    try:
        if user_id is None:
            reservations = dbu.get_all_reservations()
        else:
            reservations = dbu.get_specific_user_resvs(user_id)

        return reservations
    except:
        return None


def change_date(date):
    global today
    if date is None:
        today = datetime.datetime.now().date()
    else:
        today = date.date()


# Global variables
HOST = get_ip()
PORT = get_free_port(HOST)
BUFFSIZE = 5000 * 1231
ADDR = (HOST, PORT)
today = datetime.datetime.today().date()

# database
dbu = db_users()
dba = db_apartments()

active_apartments = [] # [apartment1, apartment2, ...]
active_rents = {} # {sock: (apartment_id, time)}

open_client_socket = [] # [sock1, sock2, ...]
to_send = [] # [(sock, message), (sock, message), ...]


start_server(HOST, PORT)

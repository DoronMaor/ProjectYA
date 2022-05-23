import pickle


class User:

    """
    Class that generates new instances of users.
    Each User have:
    - Full Name
    - Email
    - Password
    - age
    - id
    - is admin
    - reservations list [["apartment_id", "check_in", "check_out"]]
    - rated apartments list [["user_id", "rating", "comment"]]
    """

    def __init__(self, id, name, password, is_admin, email, age, reservations = None, rated_apartments = None):
        self.id = id
        self.name = name
        self.password = password
        self.is_admin = is_admin
        self.email = email
        self.age = age
        if reservations is None:
            self.reservations = []
        else:
            try:
                self.reservations = pickle.loads(reservations)
            except:
                self.reservations = reservations

        if rated_apartments is None:
            self.rated_apartments = []
        else:
            try:
                self.rated_apartments = pickle.loads(rated_apartments)
            except:
                self.rated_apartments = rated_apartments


    def __str__(self):
        return "User: " + self.name + " " + str(self.age) + " " + self.email + " " + self.password + " " + str(self.id) + " " + str(self.is_admin) + \
               " " + str(self.reservations) + " " + str(self.rated_apartments)


    #region gets and sets
    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_id(self):
        return self.id

    def get_is_admin(self):
        return self.is_admin

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def set_id(self, id):
        self.id = id

    def set_is_admin(self, is_admin):
        self.is_admin = is_admin

    def add_reservation(self, date, apartment_id):
        self.reservations.append((date, apartment_id))

    def get_reservations(self):
        return self.reservations
    #endregion


    def get_reservation_by_id(self, id):
        for reservation in self.reservations:
            if reservation[1] == id:
                return reservation
        return None

    def get_reservation_by_date(self, date):
        for reservation in self.reservations:
            if reservation[0] == date:
                return reservation
        return None

    def remove_reservation(self, date, apartment_id):
        for reservation in self.reservations:
            if reservation[0] == date and reservation[1] == apartment_id:
                self.reservations.remove(reservation)
                return True
        return False

    def rate_apartment(self, rate, apartment_id):
        self.rated_apartments.append((rate, apartment_id))

    def get_rated_apartments(self):
        return self.rated_apartments

    def get_rated_apartment_by_id(self, id):
        for rated_apartment in self.rated_apartments:
            if rated_apartment[1] == id:
                return rated_apartment
        return None

    def make_admin(self):
        self.is_admin = True

    def has_already_been_inpast_reservation(self, sdate, apartment_id):
        for reservation in self.reservations:
            if reservation[0] == sdate and reservation[1] == apartment_id:
                return True
        return False


    def is_admin_user(self):
        return self.is_admin

    def already_rated(self, apartment_id, start_date, ):
        for rated_apartment in self.rated_apartments:
            if rated_apartment[0] == apartment_id:
                #return True
                return False
        return False


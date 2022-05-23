import math
import random
import datetime
import pickle

class Apartment:
    """
    Every apartment for rent has :
    - id (unique)
    - a name
    - a number of rooms
    - a number of bedrooms
    - a price
    - a list of images
    - when is it available
    - a description
    - a list of reviews
    - a list of reservations
    - star rating (0-5)
    - a list of rules
    - area (x,y)

    Each reservation has :
    - a name of the renter [0]
    - a phone number of the renter [1]
    - a starting date of the reservation [2]
    - a ending date of the reservation [3]
    - a number of guests [4]

    Each review has :
    - a rating (0-5) [0]
    - a name of the reviewer [1]
    - a comment [2]
    - rated apartments list [["apartment_id", "rating", "comment"]]


    Each image has :
    - a name of the image
    - a path to the image

    Date format : datetime or string (YYYY-MM-DD)
    """

    def __init__(self, name, number_of_rooms, number_of_beds, price
                 , images, description, rules, area, owner, id=None, available=None, reviews=None, reservations=None):
        self.name = name
        self.number_of_rooms = number_of_rooms
        self.number_of_beds = number_of_beds
        self.price = price
        self.owner = owner
        # check if pickled
        try:
            self.images = pickle.loads(images)
        except:
            self.images = images
        if available is not None:
            self.available = available
        else:
            self.available = True
        self.description = description
        if reviews is None:
            self.reviews = []
        else:
            try:
                self.reviews = pickle.loads(reviews)
            except:
                self.reviews = reviews
        if reservations is None or reservations == []:
            self.reservations = []
        else:
            try:
                self.reservations = pickle.loads(reservations)
            except:
                self.reservations = reservations

        self.star_rating = self.calculate_star_rating()

        try:
            self.rules = pickle.loads(rules)
        except:
            self.rules = rules

        try:
            self.area = pickle.loads(area)
        except:
            try:
                self.area = self.string_to_tuple(area)
            except:
                self.area = area
        if id is None:
            self.id = random.randint(1, 1000000)
        else:
            self.id = id

    def calculate_star_rating(self):
        star_rating = 0
        for re in self.reviews:
            try:
                if type(int(re[1])) is int:
                    star_rating += re[1]
            except:
                pass
        d = self.name
        if len(self.reviews) > 0:
            star_rating = star_rating / len(self.reviews)
        else:
            return 0

        return star_rating

    def __str__(self):
        return "Apartment: " + self.name + "(owner %d)  " % self.owner + str(self.id) + " " + str(self.price) + " star" + str(self.star_rating) + " " + str(self.available) + " " + str(self.area) + " " + str(self.number_of_rooms) + " " + str(self.number_of_beds) + " " + str(self.images) + " " + str(self.description) + " " + str(self.reviews) + " " + str(self.reservations) + " " + str(self.rules)

    def get_name(self):
        return self.name

    def get_number_of_rooms(self):
        return self.number_of_rooms

    def get_number_of_beds(self):
        return self.number_of_beds

    def get_price(self):
        return self.price

    def get_images(self):
        return self.images

    def get_available(self):
        return self.available

    def get_description(self):
        return self.description

    def get_reviews(self):
        return self.reviews

    def get_reservations(self):
        return self.reservations

    def get_star_rating(self):
        return self.star_rating

    def get_rules(self):
        return self.rules

    def when_is_available(self, dates):
        """
        The function looks at the list of reservations and returns a list of dates that are available
        """
        available_dates = []
        for date in dates:
            if date not in self.reservations:
                available_dates.append(date)
        return available_dates

    def add_review(self, review):
        """
        The function adds a review to the list of reviews
        """
        self.reviews.append(review)

    def add_reservation(self, reservation):
        """
        The function adds a reservation to the list of reservations
        """
        self.reservations.append(reservation)

    def add_star(self, star):
        """
        The function adds a star to the star rating
        """
        self.star_rating = (self.star_rating[0] + star, self.star_rating[1] + 1)

    def is_ok(self, sdate, edate, guests, price, place):
        """
        The function checks if the apartment is available at the given date
        """
        place = self.string_to_tuple(place)
        if self.available:
            if guests > self.number_of_beds:
                return False
            if price < self.price:
                return False
            #if place != self.area:
            print(self)
            if not self.is_in_radius(place, self.area, 200):
                return False
            print(self)
            # if it has more than 1 reservation
            if len(self.reservations) > 1:
                for reservation in self.reservations:
                    if reservation != "" and reservation is not None:
                        d1 = datetime.datetime.strptime(reservation[2], "%Y-%m-%d").date()
                        d2 = datetime.datetime.strptime(reservation[3], "%Y-%m-%d").date()
                        if d1 <= sdate <= d2 or d1 <= edate <= d2:
                            return False
        return True

    def is_available_here(self, date):
        """
        The function checks if the apartment is available at the given date
        """
        if self.available:
            for reservation in self.reservations:
                if reservation != "" and reservation is not None:
                    d1 = datetime.datetime.strptime(reservation[2], "%Y-%m-%d").date()
                    d2 = datetime.datetime.strptime(reservation[3], "%Y-%m-%d").date()
                    if d1 <= date <= d2:
                        return False
        return True


    def is_in_radius(self, place, area, radius):
        if self.pitaguras_theo(place, area) <= radius:
            return True
        return False

    def pitaguras_theo(self, tup1, tup2):
        """
        The function calculates the distance between two points
        """
        dis = math.sqrt((tup2[0] - tup1[0]) ** 2 + (tup2[1] - tup1[1]) ** 2)
        return dis

    def string_to_tuple(self, area):
        """
        The function recives "(x,y)" string and returns a tuple
        """
        area = area.replace("(", "")
        area = area.replace(")", "")
        area = area.split(",")
        return int(area[0]), int(area[1])

    def string_to_list(self, string):
        """
        The function recives a string and returns a list
        """
        string = string.replace("[", "")
        string = string.replace("]", "")
        string = string.split(",")
        return string

    def get_number_of_reservations(self):
        return len(self.reservations)

    def get_number_of_reviews(self):
        return len(self.reviews)

    def get_number_of_guests(self):
        gues = 0
        for reservation in self.reservations:
            gues += int(reservation[4])
        return gues

    def get_reservations_reviews_ratio(self):
        return self.get_number_of_reservations() / (self.get_number_of_reviews() if self.get_number_of_reviews() != 0 else 1)

    def get_total_money(self):
        money = 0
        for reservation in self.reservations:
            money += int(self.get_days_between(reservation[2], reservation[3])) * int(self.price)
        return self.price * self.get_number_of_reservations()

    def get_days_between(self, date1, date2):
        """
        The function calculates the days between two dates
        """
        date1 = datetime.datetime.strptime(date1, "%Y-%m-%d").date()
        date2 = datetime.datetime.strptime(date2, "%Y-%m-%d").date()
        return int(abs((date2 - date1).days))

    def get_6_most_popular_reservation_dates(self):
        """
        The function returns the 6 most popular reservation dates without the year
        """
        dates = []
        for reservation in self.reservations:
            dates.append(reservation[2][:10])
        dates = list(set(dates))
        dates.sort()
        return dates[:6]

    def get_money_made_each_month(self):
        """
        The function returns the money made each month
        """
        money_dict = {}
        for reservation in self.reservations:
            date = reservation[2][:7]
            if date in money_dict:
                money_dict[date] += int(self.get_days_between(reservation[2], reservation[3])) * int(self.price)
            else:
                money_dict[date] = int(self.get_days_between(reservation[2], reservation[3])) * int(self.price)
        return money_dict





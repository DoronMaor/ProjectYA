import sqlite3 as lite
import os
import Apartment
import pickle


class db_apartments:
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
        - owner id

        Each reservation has :
        - a name of the renter [0]
        - a email of the renter [1]
        - a starting date of the reservation [2]
        - a ending date of the reservation [3]
        - a number of guests [4]

        Each review has :
        - a name of the reviewer
        - a rating (0-5)
        - a comment


        Each image has :
        - a name of the image
        - a path to the image

        Date format : datetime
        """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_name = "apartments.db"
    db_path = os.path.join(BASE_DIR, file_name)

    def __init__(self, db_path=db_path):
        """
        Initializes the class
        """
        self.db_path = db_path
        self.conn = lite.connect(self.db_path)
        self.cur = self.conn.cursor()

    def db_connect(self):
        self.conn = lite.connect(self.db_path)
        self.cur = self.conn.cursor()

    def db_close(self):
        self.conn.close()

    def db_query(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()

    def db_insert(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def db_update(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def db_delete(self, query):
        self.cur.execute(query)
        self.conn.commit()

    def query_to_apartment(self, apart):
        """
        Convert query result to apartment object
        """
        try:
            name = apart[0]
            number_of_rooms = apart[1]
            number_of_beds = apart[2]
            price = apart[3]
            try:
                images = pickle.loads(apart[4])
            except:
                images = []
            description = apart[5]
            try:
                rules = pickle.loads(apart[6])
            except:
                rules = []
            try:
                area = pickle.loads(apart[7])
            except:
                area = []
            id = apart[8]
            available = apart[9]
            try:
                reviews = pickle.loads(apart[10])
            except:
                reviews = []
            try:
                reservations = pickle.loads(apart[11])
            except:
                reservations = []

            owner = apart[12]

            return Apartment.Apartment(name, number_of_rooms, number_of_beds, price, images, description, rules, area,
                                       owner, id, available, reviews, reservations)
        except:
            return None

    def query_to_apartment2(self, apart):
        """
        Convert query result to apartment object
        """
        if apart:
            name = apart[0][0]
            number_of_rooms = apart[0][1]
            number_of_beds = apart[0][2]
            price = apart[0][3]
            images = pickle.loads(apart[0][4])
            description = apart[0][5]
            rules = pickle.loads(apart[0][6])
            area = pickle.loads(apart[0][7])
            id = apart[0][8]
            available = apart[0][9]
            reviews = pickle.loads(apart[0][10])
            reservations = pickle.loads(apart[0][11])
            owner = apart[0][12]
            return Apartment.Apartment(name, number_of_rooms, number_of_beds, price, images, description, rules, area,
                                       owner, id, available, reviews, reservations)
        else:
            return None

    def get_all_apartments(self):
        """
        Select all apartments and return them as a list of Apartment objects using db_query
        """
        query = "SELECT * FROM apartments"
        aparts = self.db_query(query)
        return [self.query_to_apartment(apart) for apart in aparts]

    def get_apartment_by_id(self, id):
        """
        Select apartment by id
        """
        query = "SELECT * FROM apartments WHERE id = {}".format(id)
        apart = self.db_query(query)
        return self.query_to_apartment2(apart)

    def book_apartment(self, renter, email, start_date, end_date, number_of_guests, apartment_id):
        """
        Book an apartment in apartments table where id = apartment_id
        """

        # reser = []
        # reservations = [[lst1], [lst2]....]
        reser = [renter, email, start_date, end_date, number_of_guests]
        get_reservations = "SELECT reservations FROM apartments WHERE id = {}".format(apartment_id)

        reservations = self.db_query(get_reservations)

        if reservations:
            try:
                reservations = pickle.loads(reservations[0])
            except:
                reservations = []
            reservations.append(reser)
            reservations = pickle.dumps(reservations)
        else:
            reservations = pickle.dumps([reser])

        self.cur.execute("UPDATE apartments SET reservations = ? WHERE id = ?", (reservations, apartment_id))
        self.conn.commit()
        return True

    def add_apartment(self, ap):
        """
        Add apartment to apartments table
        """
        try:
            ap = pickle.loads(ap)
        except:
            ap = ap
        self.cur.execute('INSERT INTO apartments VALUES (?, ?, ? ,? ,? ,? ,? ,? ,? ,? ,?, ?, ?)', (
            ap.name, ap.number_of_rooms, ap.number_of_beds, ap.price, pickle.dumps(ap.images), ap.description,
            pickle.dumps(ap.rules), pickle.dumps(ap.area), ap.id, ap.available, pickle.dumps(ap.reviews),
            pickle.dumps(ap.reservations), ap.owner))
        self.conn.commit()

    def add_review(self, review, apartment_id):
        """
        Add review to reviews table
        """
        query = "SELECT reviews FROM apartments WHERE id = {}".format(apartment_id)
        result = self.db_query(query)
        try:
            reviews = pickle.loads(result[0])
            reviews.append(review)
        except:
            result.append(review)
        self.cur.execute("UPDATE apartments SET reviews = ? WHERE id = ?", (pickle.dumps(result), apartment_id))
        self.conn.commit()

    def cancel_reservation(self, renter, apartment_id):
        """
        Cancel reservation
        """
        query = "SELECT reservations FROM apartments WHERE id = {}".format(apartment_id)
        result = self.db_query(query)
        try:
            reservations = pickle.loads(result[0][0])
            for reservation in reservations:
                if reservation[0] == renter:
                    reservations.remove(reservation)
                    self.cur.execute("UPDATE apartments SET reservations = ? WHERE id = ?",
                                     (pickle.dumps(reservations), apartment_id))
                    self.conn.commit()
                    return True
        except:
            pass
        return False

    def add_rating(self, review, ap_id):
        """
        Add rating to reviews table
        """
        query = "SELECT reviews FROM apartments WHERE id = {}".format(ap_id)
        result = self.db_query(query)
        try:
            reviews = pickle.loads(result[0][0])
            reviews.append(review)
        except:
            reviews = [review]
        self.cur.execute("UPDATE apartments SET reviews = ? WHERE id = ?", (pickle.dumps(reviews), ap_id))
        self.conn.commit()
        return True


"""
dba = db_apartments()
for a in dba.get_all_apartments():
    print(a)


ap = Apartment.Apartment("high1", 1, 2 ,106, ["image1", "image2"], "awjfvbawf", ["rules"], (390,200), 32432, None, None, [])
dba.add_apartment(ap)

ap = Apartment.Apartment("high2", 1, 2 ,147, ["image1", "image2"], "description", ["rules"], (2,1), 32432, None, None, [5, "nane", "good"])
dba.add_apartment(ap)
ap = Apartment.Apartment("high3", 1, 2 ,244, ["image1", "image2"], "description", ["rules"], (1,2), 32432, None, None, [5, "nane", "good"])
dba.add_apartment(ap)
ap = Apartment.Apartment("high4", 1, 2 ,647, ["image1", "image2"], "description", ["rules"], (2,2), 32432, None, None, [5, "nane", "good"])
dba.add_apartment(ap)

# save the images folder path into a var
images_folder_path = os.path.dirname(__file__) + "/images/"
dba = db_apartments()

ap = Apartment.Apartment("high7", 1, 2 ,734, [images_folder_path], "description", ["rules"], (3,1), 32432)
dba.add_apartment(ap)

ap = Apartment.Apartment("high6", 1, 2 ,634, [images_folder_path], "description", ["rules"], (3,1), 32432)
dba.add_apartment(ap)

ap = Apartment.Apartment("high5", 1, 2 ,534, [images_folder_path], "description", ["rules"], (3,1), 32432)
dba.add_apartment(ap)

ap = Apartment.Apartment("high4", 1, 2 ,474, [images_folder_path], "description", ["rules"], (3,1), 32432)
dba.add_apartment(ap)
"""

# print start rating of apartment id = 106143
# print(dba.get_apartment_by_id(989001))

import sqlite3 as lite
import os
import User
import Apartment


class dbaccess_apartment:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_name = "apartments_database.db"
    db_path = os.path.join(BASE_DIR, file_name)

    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self.conn = lite.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def db_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def db_insert(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def db_update(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def db_delete(self, query):
        self.cursor.execute(query)
        self.conn.commit()

    def db_close(self):
        self.conn.close()

    # Apartment functions

    def get_all_apartments(self):
        """
        Select all apartments
        """
        query = "SELECT * FROM apartments"
        return self.db_query(query)

    def print_all_apartments(self):
        """
        Print all apartments
        """
        for row in self.get_all_apartments():
            data = row[3]

            user_obj = User.User(data)

            print(user_obj)

    def create_apartments(self,ap_id, ap_area, ap_obj):
        """
        Create a apartments using a string apartment, string tuple dates (MM,DD)(MM,DD), string x,y coordinates, string id
        """

        ap_obj = ap_obj.convert_to_string()

        query = "INSERT INTO apartments (ap_id, ap_area, ap_obj)" \
                " VALUES ('%s', '%s', '%s')" % (ap_id, ap_area, ap_obj)

        self.db_insert(query)

    def select_apartment_by_id(self, user_id):
        """
        Select a user by id
        """
        query = "SELECT * FROM apartments WHERE ap_id = '%s'" % user_id
        return Apartment.Apartmentt(self.db_query(query))

    def book_apartment(self, ap_id, reservation):
        """
        books a an apartment
        """
        ap = self.select_apartment_by_id(ap_id)
        ap.add_reservation(reservation)
        ap = ap.convert_to_string()

        #update
        query = "UPDATE apartments SET ap_obj = '%s' WHERE ap_id = '%s'" % (ap, ap_id)
        self.db_update(query)



"""
c = dbaccess_apartment()
n = Apartmentt.Apartmentt("Apartment", 2, 2, 100, "images", True, "description", "rules", "(1,1)")
c.create_apartments(n.id, n.area, n)
"""
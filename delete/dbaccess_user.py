import sqlite3 as lite
import os
import User


class dbaccess_user:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_name = "users_database.db"
    db_path = os.path.join(BASE_DIR, file_name)

    def __init__(self, db_path):
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


    # User functions

    def select_all_users(self):
        """
        Select all users
        """
        query = "SELECT * FROM users"
        return self.db_query(query)

    def print_all_users(self):
        """
        Print all users
        """
        for row in self.select_all_users():
            data = row[3]

            user_obj = User.User(data)

            print(user_obj)

    def create_user(self, user_name, password, user_id, user_obj):
        """
        Create a user using a string name, string password and pickled User data
        """

        user_obj = user_obj.convert_to_string()

        query = "INSERT INTO users (username, password, user_id, user_obj) VALUES ('%s', '%s', '%s', '%s')" \
                % (user_name, password, user_id, user_obj)

        self.db_insert(query)

    def select_user_by_id(self, user_id):
        """
        Select a user by id
        """
        query = "SELECT * FROM users WHERE user_id = '%s'" % user_id
        return User.User(self.db_query(query))

    def delete_user_by_id(self, user_id):
        """
        Delete a user by id
        """
        query = "DELETE FROM users WHERE user_id = '%s'" % user_id
        self.db_query(query)

    def login(self, user_name, password):
        """
        Login a user, if does not exist, return None
        """

        print(user_name, password)
        query = "SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (user_name, password)
        print(query)
        rows = self.db_query(query)
        if len(rows) == 0:
            return None
        else:
            return User.User(rows[0][3])

    def book_apartment(self, apartment_id, user_id, reservation):

import hashlib
from database import Database

class AuthSystem:
    def __init__(self, db):
        self.db = db
        self.current_user = None

    # to encrypt password
    def __hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # current user
    def __set_current_user(self, user):
        user_info = {"id": user[0],
                     "username": user[1],
                     "password": user[2],
                     "role": user[3]}
        self.current_user = user_info

    def __get_current_user(self):
        return self.current_user

    # methods for mysql/sqlite
    def __select_all_from_db(self, type_):
        cursor = self.db.conn.cursor()
        result = ""
        try:
            cursor.execute(f"SELECT {type_} FROM users;")
            result = cursor.fetchall()
        finally:
            cursor.close()
        return result

    def __get_all_users_from_db(self):
        return self.__select_all_from_db('*')

    def __get_user_from_db(self, con_type, con_value):
        cursor = self.db.conn.cursor()
        result = ""
        try:
            cursor.execute(f"SELECT * FROM users WHERE {con_type} = ?;",
                           (con_value,))
            result = cursor.fetchone()
        finally:
            cursor.close()

        return result

    def __update_user_in_db(self, con_type, con_val, key, key_val):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute(f"UPDATE users SET {con_type} = ? WHERE {key} = ?;",
                           (con_val, key_val))
            self.db.conn.commit()
        finally:
            cursor.close()

    def __insert_user_to_db(self, username, password, role):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("""INSERT OR IGNORE INTO users (username, password_hash, role)
                                    VALUES(?, ?, ?)""", (username, password, role))
            self.db.conn.commit()
        finally:
            cursor.close()

    def __remove_user_from_db(self, username):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE username = ?;", (username,))
            self.db.conn.commit()
        finally:
            cursor.close()


    # methods for auth and personal info
    def register(self, username, password, role = 'regular'):
        hash_password = self.__hash_password(password)
        role = role if role in ["admin", "regular"] else "regular"

        usernames_list = self.__select_all_from_db("username") #fetch all usernames
        usernames_list = [user[0] for user in usernames_list] #convert from 2d to 1d

        if username not in usernames_list:
            self.__insert_user_to_db(username, hash_password, role)
            return True
        return False

    def login(self, username, password):
        user = self.__get_user_from_db("username", username)

        is_success = False
        if user and user[2] == self.__hash_password(password):
            self.__set_current_user(user)
            is_success = True
        return is_success

    def logout(self):
        self.current_user = None
        return True

    def forget_password(self, id_, username, role, new_password):
        user = self.__get_user_from_db("username", username)
        if id_ == user[0] and role == user[3]:
            new_password = self.__hash_password(new_password)
            self.__update_user_in_db("username", username,
                                     "password_hash", new_password)

    def update_password(self, username, old_pass, new_pass):
        user = self.__get_user_from_db("username", username)
        if user and user[2] == self.__hash_password(old_pass):
            new_hash_pass = self.__hash_password(new_pass)
            self.__update_user_in_db("password_hash", new_hash_pass,
                                     "username", username)
        return False

    def update_username(self, old_username, new_username, password):
        user = self.__get_user_from_db("username", old_username)
        if user and user[2] == self.__hash_password(password):
            self.__update_user_in_db("username", new_username,
                                     "id", user[0])
            return True

        return False

    # admin only methods
    def update_role(self, username, role, admin_password):
        if self.is_admin():
            user = self.__get_user_from_db("username", username)
            if user and admin_password == self.current_user["password"]:
                role = role if role in ["admin", "regular"] else "regular"
                self.__update_user_in_db("role", role,
                                       "username", username)
                return True
        return False

    def delete_user(self, username, admin_password):
        if self.is_admin():
            user = self.__get_user_from_db("username", username)
            if user and admin_password == self.current_user["password"]:
                self.__remove_user_from_db(username)

    def is_admin(self):
        """Check if current user is an admin"""
        return self.current_user and self.current_user['role'] == 'admin'

    # testing methods, delete after dev
    def print_users(self):
        for i in self.__get_all_users_from_db():
            for j in i:
                print(j, end=" ")
            print()

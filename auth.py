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
            cursor.execute(f"UPDATE users SET {key} = ? WHERE {con_type} = ?;",
                           (key_val, con_val))
            self.db.conn.commit()
        finally:
            cursor.close()

    def __insert_user_to_db(self, username, password, role, security_question, security_answer):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("""INSERT OR IGNORE INTO users (username, password_hash, role, security_question, security_answer)
                                    VALUES(?, ?, ?, ?, ?)""", 
                                    (username, password, role, security_question, security_answer))
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
    def register(self, username, password, security_question, security_answer, role = 'regular'):
        hash_password = self.__hash_password(password)
        role = role if role in ["admin", "regular"] else "regular"

        usernames_list = self.__select_all_from_db("username") #fetch all usernames
        usernames_list = [user[0] for user in usernames_list] #convert from 2d to 1d

        if username not in usernames_list:
            # Clear products for new user
            self.db.clear_products_for_new_user()
            # Register the new user
            self.__insert_user_to_db(username, hash_password, role, security_question, security_answer)
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
        if user and id_ == str(user[0]) and role == user[3]:
            new_password = self.__hash_password(new_password)
            self.__update_user_in_db("username", username,
                                     "password_hash", new_password)
            return True
        return False

    def update_password(self, username, old_pass, new_pass):
        user = self.__get_user_from_db("username", username)
        if user and user[2] == self.__hash_password(old_pass):
            new_hash_pass = self.__hash_password(new_pass)
            self.__update_user_in_db("password_hash", new_hash_pass,
                                     "username", username)
            return True
        return False

    def update_username(self, old_username, new_username, password):
        user = self.__get_user_from_db("username", old_username)
        if user and user[2] == self.__hash_password(password):
            self.__update_user_in_db("username", new_username,
                                     "id", user[0])
            return True
        return False

    # admin methods
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
                return True
        return False

    def is_admin(self):
        """Check if current user is an admin"""
        return self.current_user and self.current_user['role'] == 'admin'

    # testing methods, will delete after
    def print_users(self):
        for i in self.__get_all_users_from_db():
            for j in i:
                print(j, end=" ")
            print()

    def get_security_question(self, username):
        cursor = self.db.conn.cursor()
        try:
            cursor.execute("SELECT security_question FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()

    def reset_password(self, username, security_answer, new_password):
        cursor = self.db.conn.cursor()
        try:
            # First verify the security answer
            cursor.execute("SELECT security_answer FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            
            if not result or result[0] != security_answer:
                return False
            
            # If security answer is correct, update the password
            new_hash_password = self.__hash_password(new_password)
            cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", 
                         (new_hash_password, username))
            self.db.conn.commit()
            return True
        finally:
            cursor.close()

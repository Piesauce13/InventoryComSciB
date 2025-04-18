import hashlib
# from database import Database

class AuthSystem:
    def __init__(self, db):
        self.db = db
        self.current_user = None

    # to encrypt password
    def __hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()


    # methods for mysql
    def __set_current_user(self, user):
        user_info = {"id": user[0],
                     "username": user[1],
                     "password": user[2],
                     "role": user[3]}
        self.current_user = user_info

    def __get_current_user(self):
        return self.current_user

    def __select_all_from_db(self, type_):
        with self.db.conn.cursor() as cursor:
            cursor.execute(f"SELECT {type_} FROM users;")
            return cursor.fetchall()

    def __get_all_users_from_db(self):
        return self.__select_all_from_db('*')

    def __get_user_from_db(self, con_type, con_value):
        with self.db.conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE {con_type} = %s;",
                           (con_value,))
            return cursor.fetchone()

    def __update_user_in_db(self, con_type, con_val, key, key_val):
        with self.db.conn.cursor() as cursor:
            cursor.execute(f"UPDATE users SET {con_type} = %s WHERE {key} = %s;",
                           (con_val, key_val))
            self.db.conn.commit()

    def __insert_user_to_db(self, username, password, role):

        with self.db.conn.cursor() as cursor:
            cursor.execute("""
                                INSERT IGNORE INTO users (username, password_hash, role)
                                    VALUES(%s, %s, %s)
                                """, (username, password, role))
            self.db.conn.commit()

    def __remove_user_from_db(self, username):
        with self.db.conn.cursor() as cursor:
            cursor.execute("DELETE FROM users WHERE username = %s;", (username,))
            self.db.conn.commit()


    # methods for auth and personal info
    def registration(self, username, password, role):
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

        if self.current_user and self.current_user['role'] == 'admin':
            user = self.__get_user_from_db("username", username)
            if user and admin_password == self.current_user["password"]:
                role = role if role in ["admin", "regular"] else "regular"
                self.__update_user_in_db("role", role,
                                       "username", username)
                return True
        return False

    def delete_user(self, username, admin_password):
        if self.current_user and self.current_user['role'] == 'admin':
            user = self.__get_user_from_db("username", username)
            if user and admin_password == self.current_user["password"]:
                self.__remove_user_from_db(username)

    # testing
    def __print_users(self):
        for i in self.__get_all_users_from_db():
            print(i)
        print(self.__get_user_from_db("username", "james"))

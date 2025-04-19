import hashlib
import sqlite3

# Define the authentication system class
class AuthSystem:
    def __init__(self, db):
        self.db = db
        self.current_user = None

    def hash_password(self, password):
        """Generate a hash for the given password"""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, password, role='regular'):
        """Register a new user"""
        try:
            cursor = self.db.conn.cursor()
            hashed_password = self.hash_password(password)
            
            cursor.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                (username, hashed_password, role)
            )
            self.db.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Username already exists
            return False
        except Exception as e:
            print(f"Registration error: {e}")
            return False

    def login(self, username, password):
        """Authenticate a user"""
        try:
            cursor = self.db.conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user and user['password_hash'] == self.hash_password(password):
                # Convert SQLite Row to dict for easier access
                self.current_user = dict(user)
                return True
            return False
        except Exception as e:
            print(f"Login error: {e}")
            return False

    def logout(self):
        """Log out the current user"""
        self.current_user = None
        return True

    def get_current_user(self):
        """Get the currently logged-in user"""
        return self.current_user
    
    def is_admin(self):
        """Check if current user is an admin"""
        return self.current_user and self.current_user['role'] == 'admin'
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def initialize_database():
    #initializing the database
        conn = sqlite3.connect('restauracja.db')
        conn.row_factory = sqlite3.Row
        return conn

def create_table():
    #connecting to the database
    with initialize_database() as conn:
        print("Opened database successfully")
        cursor = conn.cursor()
        #creating a restaurantTable table
        table = '''
            CREATE TABLE IF NOT EXISTS RestaurantTable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                status TEXT NOT NULL
            )'''
        cursor.execute(table)

        #creating a user type table
        userType = '''
            CREATE TABLE IF NOT EXISTS UserType (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                typeName TEXT NOT NULL
            )'''
        cursor.execute(userType)

        #creating a user table
        user = '''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                email TEXT NOT NULL,
                phoneNumber TEXT NOT NULL,
                userName TEXT UNIQUE,
                password TEXT,
                userTypeId INTEGER NOT NULL,
                FOREIGN KEY (userTypeId) REFERENCES UserType(id)
            )'''
        cursor.execute(user)

        #creating a reservation table
        reservation = '''
            CREATE TABLE IF NOT EXISTS Reservation(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                startTime TEXT NOT NULL,
                endTime TEXT NOT NULL,
                numberOfPeople INTEGER NOT NULL,
                status TEXT NOT NULL,
                restaurantTableId INTEGERNOT NULL,
                userId INTEGER NOT NULL,
                FOREIGN KEY (restaurantTableId) REFERENCES RestaurantTable(id),
                FOREIGN KEY (userId) REFERENCES USER(id)
            )'''
        cursor.execute(reservation)

        #saving changes and closing the connection
        conn.commit()
        print("Tables created successfully")
        conn.close()

def add_user(first_name, last_name, email, phone_number, user_name, password, user_type_id):

    #connecting to the database
    try:
        with initialize_database() as conn:
            cursor = conn.cursor()
            #inserting a new user into User table
            insert_user = '''
                INSERT INTO User
                (firstName, lastName, email, phoneNumber, userName, password, userTypeId)
                VALUES
                (?,?,?,?,?,?,?)
                '''
            #encrypting the password
            hashed_password = generate_password_hash(password, method='scrypt')
            cursor.execute(insert_user(
                    first_name, 
                    last_name, 
                    email, 
                    phone_number, 
                    user_name, 
                    hashed_password, 
                    user_type_id
                ))
            #saving changes and closing the connection
            conn.commit()
            print("User added successfully")
            conn.close()
            return True
        #handling exceptions
    except sqlite3.IntegrityError:
        print("Błąd: Taki użytkownik już istnieje.")
        return False
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return False

def get_user_by_username(user_name):
    #connecting to the database
    with initialize_database() as conn:
        cursor = conn.cursor()
        #retrieving user by username
        user = '''
            SELECT * FROM User WHERE userName = ?
        '''
        cursor.execute(user, (user_name,))
        user = cursor.fetchone()
        conn.close()
        return user
        

def main():
    create_table()

if __name__ == "__main__":
    main()
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


def initialize_database():
    # initializing the database
    conn = sqlite3.connect('restauracja.db')
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    # connecting to the database
    with initialize_database() as conn:
        print("Opened database successfully")
        cursor = conn.cursor()
        # creating a restaurantTable table
        table = '''
            CREATE TABLE IF NOT EXISTS RestaurantTable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                capacity INTEGER NOT NULL,
                status TEXT NOT NULL
            )'''
        cursor.execute(table)

        # creating a user type table
        userType = '''
            CREATE TABLE IF NOT EXISTS UserType (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                typeName TEXT NOT NULL
            )'''
        cursor.execute(userType)

        # creating a user table
        user = '''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                firstName TEXT NOT NULL,
                lastName TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phoneNumber TEXT NOT NULL,
                userName TEXT UNIQUE,
                password TEXT,
                userTypeId INTEGER NOT NULL,
                FOREIGN KEY (userTypeId) REFERENCES UserType(id)
            )'''
        cursor.execute(user)

        # creating a reservation table
        reservation = '''
            CREATE TABLE IF NOT EXISTS Reservation(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                startTime TEXT NOT NULL,
                endTime TEXT NOT NULL,
                numberOfPeople INTEGER NOT NULL,
                status TEXT NOT NULL,
                restaurantTableId INTEGER NOT NULL,
                userId INTEGER NOT NULL,
                FOREIGN KEY (restaurantTableId) REFERENCES RestaurantTable(id),
                FOREIGN KEY (userId) REFERENCES USER(id)
            )'''
        cursor.execute(reservation)

        # saving changes and closing the connection
        conn.commit()
        print("Tables created successfully")


# user functions
def add_user(first_name, last_name, email, phone_number, user_name, password, user_type_id):
    # connecting to the database
    try:
        with initialize_database() as conn:
            cursor = conn.cursor()
            # inserting a new user into User table
            insert_user = '''
                INSERT INTO User
                (firstName, lastName, email, phoneNumber, userName, password, userTypeId)
                VALUES
                (?,?,?,?,?,?,?)
                '''
            # encrypting the password
            hashed_password = generate_password_hash(password, method='scrypt')
            cursor.execute(insert_user, (
                first_name,
                last_name,
                email,
                phone_number,
                user_name,
                hashed_password,
                user_type_id
            ))
            # saving changes and closing the connection
            conn.commit()
            print("User added successfully")
            new_user_id = cursor.lastrowid
            return new_user_id
        # handling exceptions
    except sqlite3.IntegrityError as e:
        # To łapie błędy logiczne (Unique, Not Null)
        print(f"BŁĄD INTEGRALNOŚCI: {e}")  # <--- TO JEST KLUCZOWE!
        return False

    except sqlite3.Error as e:
        # To łapie błędy składni SQL i inne techniczne
        print(f"BŁĄD TECHNICZNY SQL: {e}")  # <--- TO TEŻ!
        return False

    except Exception as e:
        # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
        print(f"BŁĄD PYTHON: {e}")
        return False


def get_user_by_username(user_name):
    # connecting to the database
    conn = initialize_database()
    cursor = conn.cursor()
    # retrieving user by username
    user = '''
        SELECT * FROM User WHERE userName = ?
    '''
    cursor.execute(user, (user_name,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_user_by_email(email):
    # connecting to the database
    conn = initialize_database()
    cursor = conn.cursor()
    # retrieving user by email
    user = '''
        SELECT * FROM User WHERE email = ?
    '''
    cursor.execute(user, (email,))
    user = cursor.fetchone()
    return user


def get_user_by_phone_number(phone_number):
    # connecting to the database
    conn = initialize_database()
    cursor = conn.cursor()
    # retrieving user by phone number
    user = '''
        SELECT * FROM User WHERE phoneNumber = ?
    '''
    cursor.execute(user, (phone_number,))
    user = cursor.fetchone()
    return user


# reservation functions
def create_reservation(date, start_time, end_time, number_of_people, user_id):
    # connecting to the database
    with initialize_database() as conn:
        cursor = conn.cursor()
        # searching for a table with sufficient capacity
        capacity_search = '''
            SELECT id FROM RestaurantTable
            WHERE capacity >= ?
        '''
        cursor.execute(capacity_search, (number_of_people,))
        rows = cursor.fetchall()
        if not rows:
            print("No table with sufficient capacity found.")
            return False
        else:
            sufficient_capacity_tables = {row['id'] for row in rows}
        # searching for taken tables at the specified date and time
        taken_tables_search = '''
            SELECT restaurantTableId FROM Reservation
            WHERE date = ? AND (startTime < ? OR endTime > ?)
            '''
        cursor.execute(taken_tables_search, (date, end_time, start_time))
        taken_rows = cursor.fetchall()
        taken_tables = {row['restaurantTableId'] for row in taken_rows}
        # finding available tables
        available_tables = list(sufficient_capacity_tables - taken_tables)
        if not available_tables:
            print("No available tables found for the specified date and time.")
            return False
        # assigning the first available table
        assigned_table_id = available_tables[0]
        # inserting the reservation into the Reservation table
        insert_reservation = '''
            INSERT INTO Reservation
            (date, startTime, endTime, numberOfPeople, status, restaurantTableId, userId)
            VALUES
            (?,?,?,?,'Awaiting confirmation',?,?)
        '''
        cursor.execute(insert_reservation, (
            date,
            start_time,
            end_time,
            number_of_people,
            assigned_table_id,
            user_id
        ))
        # saving changes and closing the connection
        conn.commit()
        print("Reservation created successfully")
        return True

def modify_reservation_status(reservation_id, new_status):
    # connecting to the database
    with initialize_database() as conn:
        cursor = conn.cursor()
        # updating the reservation status
        update_status = '''
            UPDATE Reservation
            SET status = ?
            WHERE id = ?
        '''
        cursor.execute(update_status, (new_status, reservation_id))
        # saving changes and closing the connection
        conn.commit()
        print("Reservation status updated successfully")
        return True


def main():
    create_table()


if __name__ == "__main__":
    main()
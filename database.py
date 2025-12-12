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
                phoneNumber TEXT UNIQUE NOT NULL,
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


# user functions returns user_id
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
        print(f"BŁĄD INTEGRALNOŚCI: {e}")  
        return False

    except sqlite3.Error as e:
        # To łapie błędy składni SQL i inne techniczne
        print(f"BŁĄD TECHNICZNY SQL: {e}")  
        return False

    except Exception as e:
        # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
        print(f"BŁĄD PYTHON: {e}")
        return False

#getting user by any user data; returns a user
def get_user(column, user_data):
    with initialize_database() as conn:
        cursor = conn.cursor()
        user = f'''
            SELECT * FROM User WHERE {column} = ?;
        '''
        try:
            cursor.execute(user, (user_data,))
            user = cursor.fetchone()
            return user
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")  
            return False

        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False

        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return False    

#display a list of users of a certain type; returns a list of users
def get_users_by_role(user_type_id):
    with initialize_database() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT * FROM User WHERE userTypeId = ?;
        '''
        try:
            cursor.execute(query, (user_type_id, ))
            user_list = cursor.fetchall()
            return user_list
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")  
            return False

        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False

        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return False   

#reset password by user_id, returns True
def reset_password(user_id, password):
    with initialize_database as conn:
        cursor = conn.cursor()
        query = '''
            UPDATE User
            SET password = ?
            WHERE id = ?;
        '''
        # encrypting the password
        hashed_password = generate_password_hash(password, method='scrypt')      
        try:
            cursor.execute(query, (hashed_password, user_id, ))
            cursor.commit()
            print('Password changed successfully')
            return True
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")  
            return False
        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False
        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return False

#modify user by user_name returns True
def modify_user(user_id, column, user_data):
    with initialize_database() as conn:
        cursor = conn.cursor()
        sql_query = f'''
            UPDATE User
            SET {column} = ?
            WHERE id = ?;
        '''
        try:
            cursor.execute(sql_query, (user_data, user_id, ))
            conn.commit()
            print('User modified successfully')
            return True
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")
            return False
        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")
            return False
        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return False

#delete user by id returns True
def delete_user(user_id):
    with initialize_database() as conn:
        cursor = conn.cursor()
        query = '''
            DELETE FROM User WHERE id = ?;
        '''
        try:
            cursor.execute(query, (user_id, ))
            conn.commit()
            print('User deleted successfully')
            return True
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")  
            return False

        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False

        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return False

# reservation functions
#add reservation, returns reservation id
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
            return 1
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
            return 2
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
        new_reservation_id = cursor.lastrowid
        return new_reservation_id

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
        try:
            cursor.execute(update_status, (new_status, reservation_id))
            conn.commit()
            print("Reservation status updated successfully")
            return True
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")  
            return False

        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False

        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return False

#get one reservation by id
def get_reservation_by_id(reservation_id):
    with initialize_database() as conn:
        cursor = conn.cursor()
        query = '''
            SELECT * FROM Reservation WHERE id = ?;
        '''
        cursor.execute(query, (reservation_id))
        selected_reservation = cursor.fetchone()
    return selected_reservation

#display reservation; returns a list of reservations
def get_reservations():
    with initialize_database() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = f'''
            SELECT * FROM Reservation r LEFT JOIN User u ON r.userId = u.id;
        '''
        try:
            cursor.execute(query, )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
            return 0

#modify reservation returns True
def modify_reservation(date, start_time, end_time, number_of_people, reservation_id):
    with initialize_database() as conn:
        cursor = conn.cursor()
        query = f'''
            UPDATE Reservation
            SET 
            date = ?,
            startTime = ?,
            endTime = ?,
            numberOfPeople = ?
            WHERE id = ?;
        '''
        try:
            cursor.execute(query, (date, start_time, end_time, number_of_people, reservation_id))
            conn.commit()
            print('Reservation modified successfully.')
            return True
        except sqlite3.Error as e:
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False

#delete reservation returns True
def delete_reservation(reservation_id):
    with initialize_database as conn:
        cursor = conn.cursor()
        query = '''
            DELETE FROM Reservation WHERE id = ?;
        '''
        try:
            cursor.execute(query, (reservation_id, ))
            cursor.commit()
            print('Reservation deleted successfully')
            return True
        except sqlite3.IntegrityError as e:
            # To łapie błędy logiczne (Unique, Not Null)
            print(f"BŁĄD INTEGRALNOŚCI: {e}")  
            return False

        except sqlite3.Error as e:
            # To łapie błędy składni SQL i inne techniczne
            print(f"BŁĄD TECHNICZNY SQL: {e}")  
            return False

        except Exception as e:
            # To łapie błędy Pythona (np. literówka w nazwie zmiennej)
            print(f"BŁĄD PYTHON: {e}")
        return False

def main():
    create_table()


if __name__ == "__main__":
    main()
import sqlite3

def initialize_database():
    #initializing the database
    try:
        conn = sqlite3.connect('restauracja.db')
        conn.row_factory = sqlite3.Row
        return conn
    #handling exceptions
    except sqlite3.OperationalError:
        print('Nie można otworzyć pliku bazy danych. Sprawdź uprawnienia dostępu.\nZamykanie programu.')

def create_table():
    #connecting to the database
    conn = initialize_database()
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


def main():
    create_table()

if __name__ == "__main__":
    main()
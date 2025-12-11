import database as db
import sqlite3
from errors import UserAlreadyExistsError, DatabaseConnectionError
from werkzeug.security import check_password_hash

<<<<<<< HEAD
class User:
    def __init__(self, first_name, last_name, email, phone_number, user_type_id, user_name = None, password = None):
=======

class User:
    def __init__(self, first_name, last_name, email, phone_number, user_type_id, user_name=None, password=None):
>>>>>>> c63059f1cb96ac6f4a238a8c5a744794ffb290fb
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.user_type_id = user_type_id
        self.user_name = user_name
        self.password = password

    def save_user_info(self):
        try:
            user_id = db.add_user(
<<<<<<< HEAD
                    self.first_name,
                    self.last_name,
                    self.email,
                    self.phone_number,
                    self.user_name,
                    self.password,
                    self.user_type_id
=======
                self.first_name,
                self.last_name,
                self.email,
                self.phone_number,
                self.user_name,
                self.password,
                self.user_type_id
>>>>>>> c63059f1cb96ac6f4a238a8c5a744794ffb290fb
            )
            return user_id
        except sqlite3.IntegrityError:
            raise UserAlreadyExistsError('Użytkownik o takiej nazwie użytkownika już istnieje')
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f'Awaria bazy danych {e}')

    def login(self):
        user = db.get_user_by_username(self.user_name)
        if not user:
            return None
        elif user and check_password_hash(user['password', self.password]):
            return user
        else:
            return None

<<<<<<< HEAD
#Kelner=3, Menadżer=4, Właściciel=5       
    @property    
    def is_staff(self):
        return self.user_type_id in [3,4,5]
    
    @property
    def is_manager(self):
        return self.user_type_id in [4, 5]
    
=======
    # Kelner=3, Menadżer=4, Właściciel=5
    @property
    def is_staff(self):
        return self.user_type_id in [3, 4, 5]

    @property
    def is_manager(self):
        return self.user_type_id in [4, 5]

>>>>>>> c63059f1cb96ac6f4a238a8c5a744794ffb290fb

class Reservation:
    def __init__(self, date, start_time, end_time, number_of_people, user_id):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_people = number_of_people
        self.user_id = user_id
import database as db
from werkzeug.security import check_password_hash


class User:
    def __init__(self, first_name, last_name, email, phone_number, user_type_id, user_name=None, password=None,
                 id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.user_type_id = user_type_id
        self.user_name = user_name
        self.password = password

    def save_user_info(self):
        unique_columns = {'email': self.email, 'userName': self.user_name}
        for key in unique_columns.keys():
            user_in_db = db.get_user(key, unique_columns[key])
        if user_in_db:
            raise ValueError('Użytkownik już istnieje.')
        user_id = db.add_user(
            self.first_name,
            self.last_name,
            self.email,
            self.phone_number,
            self.user_name,
            self.password,
            self.user_type_id
        )
        return user_id

    def save_guest_info(self):
        if db.get_user('email', self.email):
            raise ValueError('Użytkownik już istnieje.')
        user_id = db.add_user(
            self.first_name,
            self.last_name,
            self.email,
            self.phone_number,
            None,
            None,
            self.user_type_id
        )
        return user_id

    @classmethod
    def login(cls, username, password):
        user = db.get_user('userName', username)
        if not user:
            return None
        elif not check_password_hash(user['password'], password):
            return None
        else:
            return cls(
                id=user['id'],
                first_name=user['firstName'],
                last_name=user['lastName'],
                email=user['email'],
                phone_number=user['phoneNumber'],
                user_name=user['userName'],
                password=user['password'],
                user_type_id=user['userTypeId']
            )

    # Kelner=3, Menadżer=4, Właściciel=5
    @property
    def is_staff(self):
        return self.user_type_id in [3, 4, 5]

    @property
    def is_manager(self):
        return self.user_type_id in [4, 5]

    # display user by username returns selected user
    def display_user(self):
        selected_user = db.get_user('userName', self.user_name)
        if selected_user:
            return selected_user
        else:
            raise ValueError('Użytkownik nie istnieje.')

    def get_user_by_email(self):
        selected_user = db.get_user('email', self.email)
        if selected_user:
            return True
        else:
            return False
    # reset password
    # modify user
    # delete user


class Reservation:
    def __init__(self, date, start_time, end_time, number_of_people, reservation_id=None):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_people = number_of_people
        self.id = reservation_id

    def check_available_tables(self) -> list[dict]:
        available_tables = db.check_for_available_tables(self.date, self.start_time, self.end_time,
                                                         self.number_of_people)
        return available_tables

    # add reservation
    def add_reservation(self, selected_table: int) -> int:
        new_reservation_id = db.create_reservation(
            selected_table,
            self.date,
            self.start_time,
            self.end_time,
            self.number_of_people,
            self.user_id
        )
        return new_reservation_id

    # modify reservation
    def modify_reservation(self, attributes_to_change):
        # 1. Aktualizacja obiektu w Pythonie
        for key, value in attributes_to_change.items():
            if hasattr(self, key):
                setattr(self, key, value)
        if self.id is None:
            raise ValueError("Nie można modyfikować rezerwacji, która nie ma ID!")
        else:
            return db.modify_reservation(
                self.date, self.start_time, self.end_time, self.number_of_people,
                self.id
            )


# display user by role, returns a list of all users with that role
def display_users_by_role(column):
    users_with_selected_role = db.get_users_by_role(user_type_id=int)
    if users_with_selected_role:
        return users_with_selected_role
    else:
        raise ValueError('Nie ma użytkowników z wybraną rolą.')
import database as db
from werkzeug.security import check_password_hash

class User:
    def __init__(self, first_name, last_name, email, phone_number, user_type_id, user_name, password, id =  None):
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
    @classmethod
    def login(cls, username, password):
        user = db.get_user('userName', username)
        if not user:
            return None
        elif not check_password_hash(user['password'], password):
            return None
        else:
            return cls(
                    id = user['id'],
                    first_name = user['firstName'],
                    last_name = user['lastName'],
                    email = user['email'],
                    phone_number = user['phoneNumber'],
                    user_name = user['userName'],
                    password = user['password'],
                    user_type_id = user['userTypeId']
                )

    # Kelner=3, Menadżer=4, Właściciel=5
    @property
    def is_staff(self):
        return self.user_type_id in [3, 4, 5]

    @property
    def is_manager(self):
        return self.user_type_id in [4, 5]
    
    #display user by username returns selected user
    def display_user(object):
        selected_user = db.get_user('userName', object.user_name)
        if selected_user:
            return selected_user
        else: 
            raise ValueError ('Użytkownik nie istnieje.')

    #reset password
    #modify user
    #delete user

class Reservation:
    def __init__(self, date, start_time, end_time, number_of_people, user_id):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.number_of_people = number_of_people
        self.user_id = user_id
    
    #add reservation
    def add_reservation(self):
        new_reservation_id = db.create_reservation(
            self.date,
            self.start_time,
            self.end_time,
            self.number_of_people,
            self.user_id
        )
        if new_reservation_id == 1:
            print("No table with sufficient capacity found.")
        elif new_reservation_id == 2:
            print("No available tables found for the specified date and time.")
        return new_reservation_id

    #modify reservation
    def modify_reservation_status(self):
        need_confirmation = db.display_reservation('status')

    #delete reservation

#display user by role, returns a list of all users with that role
def display_users_by_role(column):
    users_with_selected_role = db.get_users_by_role(user_type_id= int)
    if users_with_selected_role:
        return users_with_selected_role
    else:
        raise ValueError ('Nie ma użytkowników z wybraną rolą.')
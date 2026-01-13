import unittest
from classes import User, Reservation
from pydantic import ValidationError
from schemas import UserRegistrationModel, ReservationModel

'------------------------USER TESTS---------------------------------'


class Unit_testing_user(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            'first_name': 'Anna',
            'last_name': 'Kowalska',
            'email': 'akowalska@test.pl',
            'phone_number': '123456789',
            'user_name': 'annak74',
            'password': 'M3p3g0#un6t1ro',
            'user_type_id': '2'
        }

    # Inicjalizacja obiektu
    def test_validate_user(self):
        user = User(**self.valid_data)

        self.assertEqual(user.first_name, 'Anna')
        self.assertEqual(user.last_name, 'Kowalska')
        self.assertEqual(user.email, 'akowalska@test.pl')
        self.assertEqual(user.phone_number, '123456789')
        self.assertEqual(user.user_name, 'annak74')
        self.assertEqual(user.password, 'M3p3g0#un6t1ro')
        self.assertEqual(user.user_type_id, '2')

    # Weryfikacja właściwości is_staff
    def test_user_is_staff_proprety(self):
        waiter = User(id=1, first_name='Anna', last_name='Kowalska', email='akowalska@test.pl',
                      phone_number='123456789', user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=3)
        self.assertTrue(waiter.is_staff)

        manager = User(id=3, first_name='Hanna', last_name='Kowalska', email='hkowalska@test.pl',
                       phone_number='123456789', user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=4)
        self.assertTrue(manager.is_staff)

        member = User(id=2, first_name='Jan', last_name='Kowalski', email='jkowalska@test.pl', phone_number='123456789',
                      user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=2)
        self.assertFalse(member.is_staff)

        guest = User(id=4, first_name='Max', last_name='Kowalski', email='mkowalska@test.pl', phone_number='123456789',
                     user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=1)
        self.assertFalse(guest.is_staff)

    # Weryfikacja właściwości is_staff
    def test_user_is_manager_property(self):
        manager = User(id=3, first_name='Hanna', last_name='Kowalska', email='hkowalska@test.pl',
                       phone_number='123456789', user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=4)
        self.assertTrue(manager.is_manager)

        owner = User(id=4, first_name='Max', last_name='Kowalski', email='mkowalska@test.pl', phone_number='123456789',
                     user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=5)
        self.assertTrue(owner.is_manager)
        self.assertTrue(owner.is_staff)

        member = User(id=2, first_name='Jan', last_name='Kowalski', email='jkowalska@test.pl', phone_number='123456789',
                      user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=2)
        self.assertFalse(member.is_manager)

        waiter = User(id=1, first_name='Anna', last_name='Kowalska', email='akowalska@test.pl',
                      phone_number='123456789', user_name='annak74', password='M3p3g0#un6t1ro', user_type_id=3)
        self.assertFalse(waiter.is_manager)

    '------------------------USER REGISTRATION MODEL TESTS---------------------------------'

    # Poprawna rejestracja
    def test_validate_correct_user_data(self):
        user = UserRegistrationModel(**self.valid_data)

        self.assertEqual(user.first_name, 'Anna')
        self.assertEqual(user.last_name, 'Kowalska')
        self.assertEqual(user.email, 'akowalska@test.pl')
        self.assertEqual(user.phone_number, '123456789')
        self.assertEqual(user.user_name, 'annak74')
        self.assertEqual(user.password, 'M3p3g0#un6t1ro')
        self.assertEqual(user.user_type_id, 2)

    # Brakujące pola
    def test_missing_field(self):
        missing_data = self.valid_data.copy()

        del missing_data['user_name']
        with self.assertRaises(ValidationError):
            UserRegistrationModel(missing_data)

    def test_invalid_email_format(self):
        bad_data = self.valid_data.copy()
        bad_data['email'] = 'akowalska'

        with self.assertRaises(ValidationError):
            UserRegistrationModel(**bad_data)

    # Walidacja długości nazwy użytkownika
    def test_username_lenght(self):
        bad_data = self.valid_data.copy()
        bad_data['user_name'] = 'ann1'

        with self.assertRaises(ValidationError):
            UserRegistrationModel(**bad_data)

    # Walidacja długości hasła
    def test_password_lenght(self):
        bad_data = self.valid_data.copy()
        bad_data['password'] = 'M3p3g0#'

        with self.assertRaises(ValidationError):
            UserRegistrationModel(**bad_data)

    # custom validators tests
    # Walidacja imienia i nazwiska
    def test_name_validator(self):
        bad_data = self.valid_data.copy()
        bad_data['first_name'] = 'Anna123'
        bad_data['last_name'] = 'Kowal1/ska'

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Name must contain only letters', str(context.exception))

    # Walidacja numeru telefonu
    def test_phone_number_validator(self):
        bad_data = self.valid_data.copy()
        bad_data['phone_number'] = '1234567k'

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Phone number must be exactly 9 digits', str(context.exception))

    # Walidacja nazwy użytkownika
    def test_user_name_validator(self):
        bad_data = self.valid_data.copy()
        bad_data['user_name'] = 'Annak'

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Username must contain only letters and digits, with at least one of each',
                      str(context.exception))

    # Walidacja hasła (Polityka bezpieczeństwa
    def test_password_no_digit(self):
        bad_data = self.valid_data.copy()
        bad_data['password'] = 'M#p#g&UntIb'

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Password must contain at least one digit', str(context.exception))

    def test_password_blank_space(self):
        bad_data = self.valid_data.copy()
        bad_data['password'] = ' M3p3g0 #un6t1ro '

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Password must not contain spaces', str(context.exception))

    def test_password_no_upper(self):
        bad_data = self.valid_data.copy()
        bad_data['password'].lower()

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Password must contain at least one uppercase letter', str(context.exception))

    def test_password_no_lower(self):
        bad_data = self.valid_data.copy()
        bad_data['password'].upper()

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Password must contain at least one lowercase letter', str(context.exception))

    def test_password_no_lower(self):
        bad_data = self.valid_data.copy()
        bad_data['password'] = 'Mp3g0Un714Oj4la'

        with self.assertRaises(ValidationError) as context:
            UserRegistrationModel(**bad_data)
        self.assertIn('Password must contain at least one special character', str(context.exception))


'----------------------------RESERVATION TESTS------------------------------'


class Unit_testing_reservation(unittest.TestCase):
    def setUp(self):
        self.valid_data = {
            'date': '23/12/2025',
            'start_time': '15:00',
            'end_time': '17:00',
            'number_of_people': '4',
            'user_id': '3'
        }

    # walidacja czy klasa Reservation utworzy poprawny objekt na podstawie podanych danych
    def test_validate_reservation(self):
        reservation = Reservation(**self.valid_data)
        self.assertEqual(reservation.date, '23/12/2025')
        self.assertEqual(reservation.start_time, '15:00')
        self.assertEqual(reservation.end_time, '17:00')
        self.assertEqual(reservation.number_of_people, '4')
        self.assertEqual(reservation.user_id, '3')

    '----------------------------RESERVATION MODEL TESTS------------------------------'

    # walidacja czy klasa ReservationModel utworzy poprawny objekt na podstawie podanych danych
    def test_validate_correct_reservation(self):
        reservation = ReservationModel(**self.valid_data)
        self.assertEqual(reservation.date, '23/12/2025')
        self.assertEqual(reservation.start_time, '15:00')
        self.assertEqual(reservation.end_time, '17:00')
        self.assertEqual(reservation.number_of_people, '4')
        self.assertEqual(reservation.user_id, '3')

    # Walidacja daty
    # Scenariusz A: Format inny niż DD-MM-YYYY.
    def test_date_format_validation(self):
        bad_data = self.valid_data.copy()
        bad_data['date'] = '23.12.2025'

        with self.assertRaises(ValidationError) as context:
            ReservationModel(**bad_data)
        self.assertIn('Date must be in DD/MM/YYYY format', str(context.exception))

    # Scenariusz B: Data wsteczna (z przeszłości)
    def past_date_validation(self):
        bad_data = self.valid_data.copy()
        bad_data['date'] = '23/11/2025'

        with self.assertRaises(ValidationError) as context:
            ReservationModel(**bad_data)
        self.assertIn('Reservation date must be in the future', str(context.exception))

        # Walidacja formatu czasu

    def time_format_validation(self):
        bad_data = self.valid_data.copy()
        bad_data['start_time'] = '15.00'
        bad_data['end_time'] = 'siedemnasta:trzydziesci'

        with self.assertRaises(ValidationError) as context:
            ReservationModel(**bad_data)
        self.assertIn('Time must be in HH:MM format', str(context.exception))

    # Logika czasu trwania rezerwacji
    # Scenariusz A: Godzina zakończenia wcześniejsza lub równa godzinie rozpoczęcia.
    def time_format_validation(self):
        bad_data = self.valid_data.copy()
        bad_data['start_time'] = '15:00'
        bad_data['end_time'] = '14:00'

        with self.assertRaises(ValidationError) as context:
            ReservationModel(**bad_data)
        self.assertIn('End time must be after start time', str(context.exception))

    # Scenariusz B: Rezerwacja krótsza niż 1 godzina
    def time_format_validation(self):
        bad_data = self.valid_data.copy()
        bad_data['start_time'] = '15:00'
        bad_data['end_time'] = '15:30'

        with self.assertRaises(ValidationError) as context:
            ReservationModel(**bad_data)
        self.assertIn('Reservation must be at least 1 hour long', str(context.exception))

    # Scenariusz C: Rezerwacja dłuższa niż 4 godziny.
    def time_format_validation(self):
        bad_data = self.valid_data.copy()
        bad_data['start_time'] = '15:00'
        bad_data['end_time'] = '20:00'

        with self.assertRaises(ValidationError) as context:
            ReservationModel(**bad_data)
        self.assertIn('Reservation cannot be longer than 4 hours', str(context.exception))
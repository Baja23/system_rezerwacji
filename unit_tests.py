import unittest
from datetime import datetime, timedelta
from classes import User, Reservation

class Unit_testing(unittest.TestCase):
    #User class methods test
    def test_user_is_staff_proprety(self):
        waiter = User(id=1, first_name='Anna', last_name='Kowalska', email='akowalska@test.pl', phone_number='123456789', user_type_id=3)
        self.assertTrue(waiter.is_staff)

        manager = User(id=3, first_name='Hanna', last_name='Kowalska', email='hkowalska@test.pl', phone_number='123456789', user_type_id=4)
        self.assertTrue(manager.is_staff)

        member = User(id=2, first_name='Jan', last_name='Kowalski', email='jkowalska@test.pl', phone_number='123456789', user_type_id=2)
        self.assertFalse(member.is_staff)

        guest = User(id=4, first_name='Max', last_name='Kowalski', email='mkowalska@test.pl', phone_number='123456789', user_type_id=1)
        self.assertFalse(guest.is_staff)
    
    def test_user_is_manager_property(self):
        waiter = User(id=1, first_name='Anna', last_name='Kowalska', email='akowalska@test.pl', phone_number='123456789', user_type_id=3)
        self.assertTrue(waiter.is_staff)

        manager = User(id=3, first_name='Hanna', last_name='Kowalska', email='hkowalska@test.pl', phone_number='123456789', user_type_id=4)
        self.assertTrue(manager.is_manager)

        guest = User(id=4, first_name='Max', last_name='Kowalski', email='mkowalska@test.pl', phone_number='123456789', user_type_id=1)
        self.assertFalse(guest.is_staff)

        member = User(id=2, first_name='Jan', last_name='Kowalski', email='jkowalska@test.pl', phone_number='123456789', user_type_id=2)
        self.assertFalse(member.is_staff)
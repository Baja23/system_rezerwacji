from pydantic import BaseModel, Field, EmailStr, field_validator, ValidationError
import string
import re
import datetime


class UserRegistrationModel(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    phone_number: str = Field(...)
    user_name: str = Field(..., min_length=5)
    password: str = Field(..., min_length=10)
    user_type_id: int = Field(...)

    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.match(r'^[A-Za-z]+$', value):
            raise ValueError('Name must contain only letters')
        return value
    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value: str) -> str:
        if not re.match(r'^\d{9}$', value):
            raise ValueError('Phone number must be exactly 9 digits')
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value: str) -> str:
        if ' ' in value:
            raise ValueError('Password must not contain spaces')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char in string.punctuation for char in value):
            raise ValueError('Password must contain at least one special character')
        return value

    @field_validator('user_name')
    @classmethod
    def validate_user_name(cls, value: str) -> str:
        pattern = r'^(?=.*\d)(?=.*[a-zA-Z])[A-Za-z0-9]+$'
        if not re.match(pattern, value):
            raise ValueError('Username must contain only letters and digits, with at least one of each')
        return value


class ReservationModel(BaseModel):
    date: str = Field(...)
    start_time: str = Field(...)
    end_time: str = Field(...)
    number_of_people: int = Field(..., gt=0)

    @field_validator('date')
    @classmethod
    def validate_date(cls, value: str) -> str:
        try:
            reservation_date = datetime.datetime.strptime(value, '%d-%m-%Y').date()
            if reservation_date <= datetime.date.today():
                raise ValueError('Reservation date must be in the future')
        except ValueError:
            raise ValueError('Date must be in DD-MM-YYYY format')
        return value
    @field_validator('start_time', 'end_time')
    @classmethod
    def validate_time(cls, value: str) -> str:
        try:
            datetime.datetime.strptime(value, '%H:%M')
        except ValueError:
            raise ValueError('Time must be in HH:MM format')
        return value
    @field_validator('end_time')
    @classmethod
    def validate_end_time(cls, value: str, info) -> str:
        start_time_str = info.data.get('start_time')
        if start_time_str:
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.datetime.strptime(value, '%H:%M').time()
            if end_time <= start_time:
                raise ValueError('End time must be after start time')
            elif end_time - start_time < datetime.timedelta(hours=1):
                raise ValueError('Reservation must be at least 1 hour long')
            elif end_time - start_time > datetime.timedelta(hours=4):
                raise ValueError('Reservation cannot be longer than 4 hours')
        return value
from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator
import string
import re

class UserRegistrationModel(BaseModel):
    first_name: str=Field(..., pattern=r'^[A-Za-z]+$')
    last_name: str=Field(..., pattern=r'^[A-Za-z]+$')
    email: EmailStr=Field(...)
    phone_number: str=Field(..., pattern=r'^\d{9}$')
    user_name: str=Field(..., min_length=5)
    password: str=Field(..., min_length=10)
    user_type_id: int=Field(...)


    #Należy dopisać te metody klasy do app.py aby zostały wywołane
    @field_validator('password')
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
    def validate_user_name(cls, value: str) -> str:
        pattern=r'^(?=.*\d)(?=.*[a-zA-Z])[A-Za-z0-9]+$'
        if not re.match(pattern, value):
            raise ValueError('Username must not contain spaces')
        return value

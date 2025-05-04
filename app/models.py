from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional

class UserInfo(BaseModel):
    name: str
    phone: str
    email: EmailStr
    appointment_date: datetime
    
    @validator('phone')
    def validate_phone(cls, v):
        v = ''.join(filter(str.isdigit, v))  # Remove any non-digit characters
        if len(v) < 10:
            raise ValueError("Phone number must be at least 10 digits")
        return v
    
    @validator('appointment_date')
    def validate_future_date(cls, v):
        if v < datetime.now():
            raise ValueError("Appointment date must be in the future")
        return v
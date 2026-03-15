from typing import ClassVar
from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date, datetime, timedelta
from decimal import Decimal
from dateutil.relativedelta import relativedelta

from typing import Optional
from config import settings


class UserRegistrationSchema(BaseModel):
    username: str = Field('username', min_length=3, max_length=50)
    email: str = Field('email', min_length=3, max_length=50)
    password: str = Field('password', min_length=3, max_length=50)

class UserAutorizationionSchema(BaseModel):
    user_login: str
    password: str

class SUserPublic(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True
        # orm_mode = True

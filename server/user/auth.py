import bcrypt
from datetime import datetime, timedelta

from jose import JWTError, jwt
from pydantic import EmailStr

from user.dao import UserDAO
from config import settings



SECRET_KEY = settings.secret_key_for_jwt
ALGORITHM = settings.algorithm_for_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=3)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(user_login: str, password: str):
    user = await UserDAO.find_one_or_none(email=user_login)
    if not user:
        user = await UserDAO.find_one_or_none(username=user_login)
        if not user:
            return False

    if verify_password(password, user.password):
        return user
    
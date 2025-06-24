from fastapi import HTTPException, status

from core import security
from schemas import user as user_schema

fake_users_db = {}


def register_user(user: user_schema.UserCreate) -> user_schema.Token:
    """
    Register a new user and return an access token.
    This function should interact with the database to create a new user.
    """
    if user.email in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    hashed_password = security.get_password_hash(user.password)
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "hashed_password": hashed_password,
    }
    fake_users_db[user.email] = user_data
    user_login = user_schema.UserLogin(email=user.email, password=user.password)
    token = security.create_access_token(user_login)
    return token


def authenticate_user(user: user_schema.UserLogin) -> user_schema.Token:
    """
    Authenticate a user and return an access token.
    This function should verify the user's credentials against the database.
    """
    user_data = fake_users_db.get(user.email)
    if not user_data or not security.verify_password(user.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return security.create_access_token(user)

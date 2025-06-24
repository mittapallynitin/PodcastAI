from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from core import config
from schemas import user as user_schema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user: user_schema.UserLogin) -> user_schema.Token:
    """
    Create an access token with the given data and expiration time.
    """
    payload = user_schema.TokenPayLoad(
        email=user.email,
        exp=datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    encoded_jwt = jwt.encode(dict(payload), key=config.SECRET_KEY, algorithm=config.ALGORITHM)
    return user_schema.Token(
        access_token=encoded_jwt, token_type="bearer"
    )


def verify_access_token(token: str) -> user_schema.TokenPayLoad:
    jwt_data = {}
    try:
        jwt_data = jwt.decode(token, key=config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return user_schema.TokenPayLoad(**jwt_data)
    except JWTError as jwt_error:
        raise ValueError("Invalid token or expired token") from jwt_error

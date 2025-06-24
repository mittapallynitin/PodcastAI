from fastapi import APIRouter, status

from schemas import user as user_schema
from services import user as user_service

router = APIRouter(prefix="/auth")


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=user_schema.Token)
async def signup(user_create: user_schema.UserCreate) -> user_schema.Token:
    token = user_service.register_user(user_create)
    return token


@router.post("/login", response_model=user_schema.Token)
async def login(user_login: user_schema.UserLogin) -> user_schema.Token:
    token = user_service.authenticate_user(user_login)
    return token

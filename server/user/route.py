from fastapi import APIRouter, Request, status, Response, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from decimal import Decimal
import os

from user.schemas import UserRegistrationSchema, UserAutorizationionSchema, SUserPublic
from user.dao import UserDAO
from user.auth import authenticate_user, create_access_token, get_password_hash
from user.dependencies import get_current_user



router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/")
async def root():
    return {"status": 200, "details": "user api work"}


@router.post("/logout")
async def logout(response: JSONResponse):
    return response.delete_cookie(key="user_access_token", path="/")


@router.post("/registration")
async def registration(request: Request, response: Response, user_data: UserRegistrationSchema) -> Response:
    email_existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if email_existing_user:
        raise UserAlreadyExists("email exists")
    username_existing_user = await UserDAO.find_one_or_none(username=user_data.username)
    if username_existing_user:
        raise UserAlreadyExists("username exists")

    user = await UserDAO.add_one(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password),
    )

    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True)
    response.status_code = status.HTTP_201_CREATED

    return response


@router.post("/login")
async def login(request: Request, response: Response, user_data: UserAutorizationionSchema) -> Response:
    user_login = user_data.user_login
    password = user_data.password

    if not user_login or not password:
        return JSONResponse(status_code=400, content={"status": 400, "details": "Bad request"})

    user = await authenticate_user(user_login, password)

    if not user:
        return JSONResponse(status_code=401, content={"status": 401, "details": "Invalid credentials"})

    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie(key="user_access_token", value=access_token, httponly=True, max_age=259200)

    response.status_code = status.HTTP_201_CREATED

    return response


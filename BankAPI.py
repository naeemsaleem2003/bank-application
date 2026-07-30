import os
from typing import Optional

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from repositories.AccountRepository import AccountRepository
from repositories.TransactionRepository import TransactionRepository
from repositories.UserRepository import UserRepository

from services.account_service import AccountService
from services.auth_service import AuthenticationError, AuthService
from services.transaction_service import TransactionService


app = FastAPI(title="Bank Application API")

frontend_origins = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

user_repository = UserRepository()
account_repository = AccountRepository()
transaction_repository = TransactionRepository()

auth_service = AuthService(user_repository)
account_service = AccountService(account_repository, user_repository)
transaction_service = TransactionService(account_repository, transaction_repository)

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "bank_session")


class AmountRequest(BaseModel):
    amount: float


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


def _serialize_user(user):
    return {
        "userId": user.user_id,
        "name": user.name,
        "email": user.email,
        "createdAt": user.created_at,
    }


def _authentication_error():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )


def _cookie_secure():
    return os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"


def _set_session_cookie(response: Response, session_id: str):
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        secure=_cookie_secure(),
        samesite="lax",
        max_age=auth_service.session_max_age_seconds(),
        path="/",
    )


def _clear_session_cookie(response: Response):
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,
        secure=_cookie_secure(),
        samesite="lax",
        path="/",
    )


def get_current_user(
    session_id: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME),
):
    try:
        return auth_service.get_user_from_session(session_id)
    except AuthenticationError:
        raise _authentication_error()


@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    try:
        return _serialize_user(
            auth_service.register(body.name, body.email, body.password)
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.post("/auth/login")
def login(body: LoginRequest, response: Response):
    try:
        user = auth_service.authenticate(body.email, body.password)
        session_id = auth_service.create_session(user)
    except AuthenticationError:
        raise _authentication_error()
    _set_session_cookie(response, session_id)
    return _serialize_user(user)


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    session_id: Optional[str] = Cookie(default=None, alias=SESSION_COOKIE_NAME),
):
    auth_service.revoke_session(session_id)
    _clear_session_cookie(response)


@app.get("/auth/me")
def get_me(current_user=Depends(get_current_user)):
    return _serialize_user(current_user)


# Account

@app.get("/accounts")
def get_accounts(current_user=Depends(get_current_user)):
    return account_service.get_accounts_for_user(current_user.user_id)


@app.get("/accounts/{account_id}")
def get_account(account_id: int, current_user=Depends(get_current_user)):
    try:
        return account_service.get_account_for_user(account_id, current_user.user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))


@app.post("/accounts", status_code=status.HTTP_201_CREATED)
def create_account(account_type: str, current_user=Depends(get_current_user)):
    try:
        return account_service.create_account(current_user.user_id, account_type)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


# Transaction

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: int, body: AmountRequest, current_user=Depends(get_current_user)):
    try:
        return transaction_service.deposit(
            account_id, body.amount, current_user.user_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: int, body: AmountRequest, current_user=Depends(get_current_user)):
    try:
        return transaction_service.withdraw(
            account_id, body.amount, current_user.user_id
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))


@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: int, current_user=Depends(get_current_user)):
    try:
        return transaction_service.get_transactions(account_id, current_user.user_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
    except PermissionError as error:
        raise HTTPException(status_code=403, detail=str(error))


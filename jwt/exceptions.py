#jwt/exceptions.py
from fastapi import HTTPException, status


class JWTException(HTTPException):
    def __init__(self, detail: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        )


class TokenExpired(JWTException):
    def __init__(self):
        super().__init__("Token expired")


class InvalidToken(JWTException):
    def __init__(self):
        super().__init__("Invalid token")

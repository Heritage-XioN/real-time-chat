from pydantic import BaseModel, EmailStr


class Signup(BaseModel):
    email: EmailStr
    username: str
    password: str

    class Config:
        from_attributes = True


class SignupResponse(BaseModel):
    status: str


class LoginResponse(BaseModel):
    status: str
    access_token: str
    token_type: str

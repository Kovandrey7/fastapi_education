from pydantic import BaseModel, EmailStr


class ShowUser(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: list


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class RolesUpdate(BaseModel):
    role: list


class UserDelete(BaseModel):
    deleted_user_id: int

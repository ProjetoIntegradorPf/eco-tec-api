from uuid import UUID
import pydantic
from datetime import date


class UserBase(pydantic.BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: str


class UserCreateSchema(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class UserSchema(UserBase):
    id: UUID

    class Config:
        orm_mode = True
        from_attributes = True

from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, constr, validator
from babel import Locale
from sqlalchemy_utils import Country


class UserLogin(BaseModel):
    username: str
    password: str


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    email_validated: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    description: Optional[str] = None
    subjects: Optional[List[str]] = Field(
        [],
        description="A list of topics of the pathway."
    )
    language: Optional[Locale] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[list[Country]] = Field([], description="A list of countries, defined by country codes.")
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the pathway."
    )

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserSummary(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    subjects: Optional[List[str]] = Field(
        [],
        description="A list of topics of the pathway."
    )
    language: Optional[Locale] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the pathway."
    )

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: Optional[constr(min_length=8, max_length=64)] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    original: Optional[constr(min_length=8, max_length=64)] = None
    password: Optional[constr(min_length=8, max_length=64)] = None


class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    hashed_password: bool = Field(default=False, alias="password")
    totp_secret: bool = Field(default=False, alias="totp")
    language: Optional[str] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )

    class Config:
        allow_population_by_field_name = True

    @validator("hashed_password", pre=True)
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False

    @validator("totp_secret", pre=True)
    def evaluate_totp_secret(cls, totp_secret):
        if totp_secret:
            return True
        return False

    @validator("language", pre=True)
    def evaluate_language(cls, language):
        if language:
            return str(language)
        return None

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None
    totp_secret: Optional[str] = None
    totp_counter: Optional[int] = None

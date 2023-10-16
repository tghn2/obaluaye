from typing import Optional, Set
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, constr, validator

from app.schemas.base_schema import BaseSchema, LocaleType, CountryListType

class UserLogin(BaseModel):
    username: str
    password: str


# Shared properties
class UserBase(BaseSchema):
    email: Optional[EmailStr] = None
    email_validated: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None
    description: Optional[str] = None
    subjects: Optional[Set[str]] = Field(set(), description="A list of topics.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the pathway."
    )

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return {s for s in v}


class UserSummary(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    subjects: Optional[Set[str]] = Field(
        set(),
        description="A list of topics of the pathway."
    )
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return {s for s in v}


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


# Additional properties to return via API
class User(UserInDBBase):
    hashed_password: bool = Field(default=False, alias="password")
    totp_secret: bool = Field(default=False, alias="totp")
    completedPersonalPathway: bool = Field(default=False)
    personalPathway: Optional[UUID] = Field(None, description="Pathway associated identity.")
    invitationCount: int = Field(default=0)

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


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None
    totp_secret: Optional[str] = None
    totp_counter: Optional[int] = None

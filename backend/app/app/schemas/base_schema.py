from pydantic import (
    BaseModel,
    Field,
    validator,
)
from typing import (
    Optional,
    Set,
)
from uuid import UUID
from datetime import datetime
import re
from babel import Locale, UnknownLocaleError
from sqlalchemy_utils import Country

# ======================================================================================================================
# THIRD-PARTY TYPES FOR LOCALE AND COUNTRY
# https://github.com/pydantic/pydantic/issues/380#issuecomment-594639970
# https://stackoverflow.com/questions/68893175/error-value-not-declarable-with-json-schema-for-purepath-with-pydantic-and-fasta
# https://docs.pydantic.dev/latest/usage/types/custom/#handling-third-party-types - ONLY PYDANTIC 2.0
class LocaleType(Locale):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        try:
            return Locale(str(val).lower())
        except UnknownLocaleError:
            return None

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", example="fr")

class CountryType(Country):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        try:
            if isinstance(val, str):
                return Country(val.upper())
            if isinstance(val, Country):
                return Country(val.code)
        except (KeyError, ValueError):
            pass
        return None

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", example="FR")

class CountryListType(Country):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_type

    @classmethod
    def validate_type(cls, val):
        validated = []
        if isinstance(val, list):
            for v in val:
                try:
                    if isinstance(v, str):
                        validated.append(Country(v.upper()))
                    elif isinstance(val, cls):
                        validated.append(Country(v.code))
                except (KeyError, ValueError):
                    pass
        return validated

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string", example=["FR", "GB", "ZA"])

def locale_encoder(x: Locale | str):
    return str(x).lower()

def country_encoder(x: Country | str):
    if isinstance(x, Country):
        return x.code
    return x

# ======================================================================================================================

class BaseSchema(BaseModel):
    @property
    def as_db_dict(self):
        to_db = self.dict(exclude_defaults=True, exclude_none=True, exclude={"identifier, id"})
        for key in ["id", "identifier"]:
            if key in self.dict().keys():
                to_db[key] = self.dict()[key].hex
        return to_db

    class Config:
        orm_mode = True
        json_encoders = {Locale: locale_encoder, Country: country_encoder}


class BaseSummarySchema(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date last modified.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date last modified.")
    isPrivate: Optional[bool] = Field(False, description="Whether private to roleplayers.")
    title: Optional[str] = Field(None, description="A human-readable title.")
    name: Optional[str] = Field(None, description="A machine-readable name.")
    description: Optional[str] = Field(
        None,
        description="A short description.",
    )
    subjects: Optional[Set[str]] = Field([], description="A list of topics.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return {s for s in v}

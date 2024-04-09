from pydantic import BaseModel
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
                    elif isinstance(v, Country):
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

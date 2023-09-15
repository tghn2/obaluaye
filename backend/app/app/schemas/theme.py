from __future__ import annotations
from typing import Optional, List
from pydantic import Field, validator
from sqlalchemy.orm import Query
from uuid import UUID
from datetime import datetime
import re

from app.schemas.base_schema import BaseSchema, LocaleType, CountryListType
from app.schemas.resource import Resource


class ThemeBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    order: Optional[int] = Field(None, description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.")
    created: Optional[datetime] = Field(None, description="Automatically generated date theme was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date theme was last modified.")
    title: Optional[str] = Field(None, description="A human-readable title given to the theme.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the theme.")
    description: Optional[str] = Field(None, description="A short description of the theme.")
    subjects: Optional[List[str]] = Field([], description="A list of topics of the theme.")
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")
    spatial: Optional[str] = Field(None, description="Spatial characteristics of the theme.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return [s for s in v]


class ThemeCreate(ThemeBase):
    title: str = Field(..., description="A human-readable title given to the theme.")
    order: int = Field(..., description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.",)
    pathway_id: UUID = Field(..., description="Pathway associated identity.")


class ThemeUpdate(ThemeCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    title: Optional[str] = Field(None, description="A human-readable title given to the theme.")
    order: Optional[int] = Field(None, description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.")
    pathway_id: Optional[UUID] = Field(None, description="Pathway associated identity.")


class Theme(ThemeBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    order: int = Field(..., description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.")
    created: datetime = Field(..., description="Automatically generated date theme was created.")
    modified: datetime = Field(..., description="Automatically generated date theme was last modified.")
    title: str = Field(..., description="A human-readable title given to the theme.")
    resources: Optional[List[Resource]] = Field([], description="A list of resources relevant to this theme.")

    @validator("resources", pre=True)
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()

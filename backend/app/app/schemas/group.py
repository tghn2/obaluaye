from __future__ import annotations
from typing import Optional, List
from pydantic import Field, validator
from sqlalchemy.orm import Query
from babel import Locale
from sqlalchemy_utils import Country
from uuid import UUID
from datetime import datetime
import re

from app.schemas.base_schema import BaseSchema
from app.schemas.pathway import Pathway
from app.schemas.role import Role


class GroupBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date group was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date group was last modified.")
    title: Optional[str] = Field(None, description="A human-readable title given to the group.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the group.")
    description: Optional[str] = Field(None, description="A short description of the group.")
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

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None

    @validator("language", pre=True)
    def evaluate_lazy_language(cls, v):
        if v and isinstance(v, str):
            return Locale(v.lower())
        if v and isinstance(v, Locale):
            return Locale(str(v).lower())

    @validator("country", pre=True)
    def evaluate_lazy_country(cls, v):
        if v and isinstance(v, list):
            return [
                Country(c.upper()) if isinstance(c, str) else c
                for c in [c for c in v if isinstance(c, str) or isinstance(c, Country)]
            ]


class GroupCreate(GroupBase):
    title: str = Field(..., description="A human-readable title given to the group.")
    pathway_id: UUID = Field(..., description="Pathway associated identity.")


class GroupUpdate(GroupCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    title: Optional[str] = Field(None, description="A human-readable title given to the group.")
    pathway_id: Optional[UUID] = Field(None, description="Pathway associated identity.")


class Group(GroupBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date group was created.")
    modified: datetime = Field(..., description="Automatically generated date group was last modified.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the group.")
    title: str = Field(..., description="A human-readable title given to the group.")
    language: Optional[str] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[list[str]] = Field([], description="A list of countries, defined by country codes.")
    pathway: Pathway = Field(..., description="Research pathway objective for this group.")
    members: List[Role] = Field(..., description="Pathway members.")

    @validator("language", pre=True)
    def evaluate_lazy_language(cls, v):
        if v and isinstance(v, Locale):
            return str(v).lower()

    @validator("country", pre=True)
    def evaluate_lazy_country(cls, v):
        return [c.code if isinstance(c, Country) else c for c in v]

    @validator("members", pre=True)
    def evaluate_lazy_members(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()

from __future__ import annotations
from pydantic import (
    Field,
    validator,
)
from typing import (
    Optional,
    List,
    Set,
)
from uuid import UUID
from datetime import datetime
import re
from sqlalchemy.orm import Query

from app.schemas.base_schema import BaseSchema, LocaleType, CountryListType
from app.schemas.resource import Resource


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
    subjects: Optional[Set[str]] = Field(set(), description="A list of topics.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")
    order: Optional[int] = Field(
        None, description="Integer count for pathway themes, but can be overloaded for other uses."
    )
    resources: Optional[List[Resource]] = Field([], description="A list of resources relevant to this summary.")

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return {s for s in v}

    @validator("resources", pre=True)
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()
        return v

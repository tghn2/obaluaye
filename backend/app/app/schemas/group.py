from typing import Optional, List
from pydantic import Field, validator
from sqlalchemy.orm import Query
from uuid import UUID
from datetime import datetime
import re

from app.schemas.base_schema import BaseSchema, BaseSummarySchema, LocaleType, CountryListType
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
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the pathway."
    )

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None


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
    title: str = Field(..., description="A human-readable title given to the group.")
    pathway: BaseSummarySchema = Field(..., description="Research pathway objective for this group.")
    members: List[Role] = Field(..., description="Pathway members.")

    @validator("members", pre=True)
    def evaluate_lazy_members(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()

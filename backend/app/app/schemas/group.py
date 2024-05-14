from typing import Optional, List, Set
from pydantic import Field, validator
from sqlalchemy.orm import Query
from uuid import UUID
from datetime import datetime
import re

from app.schemas.base_schema import BaseSchema, LocaleType, CountryListType
from app.schemas.summary import BaseSummarySchema
from app.schemas.role import Role
from app.schemas.pathway import PathwaySummary


class GroupBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date group was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date group was last modified.")
    title: Optional[str] = Field(None, description="A human-readable title given to the group.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the group.")
    description: Optional[str] = Field(None, description="A short description of the group.")
    subjects: Optional[Set[str]] = Field(set(), description="A list of topics of the pathway.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")
    spatial: Optional[str] = Field(None, description="Spatial characteristics of the pathway.")
    isComplete: Optional[bool] = Field(False, description="Group manual validation of pathway completion.")
    isFeatured: Optional[bool] = Field(False, description="Group featured as exemplar.")

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return {s for s in v}


class GroupCreate(GroupBase):
    title: str = Field(..., description="A human-readable title given to the group.")
    isActive: Optional[bool] = Field(True, description="Group is public. False for admin groups.")
    # pathway_id: UUID = Field(..., description="Pathway associated identity.")


class GroupUpdate(GroupCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    title: Optional[str] = Field(None, description="A human-readable title given to the group.")


class Group(GroupBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date group was created.")
    modified: datetime = Field(..., description="Automatically generated date group was last modified.")
    title: str = Field(..., description="A human-readable title given to the group.")
    pathway: Optional[PathwaySummary] = Field(None, description="Research pathway objective for this group.")
    themes: Optional[List[BaseSummarySchema]] = Field([], description="Ordered list of themes for this group pathway")
    roles: Optional[List[Role]] = Field([], description="Group members.")
    roleCount: Optional[int] = Field(default=0, description="Count of group members.")
    readyToComplete: Optional[bool] = Field(False, description="Group pathway is algorithmically complete.")

    @validator("roles", pre=True)
    def evaluate_lazy_roles(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()
        return v

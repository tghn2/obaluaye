from __future__ import annotations
from typing import Optional, List, Set
from pydantic import Field, validator
from sqlalchemy.orm import Query
from uuid import UUID
from datetime import datetime
import re

from app.db.base_class import Base
from app.schemas.base_schema import BaseSchema, LocaleType, CountryListType
from app.schemas.summary import BaseSummarySchema
from app.schemas.resource import Resource
from app.schemas.node import NodeJourney


class ThemeBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    order: Optional[int] = Field(
        None,
        description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.",
    )
    created: Optional[datetime] = Field(None, description="Automatically generated date theme was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date theme was last modified.")
    title: Optional[str] = Field(None, description="A human-readable title given to the theme.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the theme.")
    description: Optional[str] = Field(None, description="A short description of the theme.")
    subjects: Optional[Set[str]] = Field(set(), description="A list of topics of the theme.")
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
    # title: str = Field(..., description="A human-readable title given to the theme.")
    order: int = Field(
        ...,
        description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.",
    )
    pathway_id: UUID = Field(..., description="Pathway associated identity.")


class ThemeUpdate(ThemeCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    title: Optional[str] = Field(None, description="A human-readable title given to the theme.")
    order: Optional[int] = Field(
        None,
        description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically.",
    )
    pathway_id: Optional[UUID] = Field(None, description="Pathway associated identity.")


class Theme(ThemeBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    order: int = Field(
        ..., description="Sorting order for multiple themes. Items with the same order value are sorted alphabetically."
    )
    created: datetime = Field(..., description="Automatically generated date theme was created.")
    modified: datetime = Field(..., description="Automatically generated date theme was last modified.")
    # title: str = Field(..., description="A human-readable title given to the theme.")
    nodes: Optional[List[NodeJourney]] = Field([], description="A list of nodes which define this pathway.")
    resources: Optional[List[Resource]] = Field([], description="A list of resources relevant to this theme.")
    pathway_id: UUID = Field(..., description="Pathway associated identity.")

    @validator("resources", pre=True)
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()
        return v

    @validator("nodes", pre=True)
    def evaluate_lazy_nodes(cls, v):
        if isinstance(v, Query):
            return v.all()
        return v


class ThemeJourney(Theme):
    group: Optional[BaseSummarySchema] = Field(None, description="Research group for this journey.")
    pathway: Optional[BaseSummarySchema] = Field(None, description="Research pathway objective for this journey.")
    journeyPath: Optional[List[UUID]] = Field([], description="Next point in pathway response. None if not available.")
    journeyBack: Optional[UUID] = Field(None, description="Previous point in pathway response. None if not available.")
    journeySequence: Optional[List[UUID]] = Field([], description="Ordered list of theme ids. None if not available.")
    nodes: Optional[List[NodeJourney]] = Field([], description="A list of nodes which define this pathway.")

    @validator("pathway", pre=True)
    def evaluate_lazy_pathway(cls, v):
        if isinstance(v, Base):
            return None
        return v

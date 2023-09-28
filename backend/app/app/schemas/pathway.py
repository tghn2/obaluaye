from __future__ import annotations
from typing import Optional, List, Set
from pydantic import Field, validator
from sqlalchemy.orm import Query
# from babel import Locale
# from sqlalchemy_utils import Country
from uuid import UUID
from datetime import datetime
import re

from app.schemas.base_schema import BaseSchema, LocaleType, CountryListType
from app.schemas.role import Role
from app.schemas.theme import Theme
# from app.schemas.node import Node
from app.schemas.resource import Resource
from app.schema_types.pathway import PathwayType


class PathwayBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date pathway was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date pathway was last modified.")
    isPrivate: Optional[bool] = Field(False, description="Whether the pathway is private to roleplayers.")
    isProtected: Optional[bool] = Field(False, description="Whether the pathway is protected to require views from logged-in users.")
    # https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset
    # https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-2
    title: Optional[str] = Field(None, description="A human-readable title given to the pathway.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the pathway.")
    description: Optional[str] = Field(None, description="A short description of the pathway.")
    pathType: PathwayType = Field(default=PathwayType.RESEARCH, description="The type of pathway this represents.")
    subjects: Optional[Set[str]] = Field(
        [],
        description="A list of topics of the pathway."
    )
    country: Optional[CountryListType] = Field([], description="A list of countries, defined by country codes.")
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the pathway."
    )
    temporalStart: Optional[datetime] = Field(
        None,
        description="Temporal start of the pathway."
    )
    temporalEnd: Optional[datetime] = Field(
        None,
        description="Temporal end of the pathway."
    )
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    bibliographicCitation: Optional[str] = Field(
        None,
        description="A bibliographic pathway for the pathway."
    )

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None

    @validator("subjects", pre=True)
    def evaluate_subjects(cls, v):
        return {s for s in v}


class PathwayCreate(PathwayBase):
    title: str = Field(..., description="A human-readable title given to the pathway.")


class PathwayUpdate(PathwayCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    title: Optional[str] = Field(None, description="A human-readable title given to the pathway.")


class Pathway(PathwayBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date pathway was created.")
    modified: datetime = Field(..., description="Automatically generated date pathway was last modified.")
    title: str = Field(..., description="A human-readable title given to the pathway.")
    themes: Optional[List[Theme]] = Field([], description="A list of themes which define the nodes in this pathway.")
    resources: Optional[List[Resource]] = Field([], description="A list of resources relevant to this pathway.")

    @validator("themes", pre=True)
    def evaluate_lazy_themes(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()
        return v

    @validator("resources", pre=True)
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()
        return v


class PathwayAdmin(Pathway):
    auths: List[Role] = Field(..., description="Pathway members.")

    @validator("auths", pre=True)
    def evaluate_lazy_auths(cls, v):
        if isinstance(v, Query):
            return v.all()

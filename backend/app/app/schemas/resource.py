from __future__ import annotations
from typing import Optional
from pydantic import Field, validator
from uuid import UUID
from datetime import datetime
import re

from app.schemas.base_schema import BaseSchema, LocaleType
from app.schema_types.resource import ResourceType


class ResourceBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date resource was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date resource was last modified.")
    title: Optional[str] = Field(None, description="A human-readable title given to the resource.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the resource.")
    description: Optional[str] = Field(None, description="A short description of the resource.")
    content: Optional[str] = Field(None, description="Content for the resource. Can be markdown or a link.")
    resourceType: Optional[ResourceType] = Field(None, description="The type of resource, which defines how to use the `content` field.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of resource. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )

    @validator("name", always=True)
    def evaluate_name(cls, v, values):
        if values.get("title"):
            # https://stackoverflow.com/a/57837793/295606
            return re.sub("[^a-z0-9-]", "", values["title"].lower().replace(" ", "-"))
        return None


class ResourceCreate(ResourceBase):
    title: str = Field(..., description="A human-readable title given to the resource.")
    resourceType: ResourceType = Field(..., description="The type of resource, which defines how to use the `content` field.")
    pathway_id: Optional[UUID] = Field(..., description="Pathway associated identity.")
    theme_id: Optional[UUID] = Field(..., description="Theme associated identity.")
    node_id: Optional[UUID] = Field(..., description="Node associated identity.")


class ResourceUpdate(ResourceCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    title: Optional[str] = Field(None, description="A human-readable title given to the resource.")
    resourceType: Optional[ResourceType] = Field(None, description="The type of resource, which defines how to use the `content` field.")


class Resource(ResourceBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date resource was created.")
    modified: datetime = Field(..., description="Automatically generated date resource was last modified.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the resource.")
    title: str = Field(..., description="A human-readable title given to the resource.")
    resourceType: ResourceType = Field(..., description="The type of resource, which defines how to use the `content` field.")

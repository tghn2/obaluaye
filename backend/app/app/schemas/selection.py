from __future__ import annotations
from typing import Optional, List
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, LocaleType


class SelectionBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date selection was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date selection was last modified.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of the terms. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    term: Optional[str] = Field(None, description="The term forming the ontology for this selection.")


class CollectionSelectionBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date collection was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date collection was last modified.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the collection.")
    title: Optional[str] = Field(None, description="A human-readable title given to the collection.")
    isMulti: Optional[bool] = Field(False, description="Selection for one, or multiple, terms.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of the terms. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )


class SelectionCreate(SelectionBase):
    name: str = Field(None, description="A machine-readable name given to the collection.")
    term: str = Field(..., description="The term forming the ontology for this selection.")
    collection_id: UUID = Field(..., description="CollectionSelection associated identity.")


class CollectionSelectionCreate(CollectionSelectionBase):
    pass


class SelectionUpdate(SelectionCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    term: Optional[str] = Field(None, description="The term forming the ontology for this selection.")
    collection_id: Optional[UUID] = Field(..., description="CollectionSelection associated identity.")


class CollectionSelectionUpdate(CollectionSelectionCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the collection.")


class Selection(SelectionBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date selection was created.")
    modified: datetime = Field(..., description="Automatically generated date selection was last modified.")
    term: str = Field(..., description="The term forming the ontology for this selection.")
    collection_id: UUID = Field(..., description="CollectionSelection associated identity.")


class Collection(CollectionSelectionBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date selection was created.")
    modified: datetime = Field(..., description="Automatically generated date selection was last modified.")
    selection: Optional[List[Selection]] = Field(
        [], description="List of selection schema defining this collection ontology list."
    )

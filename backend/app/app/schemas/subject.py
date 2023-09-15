from __future__ import annotations
from typing import Optional
from pydantic import Field
from uuid import UUID

from app.schemas.base_schema import BaseSchema


class SubjectBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    term: str = Field(..., description="Unique term, in any language.")


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(SubjectCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")


class Subject(SubjectBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")

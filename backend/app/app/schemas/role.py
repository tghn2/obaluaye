from __future__ import annotations
from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema
from app.schemas.user import UserSummary
from app.schema_types import RoleType


class RoleBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date role was created.")
    responsibility: RoleType = Field(default=RoleType.VIEWER, description="Responsibility assigned to this researcher.")

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    researcher_id: UUID = Field(..., description="Specified researcher with responsibility.")
    pathway_id: UUID = Field(..., description="Unique identity for the referenced pathway.")


class RoleUpdate(RoleBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class Role(BaseSchema):
    id: UUID = Field(..., description="Automatically generated unique identity for the invitation.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    researcher: UserSummary = Field(..., description="Specified researcher with responsibility.")
    responsibility: RoleType = Field(default=RoleType.VIEWER, description="Responsibility assigned to this researcher.")

    class Config:
        orm_mode = True

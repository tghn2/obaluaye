from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, LocaleType
from app.schemas.summary import BaseSummarySchema
from app.schemas.user import UserSummary


class CommentBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date comment was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date comment was last modified.")
    content: Optional[str] = Field(None, description="Comment for the response. Can be in markdown.")
    resolved: bool = Field(default=False, description="Whether this comment has been resolved.")
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )


class CommentCreate(CommentBase):
    researcher_id: UUID = Field(..., description="Project custodian responsible for the comment.")
    response_id: UUID = Field(..., description="Comment associated response identity.")
    content: str = Field(..., description="Comment for the response. Can be in markdown.")


class CommentUpdate(CommentBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the comment.")
    researcher_id: Optional[UUID] = Field(None, description="Project custodian responsible for the comment.")
    response_id: Optional[UUID] = Field(None, description="Comment associated response identity.")
    content: str = Field(..., description="Comment for the response. Can be in markdown.")


class Comment(CommentBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the comment.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    modified: datetime = Field(..., description="Automatically generated date was last modified.")
    researcher_id: Optional[UUID] = Field(None, description="Project custodian responsible for the comment.")
    researcher: UserSummary = Field(..., description="Person who wrote the comment.")
    content: str = Field(..., description="Comment for the response. Can be in markdown.")


class CommentJourney(Comment):
    group: Optional[BaseSummarySchema] = Field(None, description="Research group for this comment.")

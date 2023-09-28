from __future__ import annotations
from typing import Optional, List
from pydantic import Field, validator
from sqlalchemy.orm import Query
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, LocaleType
from app.schemas.form import FormAttributeModel
from app.schema_types.node import NodeType
from app.schemas.resource import Resource


class NodeBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date node was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date node was last modified.")
    question: Optional[str] = Field(None, description="The question required to be answered for this node.")
    order: Optional[int] = Field(None, description="Sorting order for multiple nodes.")
    formType: Optional[NodeType] = Field(None, description="The form of response.")
    form: Optional[FormAttributeModel] = Field(
        {},
        description="Dictionary defining the question in a `node`.",
    )
    language: Optional[LocaleType] = Field(
        None,
        description="Specify the language of pathway. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )


class NodeCreate(NodeBase):
    question: str = Field(..., description="The question required to be answered for this node.")
    order: int = Field(..., description="Sorting order for multiple themes.")
    formType: NodeType = Field(..., description="The type of node, which defines how to use the `content` field.")
    form: FormAttributeModel = Field(
        ...,
        description="Dictionary defining the question in a `node`.",
    )
    theme_id: Optional[UUID] = Field(None, description="Theme associated node.")
    pathway_id: Optional[UUID] = Field(None, description="Pathway associated node.")


class NodeUpdate(NodeCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    question: Optional[str] = Field(None, description="The question required to be answered for this node.")
    order: Optional[int] = Field(None, description="Sorting order for multiple nodes.")
    formType: Optional[NodeType] = Field(None, description="The type of node, which defines how to use the `content` field.")
    form: Optional[FormAttributeModel] = Field(
        {},
        description="Dictionary defining the question in a `node`.",
    )


class Node(NodeBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date node was created.")
    modified: datetime = Field(..., description="Automatically generated date node was last modified.")
    question: str = Field(..., description="The question required to be answered for this node.")
    order: int = Field(..., description="Sorting order for multiple themes.")
    formType: NodeType = Field(..., description="The type of node, which defines how to use the `content` field.")
    form: Optional[FormAttributeModel] = Field(
        {},
        description="Dictionary defining the question in a `node`.",
    )
    resources: Optional[List[Resource]] = Field([], description="A list of resources relevant to this node.")
    theme_id: Optional[UUID] = Field(None, description="Theme associated node.")

    @validator("resources", pre=True)
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            return v.all()
        return v

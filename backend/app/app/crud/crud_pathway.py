from __future__ import annotations
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User, Pathway, PathwayTitle, PathwayDescription
from app.schemas import PathwayCreate, PathwayUpdate, PathwayAdmin, Pathway as PathwayOut
from app.core.config import settings


class CRUDPathway(CRUDBase[Pathway, PathwayCreate, PathwayUpdate, PathwayOut]):
    pass

pathway = CRUDPathway(
    model=Pathway,
    schema=PathwayOut,
    i18n_terms={"title": PathwayTitle, "description": PathwayDescription}
)

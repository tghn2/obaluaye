from __future__ import annotations
from sqlalchemy.orm import Session  # noqa: F401

from app.crud.base import CRUDBase
from app.models import User, Pathway, PathwayTitle, PathwayDescription  # noqa: F401
from app.schemas import PathwayCreate, PathwayUpdate, PathwayAdmin, Pathway as PathwayOut  # noqa: F401
from app.core.config import settings  # noqa: F401


class CRUDPathway(CRUDBase[Pathway, PathwayCreate, PathwayUpdate, PathwayOut]):
    pass

pathway = CRUDPathway(
    model=Pathway,
    schema=PathwayOut,
    i18n_terms={"title": PathwayTitle, "description": PathwayDescription}
)

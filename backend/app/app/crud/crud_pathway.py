from sqlalchemy.orm import Session, Query  # noqa: F401
from datetime import datetime

from app.crud.base import CRUDBase
from app.models import User, Pathway, PathwayTitle, PathwayDescription  # noqa: F401
from app.schemas import PathwayCreate, PathwayUpdate, PathwayAdmin, Pathway as PathwayOut  # noqa: F401
from app.schema_types import PathwayType, RoleType
from app.core.config import settings  # noqa: F401


class CRUDPathway(CRUDBase[Pathway, PathwayCreate, PathwayUpdate, PathwayOut]):
    def _filter_multi(
        self,
        *,
        db_objs: Query,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        path_type: PathwayType | str | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> list[Pathway]:
        db_objs = super()._filter_multi(
            db_objs=db_objs,
            match=match,
            date_from=date_from,
            date_to=date_to,
            user=user,
            responsibility=responsibility,
        )
        if user:
            db_objs = db_objs.filter(self.model.isPrivate.is_(False))
        if path_type:
            db_objs = db_objs.filter(self.model.pathType == path_type)
        return db_objs

    def get_multi(
        self,
        db: Session,
        *,
        db_objs: Query | None = None,
        page: int = 0,
        page_break: bool = False,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        path_type: PathwayType | str | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> list[Pathway]:
        if not db_objs:
            # Permits foreign key lists to be filtered
            db_objs = db.query(self.model)
        db_objs = self._filter_multi(
            db_objs=db_objs,
            match=match,
            date_from=date_from,
            date_to=date_to,
            path_type=path_type,
            user=user,
            responsibility=responsibility
        )
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

pathway = CRUDPathway(
    model=Pathway,
    schema=PathwayOut,
    i18n_terms={"title": PathwayTitle, "description": PathwayDescription}
)

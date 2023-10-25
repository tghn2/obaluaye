from sqlalchemy.orm import Session
from datetime import datetime
from uuid import UUID

from app.crud.base import CRUDBase
from app.models import Comment, Response
from app.schemas import CommentCreate, CommentUpdate, Comment as CommentOut
from app.core.config import settings


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate, CommentOut]):
    def get_multi(
        self,
        db: Session,
        *,
        group_ids: list[UUID],
        page: int = 0,
        page_break: bool = False,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
    ) -> list[Comment]:
        db_objs = db.query(self.model).filter(
            self.model.response.has(
                Response.group_id.in_(group_ids)
            )
        )
        db_objs = self._filter_multi(
            db_objs=db_objs,
            date_from=date_from,
            date_to=date_to,
        ).order_by(None).order_by(self.model.created.desc())
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def resolve_comment(self, db: Session, *, db_obj: Comment) -> Comment:
        obj_in = CommentUpdate(**CommentOut.from_orm(db_obj).dict())
        resolved = False
        if db_obj.resolved:
            resolved = db_obj.resolved
        obj_in.resolved = not resolved
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

comment = CRUDComment(model=Comment)

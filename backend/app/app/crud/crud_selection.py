from __future__ import annotations
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Selection, SelectionTerm, User
from app.schemas import SelectionCreate, SelectionUpdate, Selection as SelectionOut


class CRUDSelection(CRUDBase[Selection, SelectionCreate, SelectionUpdate, SelectionOut]):

    def update_user(self, db: Session, *, user_obj: User, keys_in: list[str] = []) -> User:
        db_objs = [s for s in db.query(self.model).filter(self.model.id.in_(keys_in)).all()]
        user_obj.selection = db_objs
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj


selection = CRUDSelection(model=Selection, schema=SelectionOut, i18n_terms={"term": SelectionTerm})

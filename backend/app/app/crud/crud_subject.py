from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.base import CRUDBase
from app.models import Subject
from app.schemas import SubjectCreate, SubjectUpdate, Subject as SubjectOut


class CRUDSubject(CRUDBase[Subject, SubjectCreate, SubjectUpdate, SubjectOut]):

    def create(self, db: Session, *, obj_in: str) -> Subject:
        try:
            # https://stackoverflow.com/a/52075777/295606
            db_obj = self.model(obj_in)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            db.rollback()
            db_obj = db.query(self.model).filter(self.model.term == obj_in).first()
        return db_obj

subject = CRUDSubject(model=Subject)

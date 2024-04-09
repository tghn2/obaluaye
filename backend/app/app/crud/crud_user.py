from typing import Any, Dict, Optional, Union
from uuid import UUID
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.models.pathway import Pathway
from app.models.theme import Theme
from app.models.node import Node
from app.models.response import Response
from app.schema_types import PathwayType
from app.schemas.user import UserCreate, UserInDB, UserUpdate, User as UserOut
from app.schemas.totp import NewTOTP


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate, UserOut]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password) if obj_in.password is not None else None,
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        if update_data.get("email") and db_obj.email != update_data["email"]:
            update_data["email_validated"] = False
        if "selection_ids" in update_data:
            update_data.pop("selection_ids")
        # For validation in super update
        update_data["id"] = db_obj.id
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(plain_password=password, hashed_password=user.hashed_password):
            return None
        return user

    def validate_email(self, db: Session, *, db_obj: User) -> User:
        obj_in = UserUpdate(**UserInDB.from_orm(db_obj).dict())
        obj_in.email_validated = True
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def activate_totp(self, db: Session, *, db_obj: User, totp_in: NewTOTP) -> User:
        obj_in = UserUpdate(**UserInDB.from_orm(db_obj).dict())
        obj_in = obj_in.dict(exclude_unset=True)
        obj_in["totp_secret"] = totp_in.secret
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def deactivate_totp(self, db: Session, *, db_obj: User) -> User:
        obj_in = UserUpdate(**UserInDB.from_orm(db_obj).dict())
        obj_in = obj_in.dict(exclude_unset=True)
        obj_in["totp_secret"] = None
        obj_in["totp_counter"] = None
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def update_totp_counter(self, db: Session, *, db_obj: User, new_counter: int) -> User:
        obj_in = UserUpdate(**UserInDB.from_orm(db_obj).dict())
        obj_in = obj_in.dict(exclude_unset=True)
        obj_in["totp_counter"] = new_counter
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def toggle_user_state(self, db: Session, *, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
        db_obj = self.get_by_email(db, email=obj_in.email)
        if not db_obj:
            return None
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def has_password(self, user: User) -> bool:
        if user.hashed_password:
            return True
        return False

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_email_validated(self, user: User) -> bool:
        return user.email_validated

    def _get_pathway(self, db: Session, *, user: User) -> Pathway | None:
        node_obj = (
            db.query(Node)
            .filter(
                (Node.pathway.has(Pathway.pathType == PathwayType.PERSONAL))
                & (Node.responses.any(Response.respondent_id == user.id))
            )
            .first()
        )
        if not node_obj:
            return None
        return node_obj.pathway

    def has_completed_pathway(self, db: Session, *, user: User) -> bool:
        # Get the pathway
        pathway_obj = self._get_pathway(db=db, user=user)
        if not pathway_obj:
            return False
        # Get the last theme index for the pathway
        order = pathway_obj.themes.order_by(None).order_by(Theme.order.desc()).first().order
        last = [
            theme_obj.nodes.order_by(None).order_by(Node.order.desc()).first().id
            for theme_obj in pathway_obj.themes.filter(
                (Theme.order == order) & (Theme.pathway_id == pathway_obj.id)
            ).all()
        ]
        completed = (
            db.query(Node)
            .filter(
                (Node.pathway.has(Pathway.pathType == PathwayType.PERSONAL))
                & (Node.responses.any(Response.respondent_id == user.id))
                & (Node.id.in_(last))
            )
            .first()
        )
        if completed:
            return True
        return False

    def validate_pathway(self, db: Session, *, user: User, pathway: Pathway) -> Theme | None:
        pathway_obj = self._get_pathway(db=db, user=user)
        if pathway_obj and pathway_obj.id != pathway.id:
            # Case for viewing a personal pathway that isn't the one that the user is actually working on
            return False
        return True

    def get_pathway(self, db: Session, *, user: User) -> UUID | None:
        pathway_obj = self._get_pathway(db=db, user=user)
        if not pathway_obj:
            return None
        return pathway_obj.id


user = CRUDUser(model=User)

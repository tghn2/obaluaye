from sqlalchemy.orm import Session, Query
from uuid import UUID

from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate, Role as RoleOut
from app.models.user import User
from app.models import Group
from app.models.pathway import Pathway
from app.schema_types import RoleType
from app.core.config import settings


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate, RoleOut]):
    def create(
        self,
        db: Session,
        *,
        user: User,
        group: Group,
        pathway: Pathway,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> Role:
        obj_in = {
            "researcher_id": user.id,
            "group_id": group.id,
            "pathway_id": pathway.id,
            "responsibility": responsibility
        }
        obj_in = RoleCreate(**obj_in)
        return super().create(db=db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Role, responsibility: RoleType = RoleType.VIEWER) -> Role:
        obj_in = RoleUpdate.from_orm(db_obj)
        obj_in.responsibility = responsibility
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def _get_responsibility(self, *, responsibility: RoleType) -> list[RoleType]:
        responsibilities = [RoleType.CUSTODIAN]
        if responsibility == RoleType.CURATOR:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR]
        if responsibility == RoleType.RESEARCHER:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.RESEARCHER]
        if responsibility == RoleType.VIEWER:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.RESEARCHER, RoleType.VIEWER]
        return responsibilities

    def _get_filter(
        self,
        db: Session,
        *,
        user: User,
        group: Group | None = None,
        pathway: Pathway | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> Query | None:
        if not group and not pathway:
            raise ValueError("Must have at least one of either Group or Pathway")
        query = db.query(self.model)
        responsibilities = self._get_responsibility(responsibility=responsibility)
        filter = (
            (self.model.researcher_id == user.id)
            & (self.model.responsibility.in_(responsibilities))
        )
        if pathway:
            filter = filter & (self.model.pathway_id == pathway.id)
        if group:
            filter = filter & (self.model.group_id == group.id)
        return query.filter(filter)

    def has_responsibility(
        self,
        db: Session,
        *,
        user: User,
        group: Group | None = None,
        pathway: Pathway | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> bool:
        if user.is_superuser:
            return True
        query = self._get_filter(db=db, user=user, group=group, pathway=pathway, responsibility=responsibility)
        if query:
            return query.first() is not None
        return False

    def highest_responsibility(
        self,
        db: Session,
        *,
        user: User,
        group: Group | None = None,
        pathway: Pathway | None = None,
    ) -> RoleType | None:
        if user.is_superuser:
            return RoleType.CUSTODIAN
        for responsibility in [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.RESEARCHER]:
            query = self._get_filter(db=db, user=user, group=group, pathway=pathway, responsibility=responsibility)
            if query and query.first() is not None:
                return responsibility
        return None

    def get_pathway_for_group(
        self,
        db: Session,
        *,
        user: User,
        group: Group,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> Pathway | None:
        query = self._get_filter(db=db, user=user, group=group, responsibility=responsibility)
        db_obj = query.first()
        if db_obj:
            return db_obj.pathway
        return None

    def get_group_for_pathway(
        self,
        db: Session,
        *,
        user: User,
        pathway: Pathway,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> Pathway | None:
        query = self._get_filter(db=db, user=user, pathway=pathway, responsibility=responsibility)
        db_obj = query.first()
        if db_obj:
            return db_obj.group
        return None

    def get_responsibility_for_group(
        self,
        db: Session,
        *,
        user: User,
        group: Group,
    ) -> RoleType | None:
        query = self._get_filter(db=db, user=user, group=group)
        db_obj = query.first()
        if db_obj:
            return db_obj.responsibility
        return None

    def get_member_assignable_roles_for_group(
        self,
        db: Session,
        *,
        user: User,
        group: Group,
    ) -> list[RoleType]:
        # Given a group and user, return a list of roles the user could assign to group members that are less than their
        # limits
        role_lists = {
            "CUSTODIAN": ["CUSTODIAN", "CURATOR", "RESEARCHER", "VIEWER"],
            "CURATOR": ["CURATOR", "RESEARCHER", "VIEWER"],
            "RESEARCHER": ["RESEARCHER", "VIEWER"],
            "VIEWER": [],
        }
        member_role = self.get_responsibility_for_group(db=db, user=user, group=group)
        return role_lists.get(member_role.value, [])

    def get_multi_by_group(
        self, db: Session, *, group_id: UUID, page: int = 0, page_break: bool = False
    ) -> list[Role]:
        db_objs = db.query(self.model).filter(Role.group_id == group_id)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_multi_by_researcher(
        self, db: Session, *, researcher_id: str, page: int = 0, page_break: bool = False
    ) -> list[Role]:
        db_objs = db.query(self.model).filter(Role.researcher_id == researcher_id)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def remove_researcher_from_group(self, db: Session, *, user: User, group: Group) -> Group:
        db_objs = db.query(self.model).filter(
            (self.model.researcher_id == user.id)
            & (self.model.group_id == group.id)
        )
        for db_o in db_objs.all():
            db.delete(db_o)
        db.commit()
        db.refresh(group)
        return group


role = CRUDRole(
    model=Role,
    schema=RoleOut,
)

from babel import Locale
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql.expression import func
from datetime import datetime

from app.crud.base import CRUDBase
from app.models import User, Group, Role
from app.models.pathway import Pathway
from app.models.theme import Theme
from app.models.node import Node
from app.models.response import Response
from app.schemas import GroupCreate, GroupUpdate, Group as GroupOut
from app.schema_types import RoleType, PathwayType
from app.core.config import settings  # noqa: F401


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate, GroupOut]):
    def _filter_multi(
        self,
        *,
        db_objs: Query,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        language: str | Locale | None = None,
        complete: bool | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> list[Group]:
        if match:
            db_objs = db_objs.filter(
                (self.model.title_vector.match(str(match)) | self.model.description_vector.match(str(match)))
            )
        if language:
            language = self._fix_language(language)
            db_objs = db_objs.filter(self.model.language == language)
        if isinstance(public, bool):
            db_objs = db_objs.filter(self.model.isActive.is_(public))
        if isinstance(complete, bool):
            db_objs = db_objs.filter(self.model.isComplete.is_(complete))
        if isinstance(featured, bool):
            db_objs = db_objs.filter(self.model.isFeatured.is_(featured))
        return super()._filter_multi(
            db_objs=db_objs,
            date_from=date_from,
            date_to=date_to,
        )

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
        language: str | Locale | None = None,
        complete: bool | None = None,
        featured: bool | None = None,
        public: bool | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> list[Group]:
        if not db_objs:
            # Permits foreign key lists to be filtered
            db_objs = db.query(self.model)
        db_objs = self._filter_multi(
            db_objs=db_objs,
            match=match,
            date_from=date_from,
            date_to=date_to,
            language=language,
            complete=complete,
            featured=featured,
            public=public,
            user=user,
            responsibility=responsibility,
        )
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_featured(self, db: Session, *, language: str | Locale | None = None) -> Pathway:
        db_objs = db.query(self.model)
        db_objs = db_objs.filter((self.model.isFeatured.is_(True)) & (self.model.isActive.is_(True)))
        return db_objs.order_by(func.random()).limit(settings.FEATURED_MAX).all()

    def can_remove(self, *, user: User, group: Group, responsibility: RoleType = RoleType.VIEWER) -> bool:
        # ASSUMPTION: responsibility is calculated from:
        #   `crud.role.get_responsibility_for_group(db=db, user=user, group=group)`
        if user.is_superuser or responsibility == RoleType.CUSTODIAN:
            return True
        group_count = group.roles.filter(Role.responsibility == RoleType.RESEARCHER).count()
        if group_count == 1 and responsibility == RoleType.RESEARCHER:
            # Safe to assume if the user has a researcher responsibility in the Group, and there is only one user, then:
            return True
        return False

    def has_completed_pathway(self, group: Group) -> bool:
        # Get the pathway
        pathway_obj = group.responses.first()
        if not pathway_obj:
            return False
        try:
            pathway_obj = pathway_obj.node.pathway
        except Exception:
            return False
        # Get the last theme index for the pathway
        order = pathway_obj.themes.order_by(None).order_by(Theme.order.desc()).first().order
        last = [
            theme_obj.nodes.order_by(None).order_by(Node.order.desc()).first().id
            for theme_obj in pathway_obj.themes.filter(
                (Theme.order == order) & (Theme.pathway_id == pathway_obj.id)
            ).all()
        ]
        completed = group.responses.filter(
            (Pathway.pathType == PathwayType.RESEARCH) & (Response.group_id == group.id) & (Response.node_id.in_(last))
        ).first()
        if completed:
            return True
        return False

    def get_pathway(self, *, group: Group) -> Pathway | None:
        role_obj = group.roles.first()
        if role_obj and role_obj.pathway:
            return role_obj.pathway
        return None

    def get_working_response(self, group: Group) -> Theme | None:
        if not group.responses.first():
            try:
                return group.roles.first().pathway.themes.first()
            except Exception:
                return None
        # Get last updated
        response = group.responses.order_by(None).order_by(Response.modified.desc()).first()
        return response.node.theme

    def toggle_featured(self, db: Session, *, db_obj: Group) -> Group:
        obj_in = GroupUpdate(**GroupOut.from_orm(db_obj).dict())
        isFeatured = False
        if db_obj.isFeatured:
            isFeatured = db_obj.isFeatured
        obj_in.isFeatured = not isFeatured
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    def toggle_completed(self, db: Session, *, db_obj: Group) -> Group:
        if not self.has_completed_pathway(group=db_obj):
            return db_obj
        obj_in = GroupUpdate(**GroupOut.from_orm(db_obj).dict())
        isComplete = False
        if db_obj.isComplete:
            isComplete = db_obj.isComplete
        obj_in.isComplete = not isComplete
        return self.update(db=db, db_obj=db_obj, obj_in=obj_in)


group = CRUDGroup(
    model=Group,
    schema=GroupOut,
)

from sqlalchemy.orm import Session, Query  # noqa: F401
from sqlalchemy.sql.expression import func
from datetime import datetime
from uuid import UUID

from app.crud.base import CRUDBase
from app.models import User, Pathway, PathwayTitle, PathwayDescription, Theme, Node, Response  # noqa: F401
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
        private: bool | None = None,
        featured: bool | None = None,
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
        if not user:
            db_objs = db_objs.filter(self.model.isPrivate.is_(False))
        if path_type:
            db_objs = db_objs.filter(self.model.pathType == path_type)
        if isinstance(private, bool):
            db_objs = db_objs.filter(self.model.isPrivate.is_(private))
        if isinstance(featured, bool):
            db_objs = db_objs.filter(self.model.isFeatured.is_(featured))
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
        private: bool | None = None,
        featured: bool | None = None,
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
            private=private,
            featured=featured,
            user=user,
            responsibility=responsibility
        )
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_next_theme(self, *, pathway: Pathway | None = None, theme: Theme | None = None) -> list[UUID]:
        if not pathway and not theme:
            raise ValueError("Provide at least one of theme or pathway.")
        if pathway and not theme:
            return pathway.themes.first().id
        pathway_obj = theme.pathway
        return [
            t.id for t in pathway_obj.themes.filter(
                (Theme.pathway_id == pathway_obj.id)
                & (Theme.order == theme.order + 1)
            ).all()
        ]

    def get_featured(self, db: Session) -> Pathway:
        db_objs = db.query(self.model)
        db_objs = db_objs.filter(
            (self.model.isFeatured.is_(True))
            & (self.model.isPrivate.is_(False))
            & (self.model.pathType == PathwayType.RESEARCH)
        )
        return db_objs.order_by(func.random()).first()

    def get_previous_theme(self, *, theme: Theme, response: Response | None = None) -> UUID | None:
        if theme.order == 0:
            return None
        pathway_obj = theme.pathway
        previous_themes = [
            t for t in pathway_obj.themes.filter(
                (Theme.pathway_id == pathway_obj.id)
                & (Theme.order == theme.order - 1)
            ).all()
        ]
        if not previous_themes:
            return None
        if len(previous_themes) == 1:
            return previous_themes[0].id
        if response:
            for theme in previous_themes:
                # Get last node
                node = theme.nodes.order_by(None).order_by(Node.order.desc()).first()
                if node:
                    # Check if node has a response from the same group or respondent
                    check_response = node.responses.filter(
                        (Response.node_id == node.id)
                        & (
                            (Response.respondent_id == response.respondent_id)
                            | (Response.group_id == response.group_id)
                        )
                    ).first()
                    if check_response:
                        return theme.id
        return None

    def get_last_theme_order(self, pathway: Pathway) -> int:
        theme_obj = pathway.themes.order_by(None).order_by(Theme.order.desc()).first()
        if theme_obj:
            return theme_obj.order
        return 0

    def toggle_featured(self, db: Session, *, db_obj: Pathway) -> Pathway:
        isFeatured = False
        if db_obj.isFeatured:
            isFeatured = db_obj.isFeatured
        db_obj.isFeatured = not isFeatured
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


pathway = CRUDPathway(
    model=Pathway,
    schema=PathwayOut,
    i18n_terms={"title": PathwayTitle, "description": PathwayDescription}
)

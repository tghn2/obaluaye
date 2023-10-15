from app.crud.base import CRUDBase
from app.models import User, Group, Role
from app.models.pathway import Pathway
from app.models.theme import Theme
from app.models.node import Node
from app.models.response import Response
from app.schemas import GroupCreate, GroupUpdate, Group as GroupOut
from app.schema_types import RoleType, PathwayType


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate, GroupOut]):
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
                (Theme.order == order)
                & (Theme.pathway_id == pathway_obj.id)
            ).all()
        ]
        completed = group.responses.filter(
            (Pathway.pathType == PathwayType.RESEARCH)
            & (Response.group_id == group.id)
            & (Response.node_id.in_(last))
        ).first()
        if completed:
            return True
        return False

    def get_working_response(self, group: Group) -> Theme | None:
        if not group.responses.first():
            try:
                return group.roles.first().pathway.themes.first()
            except Exception:
                return None
        # Get last updated
        response = group.responses.order_by(None).order_by(Response.modified.desc()).first()
        return response.node.theme


group = CRUDGroup(
    model=Group,
    schema=GroupOut,
)

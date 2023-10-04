from app.crud.base import CRUDBase
from app.models import User, Group, Role
from app.schemas import GroupCreate, GroupUpdate, Group as GroupOut
from app.schema_types import RoleType


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


group = CRUDGroup(
    model=Group,
    schema=GroupOut,
)

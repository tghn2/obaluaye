from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import Group
from app.schemas import GroupCreate, GroupUpdate, Group as GroupOut


class CRUDGroup(CRUDBase[Group, GroupCreate, GroupUpdate, GroupOut]):
    pass

group = CRUDGroup(model=Group)

from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import Node, NodeQuestion, NodeForm
from app.schemas import NodeCreate, NodeUpdate, Node as NodeOut


class CRUDNode(CRUDBase[Node, NodeCreate, NodeUpdate, NodeOut]):
    pass

node = CRUDNode(
    model=Node,
    schema=NodeOut,
    i18n_terms={"question": NodeQuestion, "form": NodeForm}
)

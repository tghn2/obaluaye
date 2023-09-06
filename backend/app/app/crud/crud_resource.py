from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import Resource, ResourceTitle, ResourceDescription, ResourceContent
from app.schemas import ResourceCreate, ResourceUpdate, Resource as ResourceOut


class CRUDResource(CRUDBase[Resource, ResourceCreate, ResourceUpdate, ResourceOut]):
    pass

resource = CRUDResource(
    model=Resource,
    schema=ResourceOut,
    i18n_terms={"title": ResourceTitle, "description": ResourceDescription, "content": ResourceContent}
)

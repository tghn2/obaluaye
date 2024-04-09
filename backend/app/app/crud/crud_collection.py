from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import CollectionSelection, CollectionSelectionTitle
from app.schemas import (
    CollectionSelectionCreate,
    CollectionSelectionUpdate,
    Collection as CollectionOut,
)


class CRUDCollection(
    CRUDBase[CollectionSelection, CollectionSelectionCreate, CollectionSelectionUpdate, CollectionOut]
):
    pass


collection = CRUDCollection(
    model=CollectionSelection, schema=CollectionOut, i18n_terms={"title": CollectionSelectionTitle}
)

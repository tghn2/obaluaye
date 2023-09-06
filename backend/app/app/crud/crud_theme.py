from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import Theme, ThemeTitle, ThemeDescription
from app.schemas import ThemeCreate, ThemeUpdate, Theme as ThemeOut


class CRUDTheme(CRUDBase[Theme, ThemeCreate, ThemeUpdate, ThemeOut]):
    pass

theme = CRUDTheme(
    model=Theme,
    schema=ThemeOut,
    i18n_terms={"title": ThemeTitle, "description": ThemeDescription}
)

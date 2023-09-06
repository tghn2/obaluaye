from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import Comment
from app.schemas import CommentCreate, CommentUpdate, Comment as CommentOut


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate, CommentOut]):
    pass

comment = CRUDComment(model=Comment)

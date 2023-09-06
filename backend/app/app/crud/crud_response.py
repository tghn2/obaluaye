from __future__ import annotations

from app.crud.base import CRUDBase
from app.models import Response
from app.schemas import ResponseCreate, ResponseUpdate, Response as ResponseOut


class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate, ResponseOut]):
    pass

response = CRUDResponse(model=Response)

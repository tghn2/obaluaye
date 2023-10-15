from .crud_user import user  # noqa: F401
from .crud_token import token  # noqa: F401
from .crud_group import group  # noqa: F401
from .crud_role import role  # noqa: F401

from .crud_spaces import spaces  # noqa: F401
from .crud_files import files  # noqa: F401

from .crud_invitation import invitation  # noqa: F401
from .crud_resource import resource  # noqa: F401
from .crud_subject import subject  # noqa: F401
from .crud_pathway import pathway  # noqa: F401
from .crud_theme import theme  # noqa: F401
from .crud_node import node  # noqa: F401
from .crud_response import response  # noqa: F401
from .crud_comment import comment  # noqa: F401

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item, ItemI18N # optional i18n terms
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item, {"field": ItemI18N})

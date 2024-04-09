# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa: F401
from app.models.user import User, user_subject_table, user_selection_table  # noqa: F401
from app.models.token import Token  # noqa: F401
from app.models.group import Group, group_subject_table  # noqa: F401
from app.models.invitation import Invitation  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.node import Node, NodeQuestion, NodeForm  # noqa: F401
from app.models.comment import Comment  # noqa: F401
from app.models.response import Response  # noqa: F401
from app.models.subject import Subject  # noqa: F401
from app.models.resource import Resource, ResourceTitle, ResourceDescription, ResourceContent  # noqa: F401
from app.models.theme import Theme, ThemeTitle, ThemeDescription, theme_subject_table  # noqa: F401
from app.models.pathway import Pathway, PathwayTitle, PathwayDescription, pathway_subject_table  # noqa: F401
from app.models.selection import CollectionSelection, CollectionSelectionTitle, Selection  # noqa: F401

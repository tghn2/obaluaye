from enum import auto

from app.schema_types import BaseEnum


class RoleType(BaseEnum):
    CUSTODIAN = auto()
    CURATOR = auto()
    RESEARCHER = auto()
    VIEWER = auto()

    def describe(self):
        description = {
            "CUSTODIAN": "A person with administrative and management responsibility for a pathway.",
            "CURATOR": "A person with architecture and quality responsibility for a pathway.",
            "RESEARCHER": "A person with responsibility for responding to a pathway.",
            "VIEWER": "A person who can view, but not modify, existing resources.",
        }
        return description[self.value]

from enum import auto

from app.schema_types import BaseEnum


class NodeType(BaseEnum):
    VALUE = auto()
    VALUERANGE = auto()
    SCALE = auto()
    BOOLEAN = auto()
    SELECTONE = auto()
    SELECTMANY = auto()
    SELECTBRANCH = auto()
    UPLOAD = auto()

    def describe(self):
        description = {
            "VALUE": "Value",
            "VALUERANGE": "Value range",
            "SCALE": "Scale",
            "BOOLEAN": "Boolean",
            "SELECTONE": "Select one",
            "SELECTMANY": "Select many",
            "SELECTBRANCH": "Select branch",
            "UPLOAD": "Upload",
        }
        return description[self.value]

from enum import auto

from app.schema_types import BaseEnum


class PathwayType(BaseEnum):
    PERSONAL = auto()
    RESEARCH = auto()

    def describe(self):
        description = {
            "PERSONAL": "A personal development pathway. Each must complete one before starting any research pathway.",
            "RESEARCH": "A research pathway documenting and guiding the requirements for a study.",
        }
        return description[self.value]

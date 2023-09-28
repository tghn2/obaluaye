from enum import auto

from app.schema_types import BaseEnum


class ResourceType(BaseEnum):
    MARKDOWN = auto()
    DOWNLOAD = auto()
    WEBLINK = auto()

    def describe(self):
        description = {
            "MARKDOWN": "Content written in markdown format.",
            "DOWNLOAD": "A downloadable resource.",
            "WEBLINK": "A link to an online resource.",
        }
        return description[self.value]

from enum import auto

from app.schema_types import BaseEnum


class ValueType(BaseEnum):
    DATE = auto()
    DATETIME = auto()
    YEAR = auto()
    NUMBER = auto()
    INTEGER = auto()
    BOOLEAN = auto()
    ARRAY = auto()
    STRING = auto()

    def describe(self):
        description = {
            "DATE": "Date",
            "DATETIME": "Datetime",
            "YEAR": "Year",
            "NUMBER": "Number",
            "INTEGER": "Integer",
            "BOOLEAN": "Boolean",
            "ARRAY": "Array",
            "STRING": "String",
        }
        return description[self.value]

from typing import Optional, Dict, Any, Union, List
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

from app.schemas.base_schema import BaseSchema
from app.schema_types.node import NodeType
from app.schema_types.value import ValueType


class FormAttributeModel(BaseModel):
    # https://docs.pydantic.dev/latest/usage/models/#custom-root-types
    __root__: Dict[str, Any]

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    def __setitem__(self, item, term):
        self.__root__[item] = term

    @property
    def terms(self):
        return self.__root__


class TermModel(BaseSchema):
    id: UUID = Field(default_factory=uuid4, description="Automatically generated unique identity.")
    value: Optional[str] = Field(
        None,
        description="A value presented as a defined choice in the form."
    )
    label: Optional[str] = Field(
        None,
        description="A text label describing the expected value, especially where the form may be a scale."
    )
    branch: Optional[UUID] = Field(None, description="Theme id for following branch.")


class AnswerModel(BaseSchema):
    id: UUID = Field(..., description="UUID corresponding to the relevant TermModel.")
    value: Optional[str] = Field(
        None,
        description="A value presented as a defined choice in the form."
    )
    dtype: Optional[str] = Field(None, description="Response values will be coerced to this type.")


class ConstraintsModel(BaseSchema):
    dtype: ValueType = Field(default=ValueType.STRING, description="Response values will be coerced to this type.")
    limit: Optional[int] = Field(
        None,
        description="Absolute number of terms expected in response. If no limit, is defined by the formType."
    )
    range: bool = Field(
        default=False,
        description="If a range, then responses will be treated as `from` to `to`."
    )
    minimum: Optional[Union[int, float]] = Field(
        None,
        description="An integer that specifies the minimum of a value, or the minimum number of characters of a string, depending on the field type.",
    )
    maximum: Optional[Union[int, float]] = Field(
        None,
        description="An integer that specifies the maximum of a value, or the maximum number of characters of a string, depending on the field type.",
    )


class FormModel(BaseSchema):
    """
    Used for validation of dict / json attributes in a Node.
    The form of use is:

        {<language>: FormModel }

    where `<language>` is the language, with a fallback to either of settings.DEFAULT_LANGUAGE, or the only one there.
    """
    formType: NodeType = Field(default=NodeType.VALUE, description="Base form type - duplicated")
    required: bool = Field(default=False, description="Whether a response is required or not.")
    randomise: bool = Field(
        default=False,
        description="If `formType` presents options, whether to randomise those options."
    )
    terms: Optional[List[TermModel]] = Field([], description="List of form terms, if required.")
    constraints: Optional[ConstraintsModel] = Field({}, description="Form constraints")
    example: Optional[str] = Field(None, description="An example response.")

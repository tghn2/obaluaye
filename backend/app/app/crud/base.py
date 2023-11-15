from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept
from babel import Locale, UnknownLocaleError
from datetime import datetime
from uuid import UUID, uuid4
from collections.abc import MutableMapping

from app.db.base_class import Base
from app.core.config import settings
from app.models import Subject, User
from app.schema_types import RoleType
from app.schemas.base_schema import BaseSummarySchema, BaseSchema

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
OutputSchemaType = TypeVar("OutputSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, OutputSchemaType]):
    def __init__(
        self,
        *,
        model: Type[ModelType],
        schema: Type[OutputSchemaType] | None = None,
        i18n_terms: dict[str, DeclarativeAttributeIntercept] = {},
    ):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic schema class for model output
        * `i18n_terms`: A dictionary of model field names along with their related i18n dictionary collection models
        """
        self.model = model
        self.schema = schema
        self.i18n_terms = i18n_terms

    def _get_schema(
        self, *, db_obj: ModelType, schema: BaseModel, language: str | Locale | None = None
    ) -> dict[str, Any]:
        obj_out = {}
        if language:
            language = self._fix_language(language)
        for field in schema.__fields__:
            if not hasattr(db_obj, field):
                continue
            if field in self.i18n_terms:
                i18n_obj = getattr(db_obj, field)
                if not i18n_obj:
                    continue
                if i18n_obj.get(language):
                    obj_out[field] = getattr(i18n_obj[language], field)
                elif i18n_obj.get(db_obj.language):
                    obj_out[field] = getattr(i18n_obj[db_obj.language], field)
            else:
                attr = getattr(db_obj, field)
                if not isinstance(attr, Query):
                    obj_out[field] = attr
        if language:
            obj_out["language"] = language
        return obj_out

    def get_schema_summary(self, *, db_obj: ModelType, language: str | Locale | None = None) -> BaseSummarySchema:
        obj_out = self._get_schema(db_obj=db_obj, schema=BaseSummarySchema, language=language)
        return BaseSummarySchema(**obj_out)

    def get_schema(
        self, *, db_obj: ModelType, language: str | Locale | None = None, schema_out: BaseSchema | None = None
    ) -> OutputSchemaType:
        if not schema_out:
            schema_out = self.schema
        if not schema_out:
            raise ValueError("Output schema not defined.")
        obj_out = self._get_schema(db_obj=db_obj, schema=schema_out, language=language)
        return schema_out(**obj_out)

    def get(self, db: Session, id: str | UUID) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def _filter_multi(
        self,
        *,
        db_objs: Query,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> list[ModelType]:
        if date_from and date_to and date_from > date_to:
            date_to = None
        if date_to:
            if isinstance(date_to, str):
                date_to = datetime.strptime(date_to, "%Y-%m-%d")
            db_objs = db_objs.filter(self.model.created <= date_to)
        if date_from:
            if isinstance(date_from, str):
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
            db_objs = db_objs.filter(self.model.created >= date_from)
        return db_objs

    def get_multi(
        self,
        db: Session,
        *,
        db_objs: Query | None = None,
        page: int = 0,
        page_break: bool = False,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.VIEWER,
    ) -> list[ModelType]:
        if not db_objs:
            # Permits foreign key lists to be filtered
            db_objs = db.query(self.model)
        db_objs = self._filter_multi(
            db_objs=db_objs, match=match, date_from=date_from, date_to=date_to, user=user, responsibility=responsibility
        )
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def create_subjects(self, db: Session, *, objs_in: set[str]) -> set[Subject]:
        # Automatically populate subjects as a matter of course
        # Prevents subject term duplication (hopefully)
        db_objs = set()
        for obj_in in objs_in:
            try:
                # https://stackoverflow.com/a/52075777/295606
                db_obj = Subject(obj_in)
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            except IntegrityError:
                db.rollback()
                db_obj = db.query(Subject).filter(Subject.term == obj_in).first()
            if db_obj:
                db_objs.add(db_obj)
        return db_objs

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        if not isinstance(obj_in, dict):
            obj_in = obj_in.dict(exclude_unset=True)
        obj_in_data = jsonable_encoder(obj_in)
        if hasattr(self.model, "subjects") and obj_in_data.get("subjects", False):
            sbj_objs = obj_in_data.pop("subjects", None)
            obj_in_data["subject"] = self.create_subjects(db=db, objs_in=sbj_objs)
        if hasattr(self.model, "country") and obj_in_data.get("country", False):
            obj_in_data["country"] = obj_in["country"]
        if hasattr(self.model, "language") and obj_in_data.get("language", False):
            obj_in["language"] = self._fix_language(obj_in["language"])
            obj_in_data["language"] = obj_in["language"]
            for field in self.i18n_terms:
                if obj_in_data.get(field, False):
                    obj_in_data[field] = {
                        obj_in["language"]: self.i18n_terms[field](obj_in["language"], obj_in_data[field])
                    }
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if not db_obj.id == update_data["id"]:
            raise ValueError("Update error: mismatch between object and update data.")
        # CLEAN UP DICT
        update_data.pop("id", None)
        language = update_data.pop("language", None)
        # Seems to commit to db as lowercase, so ensure this when checking for updates
        language = self._fix_language(language)
        if hasattr(db_obj, "language") and not db_obj.language and language:
            db_obj.language = language
        # UPDATE LOOP
        for field in update_data:
            if not hasattr(self.model, field):
                continue
            if field == "subjects":
                sbj_objs = self.create_subjects(db=db, objs_in=update_data.get(field, set()))
                for sbj_obj in sbj_objs:
                    db_obj.subject.add(sbj_obj)
            elif field in self.i18n_terms and language:
                # Create of the form Model(language, term, db_obj)
                i18n_obj = getattr(db_obj, field)
                if i18n_obj and i18n_obj.get(language):
                    i18n_obj = i18n_obj[language]
                    setattr(i18n_obj, field, update_data[field])
                else:
                    i18n_obj = self.i18n_terms[field](language, update_data[field], db_obj)
                db.add(i18n_obj)
                db.commit()
            else:
                setattr(db_obj, field, update_data[field])
                db.add(db_obj)
                db.commit()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: str | UUID) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def update_uuids(self, *, model: BaseModel | dict):
        # Influenced by https://stackoverflow.com/a/49723101/295606
        # Used to clone a pathway, mostly
        if isinstance(model, BaseModel):
            model = model.dict(by_alias=True, exclude_defaults=True, exclude_none=True)
        modified_model = {}
        for key, field in model.items():
            if key != "id":
                if isinstance(field, MutableMapping):
                    modified_model[key] = self.update_uuids(model=field)
                elif field and isinstance(field, list) and isinstance(field[0], MutableMapping):
                    # Assuming field consistency ... no mixed Mutables and non-Mutables
                    # Mutables being dictionaries here
                    modified_model[key] = []
                    for f in field:
                        modified_model[key].append(self.update_uuids(model=f))
                else:
                    modified_model[key] = field
            else:
                modified_model[key] = str(uuid4())
        return modified_model

    def _fix_language(self, language: str | Locale | None) -> Optional[Locale]:
        # Locale is saved as lowercase to the db
        if language and isinstance(language, Locale):
            language = Locale(str(language).lower())
        if language and isinstance(language, str):
            try:
                language = Locale(language.lower())
            except UnknownLocaleError:
                language = None
        return language

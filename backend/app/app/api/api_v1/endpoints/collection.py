from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Collection])
def read_all_collections(
    *,
    db: Session = Depends(deps.get_db),
    language: str | None = None,
    selections: bool = False,
    page: int = 0,
    current_user: models.User | None = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all collection selections.
    """
    db_objs = crud.collection.get_multi(
        db=db,
        page=page,
        user=current_user,
    )
    if not db_objs:
        # INITIALISE
        language = "en"
        terms = [
            {
                "name": "jobrole",
                "title": "Job Role",
                "isMulti": False,
            },
            {
                "name": "organisation",
                "title": "Organisation",
                "isMulti": False,
            },
            {
                "name": "affiliation",
                "title": "Affiliation",
                "isMulti": True,
            },
        ]
        objs_in = [
            schemas.CollectionSelectionCreate(
                **{"name": t["name"], "title": t["title"], "isMulti": t["isMulti"], "language": language}
            )
            for t in terms
        ]
        for obj_in in objs_in:
            crud.collection.create(db=db, obj_in=obj_in)
        db_objs = crud.collection.get_multi(
            db=db,
            page=page,
            user=current_user,
        )
    response = []
    for db_obj in db_objs:
        obj_response = crud.collection.get_schema(db_obj=db_obj, language=language)
        obj_response.selection = []
        if selections:
            for selection_obj in db_obj.selection.all():
                selection_out = crud.selection.get_schema(db_obj=selection_obj, language=language)
                obj_response.selection.append(selection_out)
        response.append(obj_response)
    return response


@router.get("/{id}", response_model=schemas.Collection)
def get_collection(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None,
    current_user: models.User | None = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a collection.
    """
    db_obj = crud.collection.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either collection does not exist, or user does not have the rights for this request.",
        )
    response = crud.collection.get_schema(db_obj=db_obj, language=language)
    response.selection = []
    for selection_obj in db_obj.selection.all():
        selection_out = crud.selection.get_schema(db_obj=selection_obj, language=language)
        response.selection.append(selection_out)
    return response


@router.post("/", response_model=schemas.Collection)
def create_collection(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.CollectionSelectionCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a collection.
    """
    # Only a superuser (currently) can create a new collection
    collection_obj = crud.collection.create(db=db, obj_in=obj_in)
    return crud.collection.get_schema(db_obj=collection_obj, language=obj_in.language)


@router.put("/{id}", response_model=schemas.Collection)
def update_collection(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.CollectionSelectionUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a collection.
    """
    db_obj = crud.collection.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either collection does not exist, or user does not have the rights for this request.",
        )
    db_obj = crud.collection.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return crud.collection.get_schema(db_obj=db_obj, language=obj_in.language)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_collection(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Remove a collection. Researcher must be a CUSTODIAN.
    """
    db_obj = crud.collection.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either collection does not exist, or user does not have the rights for this request.",
        )
    crud.collection.remove(db=db, id=id)
    return {"msg": "Collection has been successfully removed."}

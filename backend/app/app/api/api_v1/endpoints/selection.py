from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Selection])
def read_all_selections(
    *,
    db: Session = Depends(deps.get_db),
    language: str | None = None,
    page: int = 0,
    current_user: models.User | None = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all selection.
    """
    db_objs = crud.selection.get_multi(
        db=db,
        page=page,
        user=current_user,
    )
    return [crud.selection.get_schema(db_obj=db_obj, language=language) for db_obj in db_objs]


@router.get("/{id}", response_model=schemas.Selection)
def get_selection(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None,
    current_user: models.User | None = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a selection.
    """
    db_obj = crud.selection.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either selection does not exist, or user does not have the rights for this request.",
        )
    response = crud.selection.get_schema(db_obj=db_obj, language=language)
    response.selection = []
    for selection_obj in db_obj.selections.all():
        selection_out = crud.selection.get_schema(db_obj=selection_obj, language=language)
        response.selection.append(selection_out)
    return response


@router.post("/", response_model=schemas.Selection)
def create_selection(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.SelectionCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a selection.
    """
    # Only a superuser (currently) can create a new selection
    selection_obj = crud.selection.create(db=db, obj_in=obj_in)
    return crud.selection.get_schema(db_obj=selection_obj, language=obj_in.language)


@router.put("/{id}", response_model=schemas.Selection)
def update_selection(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.SelectionUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a selection.
    """
    db_obj = crud.selection.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either selection does not exist, or user does not have the rights for this request.",
        )
    db_obj = crud.selection.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return crud.selection.get_schema(db_obj=db_obj, language=obj_in.language)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_selection(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Remove a selection. Researcher must be a CUSTODIAN.
    """
    db_obj = crud.selection.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either selection does not exist, or user does not have the rights for this request.",
        )
    crud.selection.remove(db=db, id=id)
    return {"msg": "Selection has been successfully removed."}

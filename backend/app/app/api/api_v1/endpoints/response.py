from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/pathway/{id}", response_model=list[schemas.Response])
def read_all_responses(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    match: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    page: int = 0,
    language: str | None = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all responses for a specified pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    db_objs = crud.response.get_multi(
        db=db,
        db_objs=db_obj.responses,
        match=match,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )
    return [crud.response.get_schema_summary(db_obj=db_obj, language=language) for db_obj in db_objs]

@router.get("/{id}", response_model=schemas.Response)
def get_response(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None
) -> Any:
    """
    Get a response.
    """
    db_obj = crud.response.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    return crud.response.get_schema(db_obj=db_obj, language=language)

@router.post("/", response_model=schemas.Response)
def create_response(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.ResponseCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a response.
    """
    db_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if not obj_in.pathway_id or not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    response_obj = crud.response.create(db=db, obj_in=obj_in)
    return crud.response.get_schema(db_obj=response_obj, language=obj_in.language)

@router.put("/{id}", response_model=schemas.Response)
def update_response(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.ResponseUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a response.
    """
    db_obj = crud.response.get(db=db, id=id)
    if not db_obj and not crud.role.has_responsibility(
        db=db, user=current_user, group=db_obj.group, responsibility=schema_types.RoleType.RESEARCHER
    ):
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    db_obj = crud.response.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return crud.response.get_schema(db_obj=db_obj, language=obj_in.language)

@router.delete("/{id}", response_model=schemas.Msg)
def remove_response(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a response. Researcher must be a RESEARCHER.
    """
    db_obj = crud.response.get(db=db, id=id)
    if not db_obj and not crud.role.has_responsibility(
        db=db, user=current_user, group=db_obj.group, responsibility=schema_types.RoleType.RESEARCHER
    ):
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    crud.response.remove(db=db, id=id)
    return {"msg": "Response has been successfully removed."}

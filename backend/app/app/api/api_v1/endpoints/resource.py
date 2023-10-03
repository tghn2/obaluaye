from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Resource])
def read_all_resources(
    *,
    db: Session = Depends(deps.get_db),
    match: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    page: int = 0,
    language: str | None = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all resources.
    """
    db_objs = crud.resource.get_multi(
        db=db,
        match=match,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )
    return [crud.resource.get_schema_summary(db_obj=db_obj, language=language) for db_obj in db_objs]


@router.get("/pathway/{id}", response_model=list[schemas.Resource])
def read_all_resources_for_pathway(
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
    Get all resources for a specified pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    db_objs = crud.resource.get_multi(
        db=db,
        db_objs=db_obj.resources,
        match=match,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )
    return [crud.resource.get_schema_summary(db_obj=db_obj, language=language) for db_obj in db_objs]

@router.get("/{id}", response_model=schemas.Resource)
def get_resource(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None
) -> Any:
    """
    Get a resource.
    """
    db_obj = crud.resource.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    return crud.resource.get_schema(db_obj=db_obj, language=language)


@router.post("/", response_model=schemas.Resource)
def create_resource(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.ResourceCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a resource.
    """
    db_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if not obj_in.pathway_id or not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    resource_obj = crud.resource.create(db=db, obj_in=obj_in)
    return crud.resource.get_schema(db_obj=resource_obj, language=obj_in.language)


@router.put("/{id}", response_model=schemas.Resource)
def update_resource(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.ResourceUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a resource. Handles both create and update.
    """
    # Check that pathway exists and user has appropriate auths
    pathway_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if not obj_in.pathway_id or not pathway_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=pathway_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    # Check if resource exists, and zero out pathway if this isn't specifically related to it
    if obj_in.pathway_id and (obj_in.theme_id or obj_in.node_id):
        obj_in.pathway_id = None
    resource_obj = crud.resource.get(db=db, id=id)
    if not resource_obj:
        resource_obj = crud.resource.create(db=db, obj_in=obj_in)
    else:
        resource_obj = crud.resource.update(db=db, db_obj=resource_obj, obj_in=obj_in)
    return crud.resource.get_schema(db_obj=resource_obj, language=obj_in.language)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_resource(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a resource. Researcher must be a CUSTODIAN.
    """
    db_obj = crud.resource.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj.pathway, responsibility=schema_types.RoleType.CUSTODIAN
    ):
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    crud.resource.remove(db=db, id=id)
    return {"msg": "Resource has been successfully removed."}

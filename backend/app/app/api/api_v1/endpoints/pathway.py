from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Pathway])
def read_all_pathways(
    *,
    db: Session = Depends(deps.get_db),
    match: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 0,
    language: str | None = None,
) -> Any:
    """
    Get all pathways.
    """
    db_objs = crud.pathway.get_multi(
        db=db,
        match=match,
        date_from=date_from,
        date_to=date_to,
        page=page,
    )
    return [crud.pathway.get_schema_summary(db_obj=db_obj, language=language) for db_obj in db_objs]


@router.get("/{id}", response_model=schemas.Pathway)
def get_pathway(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None
) -> Any:
    """
    Get a pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    response = crud.pathway.get_schema(db_obj=db_obj, language=language)
    response.themes = []
    for theme_obj in db_obj.themes.all():
        theme_out = crud.theme.get_schema(db_obj=theme_obj, language=language)
        theme_out.nodes = []
        for node_obj in theme_obj.nodes.all():
            node_out = crud.node.get_schema(db_obj=node_obj, language=language)
            theme_out.nodes.append(node_out)
        response.themes.append(theme_out)
    return response


@router.post("/", response_model=schemas.Pathway)
def create_pathway(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.PathwayCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a pathway.
    """
    # Only a superuser (currently) can create a new pathway
    # This automatically generates a group for further management
    pathway_obj = crud.pathway.create(db=db, obj_in=obj_in)
    # Create a group
    group_in = schemas.GroupCreate(**{
        "title": f"Group for {obj_in.title}",
        "language": obj_in.language,
        "pathway_id": pathway_obj.id,
    })
    group_obj = crud.group.create(db=db, obj_in=group_in)
    # And assign the custodial role to the pathway creator
    crud.role.create(
        db=db, user=current_user, group=group_obj, pathway=pathway_obj, responsibility=schema_types.RoleType.CUSTODIAN
    )
    return crud.pathway.get_schema(db_obj=pathway_obj, language=obj_in.language)


@router.put("/{id}", response_model=schemas.Pathway)
def update_pathway(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.PathwayUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    db_obj = crud.pathway.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return crud.pathway.get_schema(db_obj=db_obj, language=obj_in.language)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_pathway(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a pathway. Researcher must be a CUSTODIAN.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    crud.pathway.remove(db=db, id=id)
    return {"msg": "Pathway has been successfully removed."}

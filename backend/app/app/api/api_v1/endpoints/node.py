from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Node])
def read_all_nodes(
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
    Get all nodes.
    """
    db_objs = crud.node.get_multi(
        db=db,
        match=match,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )
    return [crud.node.get_schema_summary(db_obj=db_obj, language=language) for db_obj in db_objs]

@router.get("/pathway/{id}", response_model=list[schemas.Node])
def read_all_nodes_for_pathway(
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
    Get all nodes for a specified pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    db_objs = crud.node.get_multi(
        db=db,
        db_objs=db_obj.nodes,
        match=match,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )
    return [crud.node.get_schema_summary(db_obj=db_obj, language=language) for db_obj in db_objs]

@router.get("/{id}", response_model=schemas.Node)
def get_node(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None
) -> Any:
    """
    Get a node.
    """
    db_obj = crud.node.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either node does not exist, or user does not have the rights for this request.",
        )
    return crud.node.get_schema(db_obj=db_obj, language=language)

@router.post("/", response_model=schemas.Node)
def create_node(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.NodeCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a node.
    """
    db_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if not obj_in.pathway_id or not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    node_obj = crud.node.create(db=db, obj_in=obj_in)
    return crud.node.get_schema(db_obj=node_obj, language=obj_in.language)

@router.put("/{id}", response_model=schemas.Node)
def update_node(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.NodeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a node.
    """
    db_obj = crud.node.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj.pathway, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either node does not exist, or user does not have the rights for this request.",
        )
    db_obj = crud.node.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return crud.node.get_schema(db_obj=db_obj, language=obj_in.language)

@router.delete("/{id}", response_model=schemas.Msg)
def remove_node(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a node. Researcher must be a CUSTODIAN.
    """
    db_obj = crud.node.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj.pathway, responsibility=schema_types.RoleType.CUSTODIAN
    ):
        raise HTTPException(
            status_code=400,
            detail="Either node does not exist, or user does not have the rights for this request.",
        )
    crud.node.remove(db=db, id=id)
    return {"msg": "Node has been successfully removed."}

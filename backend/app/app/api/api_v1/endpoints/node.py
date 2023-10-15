from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()

@router.post("/{id}", response_model=schemas.Node)
def create_node(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.NodeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create or Update a node.
    """
    # Check that pathway exists and user has appropriate auths
    pathway_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if not obj_in.pathway_id or not pathway_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=pathway_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either node does not exist, or user does not have the rights for this request.",
        )
    node_obj = crud.node.get(db=db, id=id)
    if not node_obj:
        node_obj = crud.node.create(db=db, obj_in=obj_in)
    else:
        node_obj = crud.node.update(db=db, db_obj=node_obj, obj_in=obj_in)
    return crud.node.get_schema(db_obj=node_obj, language=obj_in.language)

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

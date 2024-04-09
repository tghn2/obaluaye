from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.CommentJourney])
def read_all_comments(
    *,
    db: Session = Depends(deps.get_db),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all comments for a researcher.
    """
    if current_user.is_superuser:
        role_objs = crud.role.get_multi(
            db=db,
            date_from=date_from,
            date_to=date_to,
            page=page,
        )
    else:
        role_objs = crud.role.get_multi(
            db=db,
            db_objs=current_user.roles,
            date_from=date_from,
            date_to=date_to,
            page=page,
        )
    group_ids = [role_obj.group_id for role_obj in role_objs]
    db_objs = crud.comment.get_multi(
        db=db,
        group_ids=group_ids,
        date_from=date_from,
        date_to=date_to,
        page=page,
    )
    for db_obj in db_objs:
        db_obj.group = db_obj.response.group
    return db_objs


@router.get("/{id}", response_model=list[schemas.Comment])
def get_response_comments(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a comment.
    """
    db_obj = crud.response.get(db=db, id=id)
    if not db_obj or (db_obj.group and not crud.role.has_responsibility(db=db, user=current_user, group=db_obj.group)):
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or researcher does not have the rights for this request.",
        )
    return db_obj.comments.all()


@router.post("/{id}", response_model=schemas.Msg)
def create_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.CommentCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a comment.
    """
    # To create a comment, a researcher needs to have completed a personal pathway
    if not (crud.user.has_completed_pathway(db=db, user=current_user) or current_user.is_superuser):
        raise HTTPException(
            status_code=400,
            detail="Researcher has yet to complete a personal pathway before they can create a comment.",
        )
    db_obj = crud.response.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(db=db, user=current_user, group=db_obj.group):
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or researcher does not have the rights for this request.",
        )
    db_obj = crud.comment.create(db=db, obj_in=obj_in)
    return {"msg": str(db_obj.id)}


@router.put("/{id}", response_model=schemas.Msg)
def update_comment(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.CommentUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a comment. Must be creator of the comment.
    """
    db_obj = crud.comment.get(db=db, id=id)
    if (
        not db_obj
        or db_obj.researcher_id != current_user.id
        or not crud.role.has_responsibility(db=db, user=current_user, group=db_obj.response.group)
    ):
        raise HTTPException(
            status_code=400,
            detail="Either comment does not exist, or researcher does not have the rights for this request.",
        )
    db_obj = crud.comment.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return {"msg": str(db_obj.id)}


# @router.delete("/{id}", response_model=list[schemas.Comment])
# def remove_comment(
#     *,
#     db: Session = Depends(deps.get_db),
#     id: str,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Remove a comment. Must be creator of the comment.
#     """
#     db_obj = crud.comment.get(db=db, id=id)
#     if not db_obj or db_obj.researcher_id != current_user.id or not crud.role.has_responsibility(
#         db=db, user=current_user, comment=db_obj.response.group
#     ):
#         raise HTTPException(
#             status_code=400,
#             detail="Either comment does not exist, or researcher does not have the rights for this request.",
#         )
#     crud.comment.remove(db=db, id=id)
#     db_obj = crud.response.get(db=db, id=db_obj.response_id)
#     return db_obj.comments.all()


@router.post("/resolve/{id}", response_model=schemas.Msg)
def toggle_resolution_state(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Toggle comment resolution state.
    """
    db_obj = crud.comment.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(db=db, user=current_user, comment=db_obj.response.group):
        raise HTTPException(
            status_code=400,
            detail="Either comment does not exist, or researcher does not have the rights for this request.",
        )
    crud.comment.resolve_comment(db=db, db_obj=db_obj)
    return {"msg": str(db_obj.id)}

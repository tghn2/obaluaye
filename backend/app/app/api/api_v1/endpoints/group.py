from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/", response_model=list[schemas.Group])
def read_all_groups(
    *,
    db: Session = Depends(deps.get_db),
    match: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all groups for a researcher.
    """
    # Match can't do anything at this stage ... going to need to search on Groups not just Roles
    if current_user.is_superuser:
        db_objs = crud.role.get_multi(
            db=db,
            match=match,
            date_from=date_from,
            date_to=date_to,
            page=page,
        )
    else:
        db_objs = crud.role.get_multi(
            db=db,
            db_objs=current_user.roles,
            match=match,
            date_from=date_from,
            date_to=date_to,
            page=page,
        )
    objs_out = []
    group_uniques = set()
    for db_obj in db_objs:
        db_obj = db_obj.group
        if db_obj.id in group_uniques:
            continue
        else:
            group_uniques.add(db_obj.id)
        obj_out = crud.group.get_schema(db_obj=db_obj, language=db_obj.language, schema_out=schemas.Group)
        obj_out.roles = []
        pathway_obj = None
        for role_obj in db_obj.roles.all():
            if not pathway_obj:
                pathway_obj = role_obj.pathway
            obj_out.roles.append(crud.role.get_schema(db_obj=role_obj))
        obj_out.pathway = crud.pathway.get_schema(db_obj=pathway_obj, language=db_obj.language, schema_out=schemas.PathwaySummary)
        objs_out.append(obj_out)
    return objs_out


@router.get("/{id}", response_model=schemas.Group)
def get_group(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a group.
    """
    db_obj = crud.group.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(db=db, user=current_user, group=db_obj):
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    obj_out = crud.group.get_schema(db_obj=db_obj, language=db_obj.language, schema_out=schemas.Group)
    obj_out.roles = []
    pathway_obj = None
    for role_obj in db_obj.roles.all():
        if not pathway_obj:
            pathway_obj = role_obj.pathway
        obj_out.roles.append(crud.role.get_schema(db_obj=role_obj))
    obj_out.pathway = crud.pathway.get_schema(db_obj=pathway_obj, language=db_obj.language, schema_out=schemas.PathwaySummary)
    return obj_out


@router.post("/", response_model=schemas.Msg)
def create_group(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.GroupCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a group.
    """
    # To create a group, a researcher needs to have completed a personal pathway
    if not crud.user.has_completed_personal_pathway(user=current_user):
        raise HTTPException(
            status_code=400,
            detail="Researcher has yet to complete a personal pathway before they can create a group.",
        )
    db_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if not obj_in.pathway_id or not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or researcher does not have the rights for this request.",
        )
    group_obj = crud.group.create(db=db, obj_in=obj_in)
    crud.role.create(
        db=db, user=current_user, group=group_obj, pathway=db_obj, responsibility=schema_types.RoleType.RESEARCHER
    )
    return {"msg": "Group has been successfully created."}


@router.put("/{id}", response_model=schemas.Msg)
def update_group(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.GroupUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a group.
    """
    db_obj = crud.group.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, group=db_obj, responsibility=schema_types.RoleType.RESEARCHER
    ):
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    db_obj = crud.group.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return {"msg": "Group has been successfully updated."}


@router.delete("/{id}", response_model=schemas.Msg)
def remove_group(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a group. Researcher must be the last member of the group.
    """
    db_obj = crud.group.get(db=db, id=id)
    can_remove = False
    if db_obj:
        group_responsibility = crud.role.get_responsibility_for_group(db=db, user=current_user, group=db_obj)
        can_remove = crud.group.can_remove(user=current_user, group=db_obj, responsibility=group_responsibility)
    if not can_remove:
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    crud.group.remove(db=db, id=id)
    return {"msg": "Group has been successfully removed."}


@router.get("/{id}/members", response_model=list[schemas.Role])
def read_members(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a list of current group members.
    """
    db_obj = crud.group.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(db=db, user=current_user, group=db_obj):
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    return crud.role.get_multi_by_group(db=db, group_id=id, page=page)


@router.post("/{id}/members/{role_id}/{role_type}", response_model=list[schemas.Role])
def update_member_role(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    role_id: str,
    role_type: str,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a group role for a member.
    """
    db_obj = crud.group.get(db=db, id=id)
    role_obj = crud.role.get(db=db, id=role_id)
    valid_roles = []
    if db_obj:
        # Member can only assign roles up to their own responsibility level
        valid_roles = crud.role.get_member_assignable_roles_for_group(db=db, user=current_user, group=db_obj)
    if (
        role_type not in valid_roles
        or not db_obj
        or not role_obj
        or role_obj.group_id != db_obj.id
        or role_obj.researcher_id == current_user.id
        or not crud.role.has_responsibility(
            db=db, user=current_user, group=db_obj, responsibility=schema_types.RoleType.RESEARCHER
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    crud.role.update(db=db, db_obj=role_obj, responsibility=schema_types.RoleType(role_type))
    return crud.role.get_multi_by_group(db=db, group_id=id, page=page)


@router.delete("/{id}/members/{role_id}", response_model=list[schemas.Role])
def remove_member(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    role_id: str,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a group member.
    """
    db_obj = crud.group.get(db=db, id=id)
    role_obj = crud.role.get(db=db, id=role_id)
    if (
        not db_obj
        or not role_obj
        or role_obj.group_id != db_obj.id
        or role_obj.researcher_id == current_user.id
        or not crud.role.has_responsibility(
            db=db, user=current_user, group=db_obj, responsibility=schema_types.RoleType.RESEARCHER
        )
    ):
        # Cannot remove yourself from a group
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or user does not have the rights for this request.",
        )
    crud.role.remove_researcher_from_group(db=db, user=role_obj.researcher, group=db_obj)
    return crud.role.get_multi_by_group(db=db, group_id=id, page=page)


@router.get("/{id}/invitations", response_model=list[schemas.Invitation])
def read_invitations(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Invite a team member to a group.
    """
    db_obj = crud.group.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, group=db_obj, responsibility=schema_types.RoleType.RESEARCHER
    ):
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    db_objs = crud.invitation.get_multi_by_group(db=db, group_id=db_obj.id, page=page)
    objs_out = []
    for db_obj in db_objs:
        obj_out = crud.invitation.get_schema(db_obj=db_obj)
        obj_out.pathway = crud.pathway.get_schema_summary(db_obj=db_obj.pathway)
        obj_out.group = crud.group.get_schema_summary(db_obj=db_obj.group)
        objs_out.append(obj_out)
    return objs_out


@router.post("/{id}/invitations/{email_id}", response_model=list[schemas.Invitation])
def add_invitation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    email_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Invite a team member to a group.
    """
    db_obj = crud.group.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, group=db_obj, responsibility=schema_types.RoleType.RESEARCHER
    ):
        raise HTTPException(
            status_code=400,
            detail="Either group does not exist, or researcher does not have the rights for this request.",
        )
    pathway_id = db_obj.roles.first().pathway_id
    obj_in = schemas.InvitationCreate(**{
        "email": email_id,
        "sender_id": current_user.id,
        "group_id": db_obj.id,
        "pathway_id": pathway_id
    })
    try:
        crud.invitation.create(db=db, obj_in=obj_in)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail=f"You have already invited {obj_in.email}.",
        )
    db_objs = crud.invitation.get_multi_by_group(db=db, group_id=db_obj.id)
    objs_out = []
    for db_obj in db_objs:
        obj_out = crud.invitation.get_schema(db_obj=db_obj, schema_out=schemas.Invitation)
        obj_out.pathway = crud.pathway.get_schema_summary(db_obj=db_obj.pathway)
        obj_out.group = crud.group.get_schema_summary(db_obj=db_obj.group)
        objs_out.append(obj_out)
    return objs_out


@router.delete("/{id}/invitations/{invitation_id}", response_model=list[schemas.Invitation])
def remove_invitation(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    invitation_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove an invitation from a group.
    """
    db_obj = crud.group.get(db=db, id=id)
    invitation_obj = crud.invitation.get(db=db, id=invitation_id)
    if (
        not db_obj
        or invitation_obj.group_id != db_obj.id
        or not crud.role.has_responsibility(
            db=db, user=current_user, group=db_obj, responsibility=schema_types.RoleType.RESEARCHER
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Either of group or invitation do not exist, or researcher does not have the rights for this request.",
        )
    crud.invitation.remove(db=db, id=invitation_id)
    db_objs = crud.invitation.get_multi_by_group(db=db, group_id=db_obj.id)
    objs_out = []
    for db_obj in db_objs:
        obj_out = crud.invitation.get_schema(db_obj=db_obj, schema_out=schemas.Invitation)
        obj_out.pathway = crud.pathway.get_schema_summary(db_obj=db_obj.pathway)
        obj_out.group = crud.group.get_schema_summary(db_obj=db_obj.group)
        objs_out.append(obj_out)
    return objs_out

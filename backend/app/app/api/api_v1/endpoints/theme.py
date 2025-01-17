from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.ThemeJourney)
def get_personal_theme(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get a theme for a PERSONAL pathway. Can be used for response. Also include current responses is current user exists.
    """
    validated = False
    db_obj = crud.theme.get(db=db, id=id)
    # Could be trying to get first theme of pathway by called pathway itself
    if not db_obj:
        db_obj = crud.pathway.get(db=db, id=id)
        if db_obj:
            db_obj = db_obj.themes.first()
    if db_obj:
        validated = True
    response_obj = None
    if db_obj and db_obj.pathway and not db_obj.pathway.isPrivate and db_obj.pathway.pathType == "PERSONAL":
        validated = crud.user.validate_pathway(db=db, user=current_user, pathway=db_obj.pathway)
    if not validated:
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    # Validated, now return: pathway summary, theme -> node -> response
    response = crud.theme.get_schema(db_obj=db_obj, language=language, schema_out=schemas.ThemeJourney)
    response.pathway = crud.pathway.get_schema_summary(db_obj=db_obj.pathway, language=language)
    response.pathway.resources = []
    for resource_obj in db_obj.pathway.resources.all():
        resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
        response.pathway.resources.append(resources_out)
    response.pathway.order = crud.pathway.get_last_theme_order(pathway=db_obj.pathway)
    response.resources = []
    for resource_obj in db_obj.resources.all():
        resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
        response.resources.append(resources_out)
    response.nodes = []
    for node_obj in db_obj.nodes.all():
        node_out = crud.node.get_schema(db_obj=node_obj, language=language, schema_out=schemas.NodeJourney)
        node_out.resources = []
        for resource_obj in node_obj.resources.all():
            resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
            node_out.resources.append(resources_out)
        # Get the response, if exists
        response_obj = crud.response.get_from_node(node=node_obj, user=current_user)
        if response_obj:
            node_out.response = crud.response.get_schema(db_obj=response_obj)
        response.nodes.append(node_out)
    # Get page sequence in journey
    response.journeyPath = crud.pathway.get_next_theme(theme=db_obj)
    response.journeyBack = crud.pathway.get_previous_theme(theme=db_obj, response=response_obj)
    response.journeySequence = crud.pathway.get_theme_sequence(pathway=db_obj.pathway)
    return response


@router.get("/{group_id}/{id}", response_model=schemas.ThemeJourney)
def get_research_theme(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    group_id: str,
    language: str | None = None,
    current_user: models.User = Depends(deps.get_optional_current_user),
) -> Any:
    """
    Get a theme for a RESEARCH pathway. Can be used for response. Also include current responses is current user exists.
    """
    validated = False
    db_obj = crud.theme.get(db=db, id=id)
    group_obj = crud.group.get(db=db, id=group_id)
    # Could be a group trying to reach the first step in its pathway
    if not db_obj and group_obj:
        db_obj = crud.group.get_pathway(group=group_obj).themes.first()
    if db_obj and group_obj:
        validated = True
    if (
        group_obj
        and db_obj
        and db_obj.pathway
        and not db_obj.pathway.isPrivate
        and db_obj.pathway.pathType == "RESEARCH"
        and current_user
    ):
        validated = crud.role.has_responsibility(
            db=db, user=current_user, group=group_obj, responsibility=schema_types.RoleType.VIEWER
        )
        # An individual can chop and choose, but a group has only one working language
        language = group_obj.language
    if not validated:
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    # Validated, now return: pathway summary, theme -> node -> response
    response = crud.theme.get_schema(db_obj=db_obj, language=language, schema_out=schemas.ThemeJourney)
    response.pathway = crud.pathway.get_schema_summary(db_obj=db_obj.pathway, language=language)
    response.pathway.resources = []
    for resource_obj in db_obj.pathway.resources.all():
        resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
        response.pathway.resources.append(resources_out)
    response.pathway.order = crud.pathway.get_last_theme_order(pathway=db_obj.pathway)
    response.group = crud.group.get_schema_summary(db_obj=group_obj, language=language)
    response.resources = []
    for resource_obj in db_obj.resources.all():
        resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
        response.resources.append(resources_out)
    response.nodes = []
    for node_obj in db_obj.nodes.all():
        node_out = crud.node.get_schema(db_obj=node_obj, language=language, schema_out=schemas.NodeJourney)
        node_out.resources = []
        for resource_obj in node_obj.resources.all():
            resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
            node_out.resources.append(resources_out)
        # Get the response, if exists
        response_obj = crud.response.get_from_node(node=node_obj, group=group_obj)
        if response_obj:
            node_out.response = crud.response.get_schema(db_obj=response_obj)
        response.nodes.append(node_out)
    # Get next page in journey
    response.journeyPath = crud.pathway.get_next_theme(theme=db_obj)
    response.journeyBack = crud.pathway.get_previous_theme(theme=db_obj, response=response_obj)
    return response


@router.post("/{id}", response_model=schemas.Theme)
def create_theme(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.ThemeUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create or update a theme.
    """
    # Check that pathway exists and user has appropriate auths
    pathway_obj = crud.pathway.get(db=db, id=obj_in.pathway_id)
    if (
        not obj_in.pathway_id
        or not pathway_obj
        or not crud.role.has_responsibility(
            db=db, user=current_user, pathway=pathway_obj, responsibility=schema_types.RoleType.CURATOR
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    # Check if theme exists
    theme_obj = crud.theme.get(db=db, id=id)
    if not theme_obj:
        theme_obj = crud.theme.create(db=db, obj_in=obj_in)
    else:
        theme_obj = crud.theme.update(db=db, db_obj=theme_obj, obj_in=obj_in)
    return crud.theme.get_schema(db_obj=theme_obj, language=obj_in.language)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_theme(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a theme. Researcher must be a CUSTODIAN.
    """
    db_obj = crud.theme.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj.pathway, responsibility=schema_types.RoleType.CUSTODIAN
    ):
        raise HTTPException(
            status_code=400,
            detail="Either theme does not exist, or user does not have the rights for this request.",
        )
    crud.theme.remove(db=db, id=id)
    return {"msg": "Theme has been successfully removed."}

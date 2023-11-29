from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import io

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


def create_or_update_from_import(
    *, db: Session, obj_in: schemas.Pathway, user: models.User, db_obj: models.Pathway = None
) -> models.Pathway:
    """
    Create or update a pathway from an imported JSON file. Assumes that updates are for language changes rather than generic updates.
    """
    interim_in = crud.pathway.get_obj_as_dict(obj_in=obj_in)
    if not db_obj:
        pathway_in = schemas.PathwayCreate(**interim_in)
        pathway_obj = crud.pathway.create(db=db, obj_in=pathway_in)
        # Create a group
        group_in = schemas.GroupCreate(
            **{
                "title": f"Admin group for {obj_in.title}",
                "language": obj_in.language,
                "isActive": False,
            }
        )
        group_obj = crud.group.create(db=db, obj_in=group_in)
        # And assign the custodial role to the pathway creator
        crud.role.create(
            db=db, user=user, group=group_obj, pathway=pathway_obj, responsibility=schema_types.RoleType.CUSTODIAN
        )
    else:
        pathway_in = schemas.PathwayUpdate(**interim_in)
        pathway_obj = crud.pathway.update(
            db=db,
            db_obj=db_obj,
            obj_in=pathway_in,
        )
    # Resources
    if obj_in.resources and isinstance(obj_in.resources, list):
        for resource_obj in obj_in.resources:
            interim_in = crud.resource.get_obj_as_dict(obj_in=resource_obj)
            interim_in = schemas.ResourceUpdate(**interim_in)
            db_interim = crud.resource.get(db=db, id=resource_obj.id)
            if not db_interim:
                interim_in.pathway_id = obj_in.id
                crud.resource.create(db=db, obj_in=interim_in)
            else:
                crud.resource.update(db=db, db_obj=db_interim, obj_in=interim_in)
    # Themes
    if obj_in.themes and isinstance(obj_in.themes, list):
        for theme_obj in obj_in.themes:
            interim_in = crud.theme.get_obj_as_dict(obj_in=theme_obj)
            interim_in = schemas.ThemeUpdate(**interim_in)
            db_interim = crud.theme.get(db=db, id=theme_obj.id)
            if not db_interim:
                interim_in.pathway_id = obj_in.id
                crud.theme.create(db=db, obj_in=interim_in)
            else:
                crud.theme.update(db=db, db_obj=db_interim, obj_in=interim_in)
            # Resources
            if theme_obj.resources and isinstance(theme_obj.resources, list):
                for resource_obj in theme_obj.resources:
                    interim_in = crud.resource.get_obj_as_dict(obj_in=resource_obj)
                    interim_in = schemas.ResourceUpdate(**interim_in)
                    db_interim = crud.resource.get(db=db, id=resource_obj.id)
                    if not db_interim:
                        interim_in.pathway_id = obj_in.id
                        crud.resource.create(db=db, obj_in=interim_in)
                    else:
                        crud.resource.update(db=db, db_obj=db_interim, obj_in=interim_in)
            # Nodes
            if theme_obj.nodes and isinstance(theme_obj.nodes, list):
                for node_obj in theme_obj.nodes:
                    interim_in = crud.node.get_obj_as_dict(obj_in=node_obj)
                    interim_in = schemas.NodeUpdate(**interim_in)
                    db_interim = crud.node.get(db=db, id=node_obj.id)
                    if not db_interim:
                        interim_in.pathway_id = obj_in.id
                        crud.node.create(db=db, obj_in=interim_in)
                    else:
                        crud.node.update(db=db, db_obj=db_interim, obj_in=interim_in)
                    # Resources
                    if node_obj.resources and isinstance(node_obj.resources, list):
                        for resource_obj in node_obj.resources:
                            interim_in = crud.resource.get_obj_as_dict(obj_in=resource_obj)
                            interim_in = schemas.ResourceUpdate(**interim_in)
                            db_interim = crud.resource.get(db=db, id=resource_obj.id)
                            if not db_interim:
                                interim_in.pathway_id = obj_in.id
                                crud.resource.create(db=db, obj_in=interim_in)
                            else:
                                crud.resource.update(db=db, db_obj=db_interim, obj_in=interim_in)
    return crud.pathway.get(db=db, id=obj_in.id)


@router.get("/", response_model=list[schemas.PathwaySummary])
def read_all_public_pathways(
    *,
    db: Session = Depends(deps.get_db),
    match: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    path_type: Optional[str] = None,
    featured: bool | None = None,
    private: bool | None = None,
    language: str | None = None,
    page: int = 0,
    current_user: models.User | None = Depends(deps.get_optional_current_user),
) -> Any:
    """
    Get all public pathways. Check if current_user, and if they are pathway CUSTODIANs.
    """
    db_objs = crud.pathway.get_multi(
        db=db,
        match=match,
        date_from=date_from,
        date_to=date_to,
        path_type=path_type,
        featured=featured,
        private=private,
        page=page,
        user=current_user,
    )
    if current_user:
        validated_objs = []
        for db_obj in db_objs:
            if not db_obj.isPrivate or crud.role.has_responsibility(
                db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
            ):
                validated_objs.append(db_obj)
        db_objs = validated_objs
    return [
        crud.pathway.get_schema(db_obj=db_obj, language=language, schema_out=schemas.PathwaySummary)
        for db_obj in db_objs
    ]


@router.get("/featured", response_model=schemas.PathwaySummary)
def read_featured_pathway(
    *,
    db: Session = Depends(deps.get_db),
    language: str | None = None,
) -> Any:
    """
    Get a featured pathway.
    """
    db_obj = crud.pathway.get_featured(db=db)
    return crud.pathway.get_schema(db_obj=db_obj, language=language, schema_out=schemas.PathwaySummary)


@router.get("/personal", response_model=schemas.PathwaySummary)
def read_personal_pathway(
    *,
    db: Session = Depends(deps.get_db),
    language: str | None = None,
) -> Any:
    """
    Get a personal pathway to start.
    """
    db_obj = crud.pathway.get_featured(db=db, pathtype=schema_types.PathwayType.PERSONAL)
    return crud.pathway.get_schema(db_obj=db_obj, language=language, schema_out=schemas.PathwaySummary)


@router.get("/{id}", response_model=schemas.Pathway)
def get_pathway(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    language: str | None = None,
    current_user: models.User | None = Depends(deps.get_optional_current_user),
) -> Any:
    """
    Get a pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    responsibility = None
    if db_obj and current_user:
        responsibility = crud.role.highest_responsibility(db=db, user=current_user, pathway=db_obj)
    # if not db_obj or (db_obj.isPrivate and (not current_user or (current_user and not crud.role.has_responsibility))
    if not db_obj or (
        db_obj.isPrivate
        and (
            not current_user
            or (current_user and responsibility not in [schema_types.RoleType.CURATOR, schema_types.RoleType.CUSTODIAN])
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    response = crud.pathway.get_schema(db_obj=db_obj, language=language)
    response.responsibility = responsibility
    response.resources = []
    for resource_obj in db_obj.resources.all():
        resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
        response.resources.append(resources_out)
    response.themes = []
    for theme_obj in db_obj.themes.all():
        theme_out = crud.theme.get_schema(db_obj=theme_obj, language=language)
        theme_out.resources = []
        for resource_obj in theme_obj.resources.all():
            resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
            theme_out.resources.append(resources_out)
        theme_out.nodes = []
        for node_obj in theme_obj.nodes.all():
            node_out = crud.node.get_schema(db_obj=node_obj, language=language, schema_out=schemas.NodeJourney)
            node_out.resources = []
            for resource_obj in node_obj.resources.all():
                resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
                node_out.resources.append(resources_out)
            response_out = crud.response.get_formatted_response(db_obj=node_obj)
            if response_out:
                node_out.response = response_out
            theme_out.nodes.append(node_out)
        response.themes.append(theme_out)
    # Check if user, and user is busy with this pathway
    journey_path = None
    if current_user and not db_obj.isPrivate:
        if db_obj.pathType == "PERSONAL":
            # journey_path = crud.user.get_working_response(user=current_user, pathway=db_obj)
            journey_path = crud.pathway.get_next_theme(pathway=db_obj)
        else:
            # group_obj = crud.role.get_group_for_pathway(db=db, user=current_user, pathway=db_obj)
            journey_path = crud.pathway.get_next_theme(pathway=db_obj)
            # if group_obj:
            #     journey_path = crud.group.get_working_response(group=group_obj)
            # else:
            #     journey_path = crud.pathway.get_next_theme(pathway=db_obj)
        # if journey_path:
        #     journey_path = journey_path.id
    response.journeyPath = journey_path
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
    group_in = schemas.GroupCreate(
        **{
            "title": f"Admin group for {obj_in.title}",
            "language": obj_in.language,
            "isActive": False,
        }
    )
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
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CUSTODIAN
    ):
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    crud.pathway.remove(db=db, id=id)
    return {"msg": "Pathway has been successfully removed."}


@router.put("/{id}/toggle-state", response_model=schemas.Msg)
def toggle_state(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.PathwayUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Toggle pathway publication state (CURATOR function)
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
    ):
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    response = crud.pathway.update(db=db, db_obj=db_obj, obj_in=obj_in)
    if not response:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    return {"msg": "Publication state toggled successfully."}


@router.put("/{id}/featured", response_model=schemas.Msg)
def toggle_feature_state(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Toggle pathway featured state.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or researcher does not have the rights for this request.",
        )
    crud.pathway.toggle_featured(db=db, db_obj=db_obj)
    return {"msg": str(db_obj.id)}


@router.get("/{id}/download", response_class=StreamingResponse)
def download_pathway_model(*, db: Session = Depends(deps.get_db), id: str, language: str | None = None) -> Any:
    """
    Download a JSON model of a pathway.
    """
    db_obj = crud.pathway.get(db=db, id=id)
    if not db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    response = crud.pathway.get_schema(db_obj=db_obj, language=language)
    response.resources = []
    for resource_obj in db_obj.resources.all():
        resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
        response.resources.append(resources_out)
    response.themes = []
    for theme_obj in db_obj.themes.all():
        theme_out = crud.theme.get_schema(db_obj=theme_obj, language=language)
        theme_out.resources = []
        for resource_obj in theme_obj.resources.all():
            resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
            theme_out.resources.append(resources_out)
        theme_out.nodes = []
        for node_obj in theme_obj.nodes.all():
            node_out = crud.node.get_schema(db_obj=node_obj, language=language)
            node_out.resources = []
            for resource_obj in node_obj.resources.all():
                resources_out = crud.resource.get_schema(db_obj=resource_obj, language=language)
                node_out.resources.append(resources_out)
            theme_out.nodes.append(node_out)
        response.themes.append(theme_out)
    # https://stackoverflow.com/a/69799463/295606
    stream = io.StringIO(response.json(by_alias=True))
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename={response.name}-{response.language}.json",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )


@router.post("/import", response_model=schemas.Pathway)
def import_and_create_pathway(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.Pathway,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create a pathway from a saved JSON import. MUST be new to this database.
    """
    db_obj = crud.pathway.get(db=db, id=obj_in.id)
    if db_obj:
        raise HTTPException(
            status_code=400,
            detail="Either pathway exists, or user does not have the rights for this request.",
        )
    try:
        db_obj = create_or_update_from_import(db=db, obj_in=obj_in, user=current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=e,
        )
    return crud.pathway.get_schema(db_obj=db_obj, language=obj_in.language)


@router.put("/import/{id}", response_model=schemas.Pathway)
def import_and_update_pathway(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.Pathway,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a pathway from a saved JSON import. Tends to be for alternative language models.
    Updating a full pathway is likely to lead to a very tangled response.
    """
    db_obj = crud.pathway.get(db=db, id=str(obj_in.id))
    if (
        str(obj_in.id) != id
        or not db_obj
        or not crud.role.has_responsibility(
            db=db, user=current_user, pathway=db_obj, responsibility=schema_types.RoleType.CURATOR
        )
    ):
        raise HTTPException(
            status_code=400,
            detail="Either pathway does not exist, or user does not have the rights for this request.",
        )
    try:
        db_obj = create_or_update_from_import(db=db, obj_in=obj_in, user=current_user, db_obj=db_obj)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=e,
        )
    return crud.pathway.get_schema(db_obj=db_obj, language=obj_in.language)

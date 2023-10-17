from typing import Any
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/{id}", response_model=schemas.Response)
def get_response(
    *,
    db: Session = Depends(deps.get_db),
    id: str
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
    return crud.response.get_schema(db_obj=db_obj)


@router.post("/{id}", response_model=schemas.Response)
def create_response(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.ResponseCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create or Update a response.
    """
    # This is super complicated
    validates = True
    creates = True
    db_obj = crud.response.get(db=db, id=id)
    if db_obj:
        # Check if personal or group update
        if db_obj.node.pathway.pathType == schema_types.PathwayType.PERSONAL and db_obj.respondent_id != current_user.id:
            validates = False
        if db_obj.node.pathway.pathType == schema_types.PathwayType.RESEARCH and not crud.role.has_responsibility(
            db=db, user=current_user, pathway=db_obj.node.pathway, responsibility=schema_types.RoleType.RESEARCHER
        ):
            validates = False
        creates = False
        # Check if the response validates and double check - never trust what comes from the browser
        obj_in.validated = crud.response.validate(node=db_obj.node, response=obj_in)
    else:
        # Check if the pathway is personal or group ... if personal, either no pathway, or pathway match
        node_obj = crud.node.get(db=db, id=obj_in.node_id)
        if not node_obj:
            validates = False
        else:
            if node_obj.pathway.pathType == schema_types.PathwayType.RESEARCH and not crud.role.has_responsibility(
                db=db, user=current_user, pathway=node_obj.pathway, responsibility=schema_types.RoleType.RESEARCHER
            ):
                validates = False
            if node_obj.pathway.pathType == schema_types.PathwayType.PERSONAL:
                if current_user.responses.first() and current_user.responses.first().node.pathway_id != node_obj.pathway_id:
                    validates = False
            # Check if the response validates and double check - never trust what comes from the browser
            obj_in.validated = crud.response.validate(node=node_obj, response=obj_in)
    if not validates:
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    if creates:
        db_obj = crud.response.create(db=db, obj_in=obj_in)
    else:
        db_obj = crud.response.update(db=db, db_obj=db_obj, obj_in=obj_in)
    return crud.response.get_schema(db_obj=db_obj)

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

@router.get("/upload/{folder_id}/{source_id}", response_model=None)
async def get_upload_response(
    *,
    db: Session = Depends(deps.get_db),
    folder_id: str,
    source_id: str,
) -> StreamingResponse:
    """
    Download source from an uploaded response.
    """
    db_obj = crud.node.get(db=db, id=folder_id)
    if db_obj:
        db_obj = db_obj.responses.filter(
            (models.Response.node_id == folder_id)
            & (
                (models.Response.respondent_id == source_id)
                | (models.Response.group_id == source_id)
            )
        ).first()
    if not db_obj or not crud.files.exists(folder_id=folder_id, source_id=source_id):
        raise HTTPException(
            status_code=400,
            detail="Either the source response does not exist, or you do not have the rights for this request.",
        )
    stream = None
    if crud.files.use_spaces:
        if crud.spaces.exists(folder_id=folder_id, filename=source_id):
            stream = crud.spaces.get_stream(folder_id=folder_id, filename=source_id)
    if not stream:
        stream = crud.files.get(folder_id=folder_id, source_id=source_id)
    if not stream:
        raise HTTPException(
            status_code=400,
            detail="Either the source response does not exist, or you do not have the rights for this request.",
        )
    print(stream)
    # Get the answer dict: {id: , value: , dtype: }
    source_in = db_obj.answer  # [db_obj.language].answer
    media_type = source_in.get("dtype")
    if not media_type:
        media_type = "application/octet-stream"
    return StreamingResponse(
        content=stream,
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={source_in['value']}",
            "Access-Control-Expose-Headers": "Content-Disposition",
        },
    )

@router.post("/upload/{folder_id}/{source_id}", response_model=schemas.Msg)
async def create_upload_response(
    *,
    db: Session = Depends(deps.get_db),
    folder_id: str,
    source_id: str,
    files: list[UploadFile] = File(...),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create an upload source for a response.
    """
    db_obj = crud.node.get(db=db, id=folder_id)
    if db_obj and db_obj.pathway.pathType == schema_types.PathwayType.PERSONAL:
        if current_user.responses.first() and current_user.responses.first().node.pathway_id != db_obj.pathway_id:
            raise HTTPException(
                status_code=400,
                detail="Either root pathway does not exist, or user does not have the rights for this request.",
            )
    elif not db_obj or not crud.role.has_responsibility(
        db=db, user=current_user, pathway=db_obj.pathway, responsibility=schema_types.RoleType.RESEARCHER
    ):
        raise HTTPException(
            status_code=400,
            detail="Either root pathway does not exist, or user does not have the rights for this request.",
        )
    for source in files:
        try:
            crud.files.create(folder_id=folder_id, source_id=source_id, source=source)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=e,
            )
    return {
        "msg": "Source file successfully uploaded."
    }

@router.delete("/upload/{folder_id}/{source_id}", response_model=schemas.Msg)
async def remove_upload_response(
    *,
    db: Session = Depends(deps.get_db),
    folder_id: str,
    source_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove an uploaded source from a response.
    """
    db_obj = crud.node.get(db=db, id=folder_id)
    pathway_obj = None
    group_obj = None
    if db_obj:
        pathway_obj = db_obj.pathway
        group_obj = crud.group.get(db=db, id=source_id)
        db_obj = db_obj.responses.filter(
            (models.Response.node_id == folder_id)
            & (
                (models.Response.respondent_id == source_id)
                | (models.Response.group_id == source_id)
            )
        ).first()
    # db_obj doesn't exist, folder isn't the node id, and either use no group access, or isn't the respondent
    if not pathway_obj:
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    if pathway_obj.pathType == schema_types.PathwayType.PERSONAL and db_obj and db_obj.respondent_id != source_id:
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    elif pathway_obj.pathType == schema_types.PathwayType.RESEARCH and (not group_obj or not crud.role.has_responsibility(
        db=db, user=current_user, group=group_obj, pathway=pathway_obj, responsibility=schema_types.RoleType.RESEARCHER
    )):
        raise HTTPException(
            status_code=400,
            detail="Either response does not exist, or user does not have the rights for this request.",
        )
    crud.files.remove(folder_id=folder_id, source_id=source_id)
    return {
        "msg": "Source file successfully removed."
    }

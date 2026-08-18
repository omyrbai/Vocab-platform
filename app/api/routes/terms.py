from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.dependencies import get_term_service
from app.exceptions import ConflictError, NotFoundError
from app.schemas.term import TermRead, TermCreate, TermUpdate

router = APIRouter(
    prefix="/api/v1/terms",
    tags=["Terms"],
)

@router.get(
    "/",
    response_model=list[TermRead],
)
def get_terms(
    topic_id: int | None = None,
    src_lang_id: int | None = None,
    trg_lang_id: int | None = None,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = get_term_service(session)

    return term_service.get_filtered(
        topic_id=topic_id,
        src_lang_id=src_lang_id,
        trg_lang_id=trg_lang_id,
    )

@router.post(
    "/",
    response_model=TermRead,
    status_code=201,
)
def create_term(
    create_data: TermCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = get_term_service(session)
    try:
        return term_service.create(create_data)
    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.get(
    "/{term_id}",
    response_model=TermRead,
)
def get_term(
    term_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = get_term_service(session)

    term = term_service.get(term_id)

    if term is None:
        raise HTTPException(
            status_code=404,
            detail="Term not found.",
        )

    return term

@router.patch(
    "/{term_id}",
    response_model=TermRead,
)
def update_term(
    term_id: int,
    update_data: TermUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = get_term_service(session)

    try:
        return term_service.update(
            term_id,
            update_data,
        )

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

@router.delete(
    "/{term_id}",
    status_code=204,
)
def delete_term(
    term_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term_service = get_term_service(session)

    try:
        term_service.delete(term_id)

    except NotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
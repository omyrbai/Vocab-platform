from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.dependencies import get_language_service
from app.exceptions import ConflictError
from app.schemas.language import (
    LanguageRead,
    LanguageCreate,
    LanguageUpdate,
)

router = APIRouter(
    prefix="/api/v1/languages",
    tags=["Languages"],
)

@router.get(
    "/",
    response_model=list[LanguageRead],
)
def get_languages(
        session: Session = Depends(get_db),
):
    language_service = get_language_service(session)

    return language_service.get_all()

@router.get(
    "/{lang_id}",
    response_model=LanguageRead,
)
def get_language(
    lang_id: int,
    session: Session = Depends(get_db),
):
    language_service = get_language_service(session)

    language = language_service.get(lang_id)

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Language not found.",
        )
    return language

@router.post(
    "/",
    response_model=LanguageRead,
    status_code=201,
)
def create_language(
    create_data: LanguageCreate,
    session: Session = Depends(get_db),
):
    language_service = get_language_service(session)

    try:
        return language_service.create(create_data)
    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

@router.patch(
    "/{lang_id}",
    response_model=LanguageRead,
)
def update_language(
    lang_id: int,
    update_data: LanguageUpdate,
    session: Session = Depends(get_db),
):
    language_service = get_language_service(session)
    language = language_service.get(lang_id)

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Language not found.",
        )

    try:
        return language_service.update(
            language,
            update_data,
        )

    except ConflictError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

@router.delete(
    "/{lang_id}",
    status_code=204,
)
def delete_language(
    lang_id: int,
    session: Session = Depends(get_db),
):
    language_service = get_language_service(session)

    language = language_service.get(lang_id)

    if language is None:
        raise HTTPException(
            status_code=404,
            detail="Language not found.",
        )

    language_service.delete(language)

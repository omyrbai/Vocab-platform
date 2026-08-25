from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_current_user,
    require_admin,
)
from app.db.models.user import User
from app.dependencies import get_language_service
from app.exceptions import NotFoundError
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
):
    language_service = get_language_service(session)

    language = language_service.get(lang_id)

    if language is None:
        raise NotFoundError(
            "Language not found."
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
    current_user: User = Depends(require_admin),
):
    language_service = get_language_service(session)

    return language_service.create(create_data)

@router.patch(
    "/{lang_id}",
    response_model=LanguageRead,
)
def update_language(
    lang_id: int,
    update_data: LanguageUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    language_service = get_language_service(session)
    language = language_service.get(lang_id)

    if language is None:
        raise NotFoundError(
            "Language not found."
        )

    return language_service.update(
        language,
        update_data,
    )

@router.delete(
    "/{lang_id}",
    status_code=204,
)
def delete_language(
    lang_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    language_service = get_language_service(session)

    language = language_service.get(lang_id)

    if language is None:
        raise NotFoundError(
            "Language not found."
        )

    language_service.delete(language)

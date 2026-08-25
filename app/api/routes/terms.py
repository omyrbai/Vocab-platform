from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.db.models.user import User
from app.enums.user_role import UserRole
from app.dependencies import get_term_service
from app.exceptions import NotFoundError
from app.schemas.term import TermRead, TermCreate, TermUpdate

router = APIRouter(
    prefix="/api/v1/terms",
    tags=["Terms"],
)

def get_term_user_id(
    current_user: User,
) -> int | None:
    if current_user.role == UserRole.ADMIN:
        return None

    return current_user.user_id
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
        user_id=get_term_user_id(current_user),
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

    return term_service.create(
        user_id=get_term_user_id(current_user),
        create_data=create_data,
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

    term = term_service.get(
        user_id=get_term_user_id(current_user),
        term_id=term_id,
    )

    if term is None:
        raise NotFoundError(
            "Term not found."
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


    return term_service.update(
        user_id=get_term_user_id(current_user),
        term_id=term_id,
        update_data=update_data,
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

    term_service.delete(
        user_id=get_term_user_id(current_user),
        term_id=term_id,
    )
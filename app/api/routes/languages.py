from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.dependencies import get_language_service

router = APIRouter(
    prefix="/api/v1/languages",
    tags=["Languages"],
)

@router.get("/")
def get_languages(
        session: Session = Depends(get_db),
):
    language_service = get_language_service(session)

    return language_service.get_all()


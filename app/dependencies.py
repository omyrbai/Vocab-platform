from sqlalchemy.orm import Session

from app.repositories.language_repository import LanguageRepository
from app.repositories.term_repository import TermRepository
from app.repositories.topic_repository import TopicRepository
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_identity_repository import UserIdentityRepository

from app.services.auth_service import AuthService
from app.services.language_service import LanguageService
from app.services.term_service import TermService
from app.services.topic_service import TopicService
from app.services.user_service import UserService

def get_user_service(
    session: Session,
) -> UserService:
    return UserService(
        repository=UserRepository(session),
        language_repository=LanguageRepository(session),
    )


def get_language_service(
    session: Session,
) -> LanguageService:
    return LanguageService(
        repository=LanguageRepository(session),
    )


def get_topic_service(
    session: Session,
) -> TopicService:
    return TopicService(
        repository=TopicRepository(session),
    )


def get_term_service(
    session: Session,
) -> TermService:
    return TermService(
        term_repository=TermRepository(session),
        language_repository=LanguageRepository(session),
        topic_repository=TopicRepository(session),
    )

def get_auth_service(
    session: Session,
) -> AuthService:
    return AuthService(
        session=session,
        user_repository=UserRepository(session),
        identity_repository=UserIdentityRepository(session),
        refresh_token_repository=RefreshTokenRepository(session),
    )
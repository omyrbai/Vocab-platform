from fastapi import FastAPI

from app.api.exception_handlers import (
    authentication_exception_handler,
    conflict_exception_handler,
    forbidden_exception_handler,
    not_found_exception_handler,
)

from app.api.routes.auth import router as auth_router
from app.api.routes.languages import router as languages_router
from app.api.routes.terms import router as terms_router
from app.api.routes.topics import router as topics_router
from app.api.routes.users import router as users_router
from app.exceptions import (
    AuthenticationError,
    ConflictError,
    ForbiddenError,
    NotFoundError,
)

app = FastAPI(
    title="Vocab Platform API",
    version="1.0.0",
)

app.add_exception_handler(
    ForbiddenError,
    forbidden_exception_handler,
)

app.add_exception_handler(
    NotFoundError,
    not_found_exception_handler,
)

app.add_exception_handler(
    ConflictError,
    conflict_exception_handler,
)

app.add_exception_handler(
    AuthenticationError,
    authentication_exception_handler,
)

app.include_router(auth_router)
app.include_router(languages_router)
app.include_router(topics_router)
app.include_router(terms_router)
app.include_router(users_router)
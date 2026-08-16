from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.languages import router as languages_router
from app.api.routes.terms import router as terms_router
from app.api.routes.topics import router as topics_router
from app.api.routes.users import router as users_router


app = FastAPI(
    title="Vocab Platform API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(languages_router)
app.include_router(topics_router)
app.include_router(terms_router)
app.include_router(users_router)
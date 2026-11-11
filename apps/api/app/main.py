from fastapi import APIRouter, FastAPI

from app.routers import grades, groups, health, labs, submissions

app = FastAPI(title="StudyHub API", version="0.1.0")

# Єдиний префікс API задається тут, а не в окремих роутерах.
api = APIRouter(prefix="/api/v1")
api.include_router(health.router)
api.include_router(labs.router)
api.include_router(submissions.router)
api.include_router(grades.router)
api.include_router(groups.router)
app.include_router(api)

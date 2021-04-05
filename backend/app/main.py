from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.requests import Request
import uvicorn

from app.api.api_v1.routers.users import users_router
from app.api.api_v1.routers.auth import auth_router
from app.api.api_v1.routers.words import words_router
from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user

# from core.celery_app import celery_app
# import tasks


app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}


@app.get("/audio")
async def main():
    return FileResponse(
        "/app/app/static/audio/00_00_12-00_00_14-albert_laszlo_barabasi_the_real_relationship_between_your_age_and_your_chance_of_success.mp3"
    )


# @app.get("/api/v1/task")
# async def example_task():
#     celery_app.send_task("app.tasks.example_task", args=["Hello World"])
#
#     return {"message": "success"}


# Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(words_router, prefix="/api/v1", tags=["words"])

app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8888, log_level='debug', reload_delay=0.1)
# uvicorn main:app --reload --host="0.0.0.0" --port="8888"

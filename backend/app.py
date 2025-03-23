from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.middleware.sessions import SessionMiddleware

from backend.routers.image_route import api_image
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(
    SessionMiddleware,
    secret_key="89afb902-f84d-49c9-b89e-2be6f2389b1d",
    session_cookie="color-finder-webproject-session",
    https_only=True
)

api = APIRouter(prefix="/api")
api.include_router(api_image)

app.include_router(api)

def swagger_config():
    description = """Google Chrome extension where you can crop an image from a webpage. Another tab will be open with an website where it is possible to vizualize the color anmes from your image."""
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Color Finder Extension",
        version="0.1",
        description=description,
        routes=app.routes
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = swagger_config
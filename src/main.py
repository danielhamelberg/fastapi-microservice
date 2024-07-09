from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from .database import engine, get_db
from . import models, schemas
from auth.utils import get_current_active_user
from auth.decorators import admin_required, moderator_required
from .services.post_service import PostService
from .core.logging import setup_logging
from scripts.run_migrations import run_migrations

logger = setup_logging()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware function to log incoming requests and outgoing responses.

    Args:
        request (Request): The incoming request object.
        call_next (Callable): The next middleware or route handler.

    Returns:
        Response: The outgoing response object.
    """
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Outgoing response: {response.status_code}")
    return response


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """
    Returns the custom Swagger UI HTML page.

    This function generates and returns the HTML page for the Swagger UI.
    It specifies the OpenAPI URL, title, OAuth2 redirect URL, and the URLs for the Swagger UI JavaScript and CSS files.

    Returns:
        str: The custom Swagger UI HTML page.
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Documentation",
        oauth2_redirect_url="/docs/oauth2-redirect",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    """
    Returns the OpenAPI specification for the FastAPI Microservice.

    Returns:
        dict: The OpenAPI specification as a dictionary.
    """
    return get_openapi(
        title="FastAPI Microservice",
        version="1.0.0",
        description="This is a microservice built with FastAPI",
        routes=app.routes,
    )


@app.post("/posts", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
@admin_required
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_active_user)):
    """
    Create a new post.

    Args:
        post (schemas.PostCreate): The data for the new post.
        db (Session, optional): The database session. Defaults to Depends(get_db).
        user (models.User, optional): The current active user. Defaults to Depends(get_current_active_user).

    Returns:
        schemas.PostResponse: The created post.
    """
    post_service = PostService(db)
    return post_service.create_post(post, user)

if __name__ == "__main__":
    run_migrations()
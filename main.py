from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
import importlib

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# Include routers from installed apps
for app_name in settings.INSTALLED_APPS:
    try:
        module = importlib.import_module(f"apps.{app_name}.routes")
        router = getattr(module, "router")
        app.include_router(router, prefix=f"{settings.API_V1_STR}/{app_name}")
    except (ImportError, AttributeError):
        print(f"Warning: Could not import router for app '{app_name}'")

@app.get("/")
async def root():
    return {"message": "Welcome to the Advanced FastAPI Project v2"}


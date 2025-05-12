from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings
from config.validator import validate_on_startup
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Get settings
settings = get_settings()

# Validate environment variables on startup
validate_on_startup()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Import and include routers
from routes import auth, tasks, agents, contexts

# Include routers with API prefix
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(tasks.router, prefix=settings.API_V1_PREFIX)
app.include_router(agents.router, prefix=settings.API_V1_PREFIX)
app.include_router(contexts.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {
        "status": "ok",
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }
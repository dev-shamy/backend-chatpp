"""Main FastAPI application"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db.base import Base
from app.db.session import engine
import uvicorn
from app.websocket.main import router as websocket_router
from app.api.routes.auth import router as auth_routes

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(websocket_router)
app.include_router(auth_routes)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Chat Application API",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

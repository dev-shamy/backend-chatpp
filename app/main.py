"""Main FastAPI application"""
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db.base import Base
from app.db.session import engine
import uvicorn
from socketio_app.main import sio, register_socket_events
from app.api.routes.auth import router as auth_routes
from app.api.routes.user import router as user_routes
import socketio  # type: ignore

# Setup logging
setup_logging()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
fastapi_app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


fastapi_app.include_router(auth_routes)
fastapi_app.include_router(user_routes)

@fastapi_app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Chat Application API",
    }


@fastapi_app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Now wrap FastAPI app with socketio ASGI app for the final combined ASGI app:
app = socketio.ASGIApp(
    socketio_server=sio,
    other_asgi_app=fastapi_app,
    socketio_path="socket.io",
)

# Register socket events
register_socket_events(sio)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

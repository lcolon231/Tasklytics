from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
import os

from app.routers import auth, tasks, notifications, users
from app.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    start_scheduler()
    yield
    # Shutdown - scheduler will stop automatically


app = FastAPI(
    title="Task Tracker API",
    version="1.0.0",
    description="A comprehensive task management API with notifications and reminders",
    lifespan=lifespan
)

# CORS middleware - IMPORTANT: Add localhost:5173 for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tasklytics.dev",
        "https://www.tasklytics.dev",
        "http://localhost:3000",
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173"  # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def api_root():
    """API root endpoint"""
    return {
        "message": "Task Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "task-tracker-api"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return favicon - prevents 404 errors in browser"""
    return Response(status_code=204)


# Serve React app static files (if needed)
if os.path.exists("frontend/dist"):
    app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")


    @app.get("/app", tags=["Frontend"])
    def serve_react_app():
        """Serve the React application"""
        return FileResponse("frontend/dist/index.html")

# Include API routers with proper prefixes
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Import and include tasks router
try:
    from app.routers import tasks

    app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
except ImportError:
    # Tasks router not yet created
    pass

# Import and include other routers
try:
    from app.routers import notifications

    app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
except ImportError:
    pass

try:
    from app.routers import users

    app.include_router(users.router, prefix="/users", tags=["Users"])
except ImportError:
    pass


# Additional middleware for security headers
@app.middleware("http")
async def add_security_headers(request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
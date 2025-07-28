from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# ✅ CORSMiddleware applied FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Task Tracker API"}

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")

@app.get("/")
def serve_react_app():
    return FileResponse(os.path.join("frontend", "dist", "index.html"))

# ✅ Only one router to test cleanly
app.include_router(auth.router, prefix="/auth")
